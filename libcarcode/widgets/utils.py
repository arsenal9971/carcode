from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

class Dummy:
    pass

colors = [(1.0, 0.0, 0.0, 0.5), (0.0, 1.0, 0.0, 0.8), (0.0, 0.0, 1.0, 0.9)]

class Clipper:
    
    class __Clipper2:
        def __init__(self):
            self.regions = 0
                
        def begin(self, region):
            if self.regions == 0:
                glClear(GL_STENCIL_BUFFER_BIT)
                glEnable(GL_STENCIL_TEST)
                op = (GL_REPLACE,GL_REPLACE,GL_REPLACE)
                func = (GL_ALWAYS,1,1)
            else:
                op = (GL_KEEP, GL_KEEP,GL_INCR)
                func = (GL_EQUAL,1,1)
            
            glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
            
            glStencilOp(*op)
            glStencilFunc(*func)
            glRecti(*region)
            
            self.regions += 1
            
            glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE)
            glStencilFunc(GL_EQUAL,self.regions, self.regions)
            glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)
        
        def end(self):
            self.regions -= 1
            if self.regions == 0:
                glDisable(GL_STENCIL_TEST)
            else:
                glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE)
                glStencilFunc(GL_EQUAL,self.regions, self.regions)
                glStencilOp(GL_KEEP,GL_KEEP,GL_KEEP)

    __singleton = None
    
    def __init__(self):
        if Clipper.__singleton is None:
            Clipper.__singleton = Clipper.__Clipper2()
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