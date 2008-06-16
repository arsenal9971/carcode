from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

class Console:
    def __init__(self):
        self.maxlines = 3
        self.lines = []
        
    def draw(self, screen):
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
            line = self.lines.pop()
            del line
        self.lines.append(string)