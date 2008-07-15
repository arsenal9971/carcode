from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from utils import Clipper
from widget import Widget

TXTKEYS = {
        K_SPACE: ' '
        }

for x in xrange(ord('a'), ord('z')+1):
    TXTKEYS[x] = chr(x)
    
for x in xrange(ord('0'), ord('9')+1):
    TXTKEYS[x] = chr(x)
    
class TextBox(Widget):
    """ Simple text line editing widget """
    def __init__(self, *args,  **kargs):
        """TextBox
            
            @param pos tuple with widget position (x, y)
            @param size tuple with widget size (width, height)
        """
        Widget.__init__(self,  *args,  **kargs)
        self.text = ""
        self.focus = False
        self.cursor = 0
        self.visible = True
        
    def set_text(self, text):
        """ Set the widget text
        
            @param text string to edit, will not handle multiline strings
        """
        self.text = text
        
    def get_text(self):
        """ Gets the widget text 
            
            @return string with current widget text
        """
        return self.text
    
    def events(self, event):
        if event.type == KEYUP and self.focus:
            return True
        if event.type == KEYDOWN and self.focus:
            clen = len(self.text)
            if event.key == K_BACKSPACE:
                if clen > 0 and self.cursor > 0:
                    if self.cursor == clen:
                        self.text = self.text[0:-1]
                    else:
                        self.text = self.text[0:self.cursor-1] + self.text[self.cursor:clen]
                    self.cursor -= 1
            elif event.key == K_DELETE:
                if self.cursor < clen and clen > 0:
                    self.text = self.text[0:self.cursor] + self.text[self.cursor+1:clen]
            elif event.key == K_LEFT:
                if self.cursor > 0:
                    self.cursor -= 1
            elif event.key == K_RIGHT:
                if self.cursor < clen:
                    self.cursor += 1
            elif event.key == K_UP:
                pass
            elif event.key == K_DOWN:
                pass
            elif event.key == K_RETURN or event.key == K_KP_ENTER:
                pass
            else:
                try:
                    char = event.unicode.encode('latin-1')
                    if char:
                        self.text += char
                        self.cursor += 1
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
        
        glColor4f(*self.forecolor)
        glRecti(0, 0, self.size[0], self.size[1])
        
        glColor4f(*self.backcolor)
        glRecti(1, 1, self.size[0]-1, self.size[1]-1)
        
        clip = Clipper()
        clip.begin((1, 1, self.size[0]-1, self.size[1]-1))
        
        glPushMatrix()
        glTranslatef(2, 13, 0)
        
        glColor4f(*self.fontcolor)
        glRasterPos3i(0, 0, 0)
        
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
            
        glPopMatrix()
        
        if self.focus:
            x = (self.cursor*8) + 2
            glRecti(x, 0, x+4, 13)
            
        clip.end()
        glPopMatrix()
