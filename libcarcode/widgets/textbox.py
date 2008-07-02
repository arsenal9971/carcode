from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label

TXTKEYS = {
        K_SPACE: ' '
        }

for x in xrange(ord('a'), ord('z')+1):
    TXTKEYS[x] = chr(x)
    
for x in xrange(ord('0'), ord('9')+1):
    TXTKEYS[x] = chr(x)
    
class TextBox:
    def __init__(self, pos, size, color):
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.text = ""
        self.focus = False
        self.cursor = 0
    def events(self, event):
        if event.type == KEYDOWN and self.focus:
            return True
        if event.type == KEYUP and self.focus:
            if event.key == K_BACKSPACE:
                # TODO: Add cursor movement
                if len(self.text) > 0:
                    self.text = self.text[0:-1]
                    
            # TODO: Handle numlock, there is no way to determine current state
            #       of numlock, thus changing caps when K_NUMLOCK is pressed 
            #       is useless.
            caps = False
            if event.mod & KMOD_SHIFT:
                caps = not caps
            if TXTKEYS.has_key(event.key):
                if caps:
                    self.text += chr(event.key).upper()
                else:
                    self.text += chr(event.key)
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
        glTranslatef(2, 13, 0)
        glColor4f(*COLOR_WHITE)
        glRasterPos3i(0, 0, 0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        if self.focus:
            glTranslatef(0, -13, 0)
            x = 2 + (len(self.text) * 8)
            glRecti(x, 2, x+4, self.size[1]-2)
        glPopMatrix()