from math import atan, sin, cos, radians, sqrt
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from pygame.locals import *
from events import EventDispatcher

COLOR_WHITE = (255,255,255)

class HUD:
    def __init__(self):
        self.entities = []
    def events(self, event):
        for entity in self.entities:
            if entity.events(event):
                return True
        return False
    def draw(self):
        glPushMatrix()
        glLoadIdentity()
        for entity in self.entities:
            entity.draw()
        glPopMatrix()
    def add_entity(self, entity):
        self.entities.append(entity)
        
class Label:
    def __init__(self, text, pos, color):
        self.text = text
        self.pos = list(pos)
        self.color = color
    def events(self, event):
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glColor3ub(*self.color)
        glRasterPos3i(0, 0, 0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        glPopMatrix()

class Button:
    def __init__(self, text, pos, size, color):
        ly = (size[0] / 2) + 4
        lx = (size[1] - (len(text) * 8)) / 2
        self.label = Label(text, (lx, ly), COLOR_WHITE)
        self.color = color
        self.pos = pos
        self.size = size
        self.onClick = EventDispatcher()
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[1]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[0]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.onClick.dispatch(self)
                return True
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glColor3ub(*self.color)
        glRecti(0, 0, self.size[1], self.size[0])
        self.label.draw()
        glPopMatrix()

class List:
    def __init__(self, pos, size, color):
        self.pos = list(pos)
        self.size = list(size)
        self.color = color
        self.items = []
        if self.size[0] % 14:
            self.size[0] = self.size[0] + 14 - (self.size[0] % 14)
        self.selected = -1
        self.onSelected = EventDispatcher()
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[1]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[0]
            if inX(event.pos[0]) and inY(event.pos[1]):
                y = event.pos[1] - self.pos[1]
                self.selected = (y / 13)
                if self.selected > len(self.items):
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
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glColor3ub(*self.color)
        glRecti(0, 0, self.size[1], self.size[0])
        glColor3ub(0,0,0)
        glRecti(1, 1, self.size[1]-1, self.size[0]-1)
        glTranslatef(2, 13, 0)
        i = 0
        for item in self.items:
            if i == self.selected:
                glColor3ub(100,0,0)
                glRecti(0, item.pos[1]-11, self.size[1]-2, item.pos[1]+1)
            item.draw()
            i += 1
        glPopMatrix()