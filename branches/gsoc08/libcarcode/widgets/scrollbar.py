from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from button import Button
from constants import *
from events import EventDispatcher
from label import Label
from utils import Clipper, mangle_event
from widget import Widget

def Quad(v1, v2):
    glBegin(GL_LINE_STRIP)
    glVertex2f(v1[0], v1[1])
    glVertex2f(v2[0], v1[1])
    glVertex2f(v2[0], v2[1])
    glVertex2f(v1[0], v2[1])
    glVertex2f(v1[0], v1[1])
    glEnd()

class Arrow:
    def __init__(self, size, orientation):
        self.size = size
        self.orientation = orientation
    def draw(self):
        glPushMatrix()
        glScalef(self.size[0], self.size[1], 1.0)
        glBegin(GL_TRIANGLES)
        glColor4f(*COLOR_WHITE)
        if self.orientation == 1:
            glVertex2f(0.0, 1.0)
            glVertex2f(0.5, 0.0)
            glVertex2f(1.0, 1.0)
        else:
            glVertex2f(0.0, 0.0)
            glVertex2f(0.5, 1.0)
            glVertex2f(1.0, 0.0)
        glEnd()
        glPopMatrix()
        
class ScrollBar(Widget):
    """ Simple scroll bar """
    def __init__(self, orientation = VERTICAL,  maxval = 100,  *args,  **kargs):
        """ ScrollBar
        
            @param orientation scrollbar orientation, either VERTICAL or HORIZONTAL
            @param maxval maximum scroll value (default 100)
            @param pos tuple with widget position (x, y)
            @param size tuple with widget size (width, height)
        """
        Widget.__init__(self,  *args,  **kargs)
        self.maxval = maxval
        self.value = 0
        self.onScroll = EventDispatcher()
        self.selected = -1
        self.visible = True
        
        self.arrowup = Button(Arrow((self.size[0],12), 1), (0 ,0), (self.size[0],12), backcolor=self.backcolor)
        self.arrowdown = Button(Arrow((self.size[0],12), 0), (0, self.size[1]-12), (self.size[0],12), backcolor=self.backcolor)
        
        self.barh = (self.size[1] - 24) / 5
        self.maxy = self.size[1] - self.barh - 24
        
        self.arrowup.onClick.subscribe(self.scrollup)
        self.arrowdown.onClick.subscribe(self.scrolldown)
        self.startitem = 0
        self.maxoffset = 0
    
    def set_value(self,  val):
        """ Set the scrollbar value
        
        @param val number for value 
        """
        self.value = value
        
    def get_value(self):
        """ Get the current scrollbar value
        
        @return scrollbar value
        """
        return self.value
        
    def set_maxvalue(self,  maxval):
        """ Set the maximum allowed value for scrollbar
        
        @param maxval number for maximum value
        """
        self.maxval = maxval
    
    def scrollup(self, btn):
        if self.value > 0:
            self.value -= 1;
            
    def scrolldown(self, btn):
        if self.value < self.maxval:
            self.value += 1;
        
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            
            nevent = mangle_event(event, self.pos)
            
            if inX(event.pos[0]) and inY(event.pos[1]):
                if self.arrowup.events(nevent) or self.arrowdown.events(nevent):
                    return True
        return False
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        
        glColor4f(*self.forecolor)
        glRecti(0, 0, self.size[0], self.size[1])
        
        glColor4f(*self.backcolor)
        glRecti(1, 1, self.size[0]-1, self.size[1]-1)
        
        self.arrowup.draw()
        self.arrowdown.draw()
        
        #Quad((self.size[0]-13, 0), (self.size[0],self.size[1]-1))
        
        glColor4f(*self.forecolor)
        
        by = 12 + (((self.maxy) / self.maxval) * self.value)
        
        glRecti(0, by, self.size[0], by + self.barh)
        
        glPopMatrix()
