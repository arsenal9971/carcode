from math import atan, sin, cos, radians, sqrt
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from pygame.locals import *
from events import EventDispatcher

COLOR_WHITE = (255,255,255)
TXTKEYS = {
        K_SPACE: ' '
        }

for x in xrange(ord('a'), ord('z')+1):
    TXTKEYS[x] = chr(x)
    
for x in xrange(ord('0'), ord('9')+1):
    TXTKEYS[x] = chr(x)
        
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

class Window:
    def __init__(self, label, pos, size, color, modal = False):
        self.label = Label(label, (4,12), COLOR_WHITE)
        self.pos = pos
        self.size = size
        self.color = color
        self.entities = []
        self.focus = True
        self.modal = modal
        
    def add_entity(self, entity):
        self.entities.append(entity)
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glColor3ub(*self.color)
        glRecti(0, 0, self.size[1], self.size[0])
        
        if self.focus:
            glColor3ub(0, 0, 200)
        else:
            glColor3ub(100, 100, 100)
        glRecti(0, 0, self.size[1], 15)
        
        self.label.draw()
        
        glTranslatef(2, 17, 0)
        for entity in self.entities:
            entity.draw()
        glPopMatrix()
    def events(self, event):
        if event.type == MOUSEBUTTONUP and not self.modal:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[1]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[0]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.focus = True
            else:
                self.focus = False
                return False
        if self.focus:
            for entity in self.entities:
                if entity.events(event):
                    return True
        if self.modal:
            return True
        return False
        
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

class Textbox:
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
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[1]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[0]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.focus = True
                return True
            else:
                self.focus = False
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glColor3ub(*self.color)
        glRecti(0, 0, self.size[1], self.size[0])
        glColor3ub(0,0,0)
        glRecti(1, 1, self.size[1]-1, self.size[0]-1)
        glTranslatef(2, 13, 0)
        glColor3ub(*COLOR_WHITE)
        glRasterPos3i(0, 0, 0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        if self.focus:
            glTranslatef(0, -13, 0)
            x = 2 + (len(self.text) * 8)
            glRecti(x, 2, x+4, self.size[0]-2)
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