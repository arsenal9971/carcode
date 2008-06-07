from math import sin, cos, radians, sqrt
from OpenGL.GL import *

class Sensor:
    ''' Sensor class
    Reads pixel data from backbuffer in a given position,
    pixel is a touple containing (R,G,B) values.
    '''
    def __init__(self, x, y):
        self.offx = x
        self.offy = y
        self.pixel = (0,0,0)
        if x == 0 and y == 0:
            self.angle = 0
            self.length = 0
        else:
            if x == 0:
                self.angle = radians(90)
                self.length = y
            else:
                self.angle = float(y)/x
                self.length = sqrt((x*x) + (y*y))
        
    def update(self, angle):
        rad = radians(angle) + self.angle
        x = 400 + int(self.length * cos(rad))
        y = 300 - int(self.length * -sin(rad))
        glReadBuffer(GL_BACK)
        pixels = glReadPixelsb(x, y, 1, 1, GL_RGB)
        self.pixel = pixels[0][0]
    
    def read_data(self):
        return self.pixel
    
    def draw(self, angle):
        rad = radians(angle) + self.angle
        x = self.length * cos(rad)
        y = self.length * -sin(rad)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(400 + x, 300 + y, 0.0)
        glColor3ub(255,255,255)
        glRecti(-2, -2, 2, 2)
        glPopMatrix()

class ColorSensor(Sensor):
    ''' ColorSensor class
    Looks for a specific color in the backbuffer,
    pixel is True of the color is found, False otherwise.
    '''
    def __init__(self, x, y, color):
        Sensor.__init__(self, x, y)
        self.color = color
    
    def update(self, angle):
        Sensor.update(self, angle)
        # Compare both color tuples by xor'ing each value
        # then sum the results.
        r = reduce(lambda x,y: x+y, [a ^ b for a, b in zip(self.pixel, self.color)])
        
        #if the sum result is > 0 then the colors are different
        if r:
            self.pixel = False
        else:
            self.pixel = True