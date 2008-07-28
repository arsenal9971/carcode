from math import atan, sin, cos, radians, sqrt
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from collision import BoundingBox
from physics import ccEntity,  BoxGeometry

DEBUG = False

def distance(p1,  p2):
    x,  y = p2[0] - p1[0],   p2[1] - p1[1]
    
    d = sqrt(x*x + y*y)
    return d

def unitv(p1,  p2):
    x,  y = p2[0] - p1[0],   p2[1] - p1[1]
    
    d = sqrt(x*x + y*y)
    
    if d == 0:
        return 0, 0
    
    return x/d,  y/d
    
class Box(ccEntity):
    def __init__(self, pos, size, color, col=False):
        """Box
        
        @param pos tuple with box position (x, y)
        @param size tuple with box size (width, height)
        @param color tuple with box color (r, g, b, a)
        @param col if object should detect collisions 
        """
        ccEntity.__init__(self,  pos = pos)
        self.x = pos[0]
        self.y = pos[1]
        self.height = size[1] 
        self.width = size[0] 
        self.color = color
        self.center = (size[0]/2.0,  size[1]/2.0)
        self.collisionable = col
        self.region = BoxGeometry(size[0]/2.0,  size[1]/2.0,  self.width,  self.height)
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0.0)
        if len(self.color) > 3:
            glColor4f(*self.color)
        else:
            glColor3f(*self.color)
        glRecti(0, 0, self.width, self.height)
        glPopMatrix()

class Text:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.collisionable = False
        
    def update(self):
        pass
    
    def draw(self):
        glPushMatrix()
        glRasterPos2i(self.x, self.y)
        glColor3ub(*self.color)
        for c in self.text:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        glPopMatrix()
    
class Road(ccEntity):
    def __init__(self, road_points):
        ccEntity.__init__(self)
        self.road_points = road_points
        
    # TODO: handle multipoint roads, only 2 points are supported
    # TODO: Optimize, preprocess at init and use call lists
    def draw(self):
        width = glGetIntegerv(GL_LINE_WIDTH)
        for i in xrange(len(self.road_points) - 1):
            p1 = self.road_points[i]
            p2 = self.road_points[i+1]
            
            d = distance(p1,  p2)
            
            lc = int(d / 60)
            
            ux,  uy = unitv(p1,  p2)
            
            rx,  ry = -uy * 50,  ux * 50
            lx,  ly = uy * 50,  -ux * 50
            
            glBegin(GL_QUADS)
            glColor3f(0.3, 0.3, 0.3)
            glVertex2f(p1[0]+lx, p1[1]+ly)
            glVertex2f(p2[0]+lx, p2[1]+ly)
            glVertex2f(p2[0]+rx, p2[1]+ry)
            glVertex2f(p1[0]+rx, p1[1]+ry)
            glEnd()
            
            
            cx,  cy = p1
            glLineWidth(3)
            for j in xrange(lc):
                glBegin(GL_LINES)
                glColor3f(1.0, 1.0, 1.0)
                glVertex2f(cx,  cy)
                
                cx += ux * 45
                cy += uy * 45
                
                glVertex2f(cx,  cy)
                
                cx += ux * 15
                cy += uy * 15
                glEnd()
            glLineWidth(width)
