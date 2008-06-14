from OpenGL.GL import *

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
    def __init__(offsetx, offsety):
        self.x = offsetx
        self.y = offsety
    def inVector(self, v):
        pass
    def inLine(self, v1, v2):
        pass

class BoundingBox(BoundingRegion):
    def __init__(self, x, y, height, width):
        BoudingRegion.__init__(self, x, y)
        self.height = height
        self.width = width
        
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