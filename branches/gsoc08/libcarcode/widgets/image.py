from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

import pygame
from pygame.locals import *

from events import EventDispatcher

class Image:
    def __init__(self, pos, filename):
        self.pos = pos
        img = pygame.image.load(filename)
        img = img.convert_alpha()
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
        self.visible = True
    def __del__(self):
        try:
            glDeleteLists(self.l, 1)
        except:
            pass
    def events(self, event):
        return False
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glCallList(self.l)
        glPopMatrix()