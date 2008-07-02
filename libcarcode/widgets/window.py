from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label

class Dummy:
    pass

class Window:
    def __init__(self, label, pos, size, color, modal = False):
        self.label = Label(label, (4,12), COLOR_WHITE)
        self.pos = pos
        self.size = size
        self.color = color
        self.entities = []
        self.focus = True
        self.modal = modal
        
    def add_entity(self, entity):
        self.entities.append(entity)
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRecti(0, 0, self.size[0], self.size[1])
        
        if self.focus:
            glColor3ub(0, 0, 200)
        else:
            glColor3ub(100, 100, 100)
        glRecti(0, 0, self.size[0], 15)
        
        self.label.draw()
        
        glTranslatef(2, 17, 0)
        for entity in self.entities:
            entity.draw()
        glPopMatrix()
    def events(self, event):
        if event.type == MOUSEBUTTONUP and not self.modal:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.focus = True
            else:
                self.focus = False
                return False
        if self.focus:
            if event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
                nevent = Dummy()
                nevent.type = event.type
                nevent.pos = (event.pos[0] - self.pos[0] - 2, event.pos[1] - self.pos[1] - 17)
            else:
                nevent = event
            for entity in self.entities:
                if entity.events(nevent):
                    return True
        if self.modal:
            return True
        return False