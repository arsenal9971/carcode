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
        self.label = Label(label, pos=(2,2))
        self.pos = pos
        self.size = size
        self.color = color
        self.entities = []
        self.focus = True
        self.modal = modal
        
    def add_entity(self, entity):
        self.entities.append(entity)
        
    def draw(self):
        # Move to position
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        
        # Draw title bar
        if self.focus:
            glColor3ub(0, 0, 200)
        else:
            glColor3ub(100, 100, 100)
        glRecti(0, 0, self.size[0], 15)
        
        # Draw title bar label
        self.label.draw()
        
        # Translate to usable window region
        glTranslatef(0, 15, 0)
        
        # Draw window background
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRecti(0, 0, self.size[0], self.size[1])
        
        # Enable stencil test for clipping
        glClear(GL_STENCIL_BUFFER_BIT)
        glEnable(GL_STENCIL_TEST)
        
        # Draw window region in stencil buffer
        glColorMask(GL_FALSE,GL_FALSE,GL_FALSE,GL_FALSE)
        glStencilOp(GL_REPLACE,GL_REPLACE,GL_REPLACE)
        glStencilFunc(GL_ALWAYS,1,1)
        
        glRecti(0, 0, self.size[0], self.size[1])
        
        # Draw entities testing against stencil for visible parts,
        # everything inside stencil will be draw.
        glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE)
        glStencilFunc(GL_EQUAL,1,1)
        glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
        
        for entity in self.entities:
            entity.draw()
        
        # Disable stencil tests
        glDisable(GL_STENCIL_TEST)
        
        # Restore transformation matrix
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