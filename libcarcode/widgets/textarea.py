from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from utils import Clipper

TXTKEYS = {
        K_SPACE: ' ',
        }

for x in xrange(K_EXCLAIM, ord('z')+1):
    TXTKEYS[x] = chr(x)

class TextArea:
    """ Multiline text editing widget """
    def __init__(self, pos, size, color):
        """TextBox
            
            @param pos tuple with widget position (x, y)
            @param size tuple with widget size (width, height)
            @param color tuple with font color (r, g, b, a)
        """
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.text = [""]
        self.focus = False
        self.xcursor = 0
        self.ycursor = 0
        self.srow = 0
        self.mrow = size[1] / 13
        self.visible = True
        
    def set_text(self, text):
        """ Set the widget text
        
            @param text string to edit
        """
        self.text = text.split('\n')
        
    def get_text(self):
        """ Gets the widget text 
            
            @return string with current widget text
        """
        ret = ''
        for line in self.text:
            ret += line + '\n'
        return ret
    
    def row(self):
        if len(self.text) == 1:
            return 0
        if self.ycursor < len(self.text):
            return self.ycursor
        
    def events(self, event):
        if event.type == KEYUP and self.focus:
            return True
        if event.type == KEYDOWN and self.focus:
            cline = self.text[self.ycursor]
            clen = len(cline)
            if event.key == K_BACKSPACE:
                if clen > 0:
                    if self.xcursor == clen:
                        self.text[self.ycursor] = cline[0:-1]
                    else:
                        self.text[self.ycursor] = cline[0:self.xcursor-1] + cline[self.xcursor:clen]
                    self.xcursor -= 1
                else:
                    if len(self.text) > 0 and self.ycursor > 0:
                        del self.text[self.ycursor]
                        self.ycursor -= 1
                        self.xcursor = len(self.text[self.ycursor])
            elif event.key == K_DELETE:
                if self.xcursor < clen:
                    self.text[self.ycursor] = cline[0:self.xcursor] + cline[self.xcursor+1:clen]
            elif event.key == K_LEFT:
                if self.xcursor > 0:
                    self.xcursor -= 1
            elif event.key == K_RIGHT:
                if self.xcursor < len(self.text[self.ycursor]):
                    self.xcursor += 1
            elif event.key == K_UP:
                if self.ycursor > 0:
                    self.ycursor -= 1
                    if len(self.text[self.ycursor]) < self.xcursor:
                        self.xcursor = len(self.text[self.ycursor])
                return True
            elif event.key == K_DOWN:
                if self.ycursor < len(self.text)-1:
                    self.ycursor += 1
                    if len(self.text[self.ycursor]) < self.xcursor:
                        self.xcursor = len(self.text[self.ycursor])
                return True
            elif event.key == K_RETURN or event.key == K_KP_ENTER:
                if self.xcursor == clen:
                    itext = ""
                else:
                    itext = cline[self.xcursor:clen]
                    self.text[self.ycursor] = cline[0:self.xcursor]
                self.ycursor += 1
                self.xcursor = 0
                if self.ycursor < len(self.text) -1:
                    self.text.append(itext)
                else:
                    self.text.insert(self.ycursor, itext)
            else:
                try:
                    char = event.unicode.encode('latin-1')
                    l = len(self.text[self.ycursor])
                    if char:
                        self.text[self.ycursor] = self.text[self.ycursor][0:self.xcursor] + char + self.text[self.ycursor][self.xcursor:l]
                        self.xcursor += 1
                except:
                    pass
            return True
            
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.focus = True
                return True
            else:
                self.focus = False
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRecti(0, 0, self.size[0], self.size[1])
        glColor3f(0,0,0)
        glRecti(1, 1, self.size[0]-1, self.size[1]-1)
        clip = Clipper()
        clip.begin((1, 1, self.size[0]-1, self.size[1]-1))
        glPushMatrix()
        glTranslatef(2, 13, 0)
        glColor4f(*COLOR_WHITE)
        glRasterPos3i(0, 0, 0)
        li = 0
        for line in self.text:
            for c in line:
                glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
            li += 13
            glRasterPos3i(0, li, 0)
        glPopMatrix()
        if self.focus:
            x = (self.xcursor*8) + 2
            y = (self.ycursor*13) + 2
            glRecti(x, y, x+4, y+13)
        clip.end()
        glPopMatrix()
