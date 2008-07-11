from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

class Console:
    def __init__(self, maxlines = 3):
        self.maxlines = maxlines
        self.lines = []
        
    def clear(self):
        try:
            while True:
                l = self.lines.pop()
                del l
        except IndexError:
            pass
            
    def draw(self):
        glPushMatrix()
        glLoadIdentity()
        y = 12
        for line in self.lines:
            glRasterPos2i(0, y)
            for c in line:
                glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
            y += 12
        glPopMatrix()
            
    def write(self, string):
        if len(self.lines) == self.maxlines:
            line = self.lines.pop(0)
            del line
        self.lines.append(string)