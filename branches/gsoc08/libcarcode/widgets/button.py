from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label

class Button:
    """Button widget class"""
    
    def __init__(self, contents, pos, size, color):
        lx = (size[0] / 2) - (contents.size[0] / 2)
        ly = (size[1] / 2) - (contents.size[1] / 2)
        
        self.contents = contents
        self.contents.pos = [lx, ly]
        
        self.color = color
        self.pos = pos
        self.size = size
        self.onClick = EventDispatcher()
        self.visible = True
    
    def resize(self, size):
        """Changes the size of the widget
        
            size - a tuple with (width, height)
        """
        self.size = size
        lx = (size[0] / 2) - (self.contents.size[0] / 2)
        ly = (size[1] / 2) - (self.contents.size[1] / 2)
        self.contents.pos = [lx, ly]
        
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.onClick.dispatch(self)
                return True
            
        return False
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRecti(0, 0, self.size[0], self.size[1])
        
        self.contents.draw()
        
        glPopMatrix()
