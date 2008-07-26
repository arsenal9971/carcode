from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label
from utils import Clipper, mangle_event
from widget import Widget

class Window(Widget):
    """ Toplevel window container """
    def __init__(self, label, modal= False,  *args,  **kargs):
        """Window
        
            @param label string for the window title header
            @param modal window modal
            @param pos tuple with widget position (x, y)
            @param size tuple with widget size (width, height)
        """
        Widget.__init__(self,  *args,  **kargs)
        
        self.label = Label(label, pos=(2,2),  fontcolor=COLOR_WHITE)
        self.entities = []
        self.focus = True
        self.modal = modal
        self.visible = True
        
    def add_entity(self, entity):
        """ Add a widget to the window
            
            @param entity object which implements the widget protocol
        """
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
        glColor4f(*self.backcolor)
        glRecti(0, 0, self.size[0], self.size[1])
        
        clip = Clipper()
        clip.begin((0, 0, self.size[0], self.size[1]))
        
        for entity in self.entities:
            entity.draw()
        
        clip.end()
        
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
            nevent = mangle_event(event, (self.pos[0], self.pos[1]+17))
            
            for entity in self.entities:
                if entity.events(nevent):
                    return True
                
        if self.modal:
            return True
        
        return False
