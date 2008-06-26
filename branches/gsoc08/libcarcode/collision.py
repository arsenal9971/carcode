from OpenGL.GL import *
from math import sin, cos, degrees, radians, sqrt, pi, atan

class pyLine:
    def __init__(self, *args):
        def arg4(x1, y1, x2, y2):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
        def arg2(pos1, pos2):
            self.x1 = pos1[0]
            self.y1 = pos1[1]
            self.x2 = pos2[0]
            self.y2 = pos2[1]
        
        if len(args) == 2:
            arg2(*args)
        else:
            arg4(*args)
            
        if self.x2 != self.x1:
            self.m = round((self.y2-self.y1) / (self.x2-self.x1), 2)
        else:
            if self.y1 > self.y2:
                self.m = -65536
            else:
                self.m = 65536
            
    def crossect(self, line):
        pass
    def __eq__(self, line):
        return self.m == line.m
    def __add__(self, line):
        if self.m == line.m:
            self.x2 = line.x2
            self.y2 = line.y2
    def draw(self):
        glBegin(GL_LINES)
        glColor3f(0.5, 0.1, 0.3)
        glVertex2f(self.x1, self.y1)
        glVertex2f(self.x2, self.y2)
        glEnd()
        
    def __repr__(self):
        return "pyLine(%i, %i, %i, %i)" % (self.x1, self.y1, self.x2, self.y2)
    
class BoundingRegion:
    def __init__(self, offsetx, offsety, angle=0.0):
        self.x = offsetx
        self.y = offsety
        self.angle = angle
        self.points = []
    
    def update(self):
        rad = radians(-self.angle)
        
        c = cos(rad)
        s = sin(rad)
            
        x = (self.points[0][0] * c) - (self.points[0][1] * s)
        y = (self.points[0][0] * s) + (self.points[0][1] * c)
        
        self.xh = x
        self.xl = x
        self.yh = y
        self.yl = y
        
        for point in self.points:
            x = (point[0] * c) - (point[1] * s)
            y = (point[0] * s) + (point[1] * c)
            
            if x > self.xh:
                self.xh = x
            if x < self.xl:
                self.xl = x
            if y > self.yh:
                self.yh = y
            if y < self.yl:
                self.yl = y
            
    def get_sa(self):
        return ((self.xl + self.x, self.xh + self.x), (self.yl + self.y, self.yh + self.y))
            
    def draw(self):
        rad = radians(-self.angle)
        
        c = cos(rad)
        s = sin(rad)
        
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0,1.0,1.0)
        for point in self.points:
            x = (point[0] * c) - (point[1] * s)
            y = (point[0] * s) + (point[1] * c)
            glVertex2f(x+self.x,y+self.y)
        x = (self.points[0][0] * c) - (self.points[0][1] * s)
        y = (self.points[0][0] * s) + (self.points[0][1] * c)
        glVertex2f(x+self.x,y+self.y)
        glEnd()
        
    def collide(self, region):
        sx, sy = self.get_sa()
        rx, ry = region.get_sa()
        if rx[1] < sx[0] or rx[0] > sx[1]:
            return False
        if ry[1] < sy[0] or ry[0] > sy[1]:
            return False
        return True
    
    def contains(self, region):
        sx, sy = self.get_sa()
        rx, ry = region.get_sa()
        if rx[0] < sx[0] or rx[0] > sx[1]:
            return False
        if rx[1] < sx[0] or rx[1] > sx[1]:
            return False
        if ry[0] < sy[0] or ry[0] > sy[1]:
            return False
        if ry[1] < sy[0] or ry[1] > sy[1]:
            return False
        return True
    def inVector(self, v):
        pass
    def inLine(self, v1, v2):
        pass

class BoudingCircle(BoundingRegion):
    def __init__(x, y, radius):
        BoudingRegion.__init__(self, x, y)
        self.radius = radius
    def inVector(self, v):
        d = sqrt((v[0] * self.x) + (v[1] * self.y))
        if self.radius > d:
            return True
        return False
    
class BoundingBox(BoundingRegion):
    def __init__(self, x, y, height, width):
        BoundingRegion.__init__(self, 0, 0)
        hw = width/2.0
        hh = height/2.0
        self.points = [(x - hw, y + hh), (x + hw, y + hh), (x + hw, y - hh), (x - hw, y - hh)]
        self.height = height
        self.width = width
        self.update()
        
    def inVector(self, v):
        if v[0] >= self.x and vx <= (self.x + width):
            inX = True
        else:
            inX = False
        
        if v[1] >= self.y and vx <= (self.y + height):
            inY = True
        else:
            inY = False
        
        return inX and inY
        
    def inLine(self, v1, v2):
        pass