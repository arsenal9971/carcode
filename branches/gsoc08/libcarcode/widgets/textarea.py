from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label

TXTKEYS = {
        K_SPACE: ' ',
        }

for x in xrange(K_EXCLAIM, ord('z')+1):
    TXTKEYS[x] = chr(x)

class TextArea:
    def __init__(self, pos, size, color):
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
        self.text = text
        
    def get_text(self):
        return self.text
    
    def row(self):
        if len(self.text) == 1:
            return 0
        if self.ycursor < len(self.text):
            return self.ycursor
        
    def events(self, event):
        if event.type == KEYDOWN and self.focus:
            return True
        if event.type == KEYUP and self.focus:
            if event.key == K_BACKSPACE:
                # TODO: Add cursor movement
                if len(self.text[self.ycursor]) > 0:
                    self.text[self.ycursor] = self.text[self.ycursor][0:-1]
                    self.xcursor -= 1
            if event.key == K_UP:
                if self.ycursor > 0:
                    self.ycursor -= 1
                    #if len(self.text.[ycursor]) < self.xcursor:
                    self.xcursor = len(self.text[ycursor])
                return True
            if event.key == K_DOWN:
                if self.ycursor < len(self.text):
                    self.ycursor += 1
                    #if len(self.text.[ycursor]) < self.xcursor:
                    self.xcursor = len(self.text[ycursor])
                return True
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                if self.ycursor == len(self.text) -1:
                    self.text.append("")
                    self.ycursor += 1
                    self.xcursor = 0
                    
            # TODO: Handle numlock, there is no way to determine current state
            #       of numlock, thus changing caps when K_NUMLOCK is pressed 
            #       is useless.
            caps = False
            if event.mod & KMOD_SHIFT:
                caps = not caps
            if TXTKEYS.has_key(event.key):
                #line = self.text[ycursor]
                if caps:
                    self.text[self.ycursor] += chr(event.key).upper()
                else:
                    self.text[self.ycursor] += chr(event.key)
                self.xcursor += 1
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
        glPopMatrix()