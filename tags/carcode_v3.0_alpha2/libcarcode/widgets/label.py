from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from widget import Widget

class Label(Widget):
    """Label widget
        Simple widget to display text, cannot be resized and its size is
        determined according to the text and font.
    """
    def __init__(self, text, *args,  **kargs):
        """Label
        
            @param text string to be display
            @param pos touple position (x, y)
        """
        Widget.__init__(self,  *args,  **kargs)
        
        self.text = text
        self.size = [len(text) * 8, 13]
        self.visible = True
    
    def set_text(self, text):
        """Sets the label text"""
        self.text = text
        self.size = [len(text) * 8, 13]
        
    def events(self, event):
        return False
    
    def set_size(self,  size):
        # Labels cannot be resized
        pass
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        
        glColor4f(*self.fontcolor)
        
        glRasterPos3i(0, 10, 0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
            
        glPopMatrix()
