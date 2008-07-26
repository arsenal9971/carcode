from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from label import Label

# TODO: Add input support, with a textbox and process input
class Console:
    """ Small interactive text console """
    def __init__(self, pos,  size,  maxlines = 3):
        """Console
        
        @param pos tuple with widget position (x, y)
        @param size tuple with widget size (width, height)
        @param maxlines max lines to display, default 3
        """
        self.maxlines = maxlines
        self.pos = pos
        self.size = size
        self.lines = []
        self.visible = True
        
        x = pos[0]
        y = pos[1] + (maxlines * 13)
        
        for i in xrange(maxlines):
            label = Label("",  pos=(x, y))
            self.lines.append(label)
            y -= 13
        
        self.strlist = []
    
    def events(self,  event):
        return False
        
    def update(self):
        i = 0
        for label in self.lines:
            if i == len(self.strlist):
                return
            line = self.strlist[i]
            label.set_text(line)
            i += 1
            
    def clear(self):
        """ Clear console lines """
        try:
            while True:
                l = self.strlist.pop()
                del l
        except IndexError:
            pass
        for label in self.lines:
            label.set_text("")
            
    def draw(self):
        for line in self.lines:
            line.draw()
            
    def write(self, string):
        """ Write a string line to console widget
        
        @param string one line string to print
        """
        if len(self.strlist) == self.maxlines:
            line = self.strlist.pop()
            del line
        self.strlist.insert(0,  string)
        self.update()
