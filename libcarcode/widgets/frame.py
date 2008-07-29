from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label
from utils import Clipper,  mangle_event
from widget import Widget

class Frame(Widget):
    """ Widget decorator frame with label on top """
    def __init__(self, label, *args,  **kargs):
        """Frame
            
        @param label string to use as frame label
        @param pos tuple with widget position (x, y)
        @param size tuple with widget size (width, height)
        """
        Widget.__init__(self,  *args,  **kargs)
        
        self.label = Label(label)
        self.label.set_pos((5, 0))
        
        self.entity = None
    
    def set_entity(self, obj):
        self.entity = obj
        self.entity.set_pos((0,0))
        self.entity.set_size((self.size[0]-2,self.size[1]-15))
        
    def on_resize(self):
        self.entity.set_pos((0,0))
        self.entity.set_size((self.size[0]-2,self.size[1]-15))
    
    def events(self, event):
        pos = (self.pos[0] + 1, self.pos[1] + 13)
        nevent = mangle_event(event, pos)
        
        if self.entity is not None:
            return self.entity.events(nevent)
        return False
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        
        glColor3f(*self.forecolor)
        glRecti(self.pos[0], self.pos[1]+6, self.size[0], self.size[1])
        
        glColor3f(*self.backcolor)
        glRecti(self.pos[0]+1, self.pos[1]+7, self.size[0]-1, self.size[1]-1)
        
        glRecti(self.label.pos[0], self.label.pos[1], self.label.size[0], self.label.size[1])
        self.label.draw()
        
        if self.entity is not None:
            glTranslatef(1, 13, 0)
            self.entity.draw()
        
        glPopMatrix()