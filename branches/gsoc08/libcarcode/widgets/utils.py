from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

class Dummy:
    pass

colors = [(1.0, 0.0, 0.0, 0.5), (0.0, 1.0, 0.0, 0.8), (0.0, 0.0, 1.0, 0.9)]

class Clipper:
    
    class __Clipper:
        def __init__(self):
            self.regions = []
        
        def __begin(self):
            glClear(GL_STENCIL_BUFFER_BIT)
            glEnable(GL_STENCIL_TEST)
            
            i = 0
            glColorMask(GL_FALSE,GL_FALSE,GL_FALSE,GL_FALSE)
            
            if len(self.regions) == 1:
                reg = self.regions[0]
                glStencilOp(GL_REPLACE,GL_REPLACE,GL_REPLACE)
                glStencilFunc(GL_ALWAYS,1,1)
                glRecti(*reg)
            else:
                reg = self.regions[0]
                glStencilOp(GL_REPLACE,GL_REPLACE,GL_REPLACE)
                glStencilFunc(GL_ALWAYS,1,1)
                glRecti(*reg)
                
                reg = self.regions[1]
                glStencilOp(GL_ZERO,GL_ZERO,GL_ZERO)
                glStencilFunc(GL_EQUAL,1,1)
                glRecti(*reg)
                
                reg = self.regions[0]
                glStencilOp(GL_REPLACE,GL_KEEP,GL_ZERO)
                glStencilFunc(GL_EQUAL,1,1)
                glRecti(*reg)
                
            glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE)
            glStencilFunc(GL_EQUAL,1,1)
            glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
                
        def begin(self, region):
            self.regions.insert(0,region)
            self.__begin()
        
        def end(self):
            self.regions.pop(0)
            if len(self.regions) == 0:
                glDisable(GL_STENCIL_TEST)
            else:
                glDisable(GL_STENCIL_TEST)
                self.__begin()

    __singleton = None
    
    def __init__(self):
        if Clipper.__singleton is None:
            Clipper.__singleton = Clipper.__Clipper()
        self.__singleton = Clipper.__singleton
        #self.__dict__['_Clipper__singleton'] = Clipper.__singleton
    def begin(self, *args):
        self.__singleton.begin(*args)
    def end(self):
        self.__singleton.end()
    
        
def mangle_event(event, obj_pos):
    if event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN:
        nevent = Dummy()
        nevent.type = event.type
        nevent.pos = (event.pos[0] - obj_pos[0], event.pos[1] - obj_pos[1])
    else:
        nevent = event
    return nevent