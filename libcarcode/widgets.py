from math import atan, sin, cos, radians, sqrt
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from pygame.locals import *
from events import EventDispatcher
import helpers

COLOR_WHITE = (1.0,1.0,1.0,1.0)

TXTKEYS = {
        K_SPACE: ' '
        }

for x in xrange(ord('a'), ord('z')+1):
    TXTKEYS[x] = chr(x)
    
for x in xrange(ord('0'), ord('9')+1):
    TXTKEYS[x] = chr(x)

class Dummy:
    pass
        
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
        entity.parent = self
        self.entities.append(entity)
    def remove_entity(self, entity):
        self.entities.remove(entity)

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
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRecti(0, 0, self.size[0], self.size[1])
        
        if self.focus:
            glColor3ub(0, 0, 200)
        else:
            glColor3ub(100, 100, 100)
        glRecti(0, 0, self.size[0], 15)
        
        self.label.draw()
        
        glTranslatef(2, 17, 0)
        for entity in self.entities:
            entity.draw()
        glPopMatrix()
    def events(self, event):
        if event.type == MOUSEBUTTONUP and not self.modal:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.focus = True
            else:
                self.focus = False
                return False
        if self.focus:
            if event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
                nevent = Dummy()
                nevent.type = event.type
                nevent.pos = (event.pos[0] - self.pos[0] - 2, event.pos[1] - self.pos[1] - 17)
            else:
                nevent = event
            for entity in self.entities:
                if entity.events(nevent):
                    return True
        if self.modal:
            return True
        return False

class Dialog(Window):
    def __init__(self, label, callback):
        height = 80
        width = 180
        label = Label(label, (0, 17), COLOR_WHITE)
        self.btnYes = Button("Yes", (15, 35), (60, 20), (0.2,0.2,0.2))
        self.btnNo = Button("No", (95, 35), (60, 20), (0.2,0.2,0.2))
        self.btnYes.onClick.subscribe(self.answared)
        self.btnNo.onClick.subscribe(self.answared)
        
        self.callback = callback
        Window.__init__(self, "Dialog", (270, 220), (width, height), (0.5,0.5,0.5,0.5))
        self.modal = True
        self.add_entity(label)
        self.add_entity(self.btnYes)
        self.add_entity(self.btnNo)
            
    def answared(self, button):
        if button == self.btnYes:
            self.callback("Yes")
        else:
            self.callback("No")
        self.parent.remove_entity(self)
            
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
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRasterPos3i(0, 0, 0)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        glPopMatrix()

class Button:
    def __init__(self, text, pos, size, color):
        ly = (size[1] / 2) + 4
        lx = (size[0] - (len(text) * 8)) / 2
        self.label = Label(text, (lx, ly), COLOR_WHITE)
        self.color = color
        self.pos = pos
        self.size = size
        self.onClick = EventDispatcher()
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            if inX(event.pos[0]) and inY(event.pos[1]):
                self.onClick.dispatch(self)
                return True
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        if len(self.color) == 3:
            glColor3f(*self.color)
        else:
            glColor4f(*self.color)
        glRecti(0, 0, self.size[0], self.size[1])
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
            glRecti(x, 2, x+4, self.size[0]-2)
        glPopMatrix()
        
class Image:
    def __init__(self, pos, filename):
        self.pos = pos
        img, rect = helpers.load_image(filename)
        w, h = img.get_size()
        self.size = (w, h)
        self.l = glGenLists(1)
        glNewList(self.l, GL_COMPILE)
        glBegin(GL_POINTS)
        for x in xrange(w):
            for y in xrange(h):
                d = img.get_at((x, y))
                glColor4ub(*d)
                glVertex2i(x, y)
        glEnd()
        glEndList()
        del img
        del rect
    def __del__(self):
        glDeleteLists(self.l, 1)
    def events(self, event):
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glCallList(self.l)
        glPopMatrix()

class List:
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
    def events(self, event):
        if event.type == MOUSEBUTTONUP:
            inX = lambda x: x >= self.pos[0] and x <= self.pos[0]+self.size[0]
            inY = lambda y: y >= self.pos[1] and y <= self.pos[1]+self.size[1]
            if inX(event.pos[0]) and inY(event.pos[1]):
                y = event.pos[1] - self.pos[1]
                self.selected = (y / 13)
                if self.selected > len(self.items):
                    self.selected = -1
                else:
                    self.onSelected.dispatch(self)
                print "Selected ", self.selected
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
        
        glTranslatef(2, 13, 0)
        i = 0
        for item in self.items:
            if i == self.selected:
                glColor4f(0.5,0,0, 0.5)
                glRecti(0, item.pos[1]-11, self.size[0]-3, item.pos[1]+1)
            if i == self.maxrows:
                break;
            item.draw()
            i += 1
        glDisable(GL_STENCIL_TEST)
        glPopMatrix()