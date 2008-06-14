# arena.py
import pygame, sys, os
import car
from pygame.locals import *

from OpenGL.GL import *

import helpers
from collision import pyLine

WHITE = (250, 250, 250)
        
class Arena:
    def __init__(self, parent):
        self.parent = parent
        
        self.entities = []
        self.car = None
        self.lines = []
    
    def set_car(self, car):
        self.car = car
        self.parent.add_key(K_s, car.flip_engine)
        self.parent.add_key(K_g, car.flip_gear)
        self.parent.add_key(K_UP, car.accelerate)
        self.parent.add_key(K_LEFT, car.steer_left)
        self.parent.add_key(K_RIGHT, car.steer_right)
        self.parent.add_key(K_DOWN, car.brake)
        self.parent.add_key(K_h, car.honk)
        self.parent.add_key(K_z, car.blinker_left_flip)
        self.parent.add_key(K_c, car.blinker_right_flip)
        self.parent.add_key(K_t, car.flip_tracer)
    
    def add_entity(self, entity):
        self.entities.append(entity)
    
    def update(self):
        for entity in self.entities:
            entity.update()
        self.car.update()
        
    def draw(self, surface):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(400 -self.car.x, 300-self.car.y, 0)
        
        for entity in self.entities:
            entity.draw()
        
        if self.car.moving():
            line = pyLine(self.car.start, self.car.end)
            
            if len(self.lines) == 0:
                self.lines.append(line)
            else:
                last = self.lines[-1]
                if last == line:
                    last += line
                else:
                    self.lines.append(line)
        
        if len(self.lines) > 0:
            glBegin(GL_LINES)
            glColor3f(1.0,0.2,0.3)
            for line in self.lines:
                glVertex2f(line.x1, line.y1)
                glVertex2f(line.x2, line.y2)
            glEnd()
        self.car.draw()
        