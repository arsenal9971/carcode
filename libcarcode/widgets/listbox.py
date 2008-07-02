from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from constants import *
from events import EventDispatcher
from label import Label

class ListBox:
    def __init__(self, pos, size, color):
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.items = []
        if self.size[1] % 14:
            self.size[1] = self.size[1] + 14 - (self.size[1] % 14)
        self.maxrows = self.size[1] / 14
        self.selected = -1
        self.onSelected = EventDispatcher()
        self.visible = True
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            if inX(event.pos[0]) and inY(event.pos[1]):
                y = event.pos[1] - self.pos[1]
                self.selected = (y / 13)
                if self.selected >= len(self.items):
                    self.selected = -1
                else:
                    self.onSelected.dispatch(self)
                return True
        return False
                
    def update(self):
        i = 0
        for item in self.items:
            item.pos[1] = i * 13 + 1
            i += 1
            
    def add_list(self, items):
        for item in items:
            self.add_item(item)
            
    def add_item(self, item):
        self.items.append(Label(item, (0,0), COLOR_WHITE))
        self.update()
        
    def remove_item(self, n):
        if n < len(self.items) and n >= 0:
            item = self.items[n]
            del item
            del self.items[n]
            self.update()
            return True
        return False
    def empty(self):
        self.items = []
        
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
        
        glClear(GL_STENCIL_BUFFER_BIT)
        glEnable(GL_STENCIL_TEST)
        glColorMask(GL_FALSE,GL_FALSE,GL_FALSE,GL_FALSE)
        glStencilOp(GL_REPLACE,GL_REPLACE,GL_REPLACE)
        glStencilFunc(GL_ALWAYS,1,1)
        glRecti(1, 1, self.size[0]-1, self.size[1]-1)
        glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE)
        glStencilFunc(GL_EQUAL,1,1)
        glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
        
        glTranslatef(2, 0, 0)
        i = 0
        for item in self.items:
            if i == self.selected:
                glColor4f(0.5,0,0, 0.5)
                glRecti(0, item.pos[1], self.size[0]-3, item.pos[1]+13)
            if i == self.maxrows:
                break;
            item.draw()
            i += 1
        glDisable(GL_STENCIL_TEST)
        glPopMatrix()