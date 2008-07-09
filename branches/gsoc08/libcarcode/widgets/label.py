from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *

class Label:
    """Label widget
        Simple widget to display text, cannot be resized and its size is
        determined according to the text and font.
    """
    def __init__(self, text, pos = (0,0), color = COLOR_WHITE):
        """Label
        
            @param text string to be display
            @param pos touple position (x, y)
            @param color touple of 4 floats (0.0-1.0) describing font color (r, g, b, a)
        """
        self.text = text
        self.pos = list(pos)
        self.color = color
        self.size = [len(text) * 8, 13]
        self.visible = True
    
    def set_text(self, text):
        """Sets the label text"""
        self.text = text
        self.size = [len(text) * 8, 13]
        
    def events(self, event):
        return False
    
    def resize(self, size):
        pass
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        
        glRasterPos3i(0, 10, 0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
            
        glPopMatrix()
