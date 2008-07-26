from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label
from widget import Widget

class Button(Widget):
    """Button widget class"""
    
    def __init__(self, contents,  *args,  **kargs):
        """Button
        
        @param contents widget to display inside button, most common Label
        @param pos tuple with widget position (x, y)
        @param size tuple with widget size (width, height)
        """
        Widget.__init__(self,  *args,  **kargs)
        
        lx = (self.size[0] / 2) - (contents.size[0] / 2)
        ly = (self.size[1] / 2) - (contents.size[1] / 2)
        
        self.contents = contents
        self.contents.pos = [lx, ly]
        
        self.color = color
        self.onClick = EventDispatcher()
        self.visible = True
    
    def set_size(self, size):
        """Changes the size of the widget
        
            @param size tuple with size (width, height)
        """
        Widget.set_size(self,  size)
        
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
        
        glColor4f(*self.backcolor)
        glRecti(0, 0, self.size[0], self.size[1])
        
        self.contents.draw()
        
        glPopMatrix()
