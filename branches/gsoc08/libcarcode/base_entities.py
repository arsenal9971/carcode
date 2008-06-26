from math import atan, sin, cos, radians, sqrt
from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from collision import BoundingBox

DEBUG = False

class Box:
    def __init__(self, x, y, height, width, color, col=False):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        
        self.collisionable = col
        self.bbox = BoundingBox(x + (width/2) , y + (height/2), height, width)
        self.bbox.update()
        
    def update(self):
        pass
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.0)
        glColor3ub(*self.color)
        glRecti(0, 0, self.width, self.height)
        glPopMatrix()
        if DEBUG:
            self.bbox.draw()

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
    
class Road:
    def __init__(self, road_points, width=50):
        self.road_points = road_points
        self.width = width
        
    def update(self):
        # Dummy update function
        pass
    
    def draw(self):
        for i in xrange(len(self.road_points) - 1):
            p1 = self.road_points[i]
            p2 = self.road_points[i+1]
            
            # Check if angle could be 90
            # evading the ZeroDivision exception
            if p2[0] == p1[0]:
                if p2[1] < p1[1]:
                    angle = radians(-90)
                else:
                    angle = radians(90)
            else:
                m = (p2[1] - p1[1]) / (p2[0] - p1[0])
                angle = atan(m)
            
            # Get the perpendicular angle to Line P1-P2 angle
            angle = angle + radians(90)
            
            # Get distance between vectors
            vlen = sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))
            
            if i > 0:
                # Calculate vectors to just extend past line
                l1 = l2
                l4 = l3
                l2 = (l2[0] + (vlen * cos(angle)), l2[1] + (vlen * -sin(angle)))
                l3 = (l3[0] + (vlen * cos(angle)), l3[1] + (vlen * -sin(angle)))
            else:
                # It is the first line, calculate al vectors
                l1 = (p1[0] + (-self.width * cos(angle)), p1[1] + (self.width * -sin(angle)))
                l4 = (p1[0] - (-self.width * cos(angle)), p1[1] - (self.width * -sin(angle)))
            
                l2 = (p2[0] + (-self.width * cos(angle)), p2[1] + (self.width * -sin(angle)))
                l3 = (p2[0] - (-self.width * cos(angle)), p2[1] - (self.width * -sin(angle)))
            
            # Set color (greyish)
            glColor3f(0.4, 0.4, 0.4)
            
            # Draw quads
            glBegin(GL_QUADS)
            glVertex2f(*l1)
            glVertex2f(*l2)
            glVertex2f(*l3)
            glVertex2f(*l4)
            glEnd()