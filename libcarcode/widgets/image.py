from OpenGL.GL import *

import pygame
from pygame.locals import *

from events import EventDispatcher
from widget import Widget

class Image(Widget):
    """ Image widget """
    def __init__(self, filename,  *args,  **kargs):
        """ Image
        @param filename filename of the image
        """
        Widget.__init__(self,  *args,  **kargs)
        
        # Raw image data from pygame
        img = pygame.image.load(filename)
        img = img.convert_alpha()
        
        w, h = img.get_size()
        self.size = (w, h)
        
        # Generate new compiled list
        self.imgList = glGenLists(1)
        
        # Begin adding points to the compiled list
        glNewList(self.imgList, GL_COMPILE)
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
            glDeleteLists(self.imgList, 1)
        except:
            pass
        
    def set_size(self,  size):
        # Image widgets cannot be resized
        pass
        
    def events(self, event):
        return False
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glCallList(self.imgList)
        glPopMatrix()
