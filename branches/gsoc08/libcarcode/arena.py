# arena.py
import pygame, sys, os
import car
from pygame.locals import *

from OpenGL.GL import *

import helpers

WHITE = (250, 250, 250)

class Path:
    def __init__(self):
        self.x = 500
        self.y = 200
    def update(self):
        pass
    def draw(self):
        glColor3f(0.4, 0.4, 0.4)
        glRecti(self.x, self.y, self.x + 300, self.y + 100)
        glColor3f(1.0, 1.0, 1.0)
        glRecti(self.x, self.y+2, self.x + 300, self.y + 4)
        glRecti(self.x, self.y+96, self.x + 300, self.y + 98)
        
class Arena:
    def __init__(self, parent):
        self.parent = parent
        
        self.entities = [Path()]
        self.car = None
    
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
        glTranslatef(-self.car.x, -self.car.y, 0)
        
        for entity in self.entities:
            entity.draw()
        #self.surface.blit(self.trace, self.trace.get_rect())
        #c1 = list(self.car.rect.topleft)
        self.car.draw()
        #c2 = list(self.car.rect.topleft)
        #dx = c2[0] - c1[0]
        #dy = c2[1] - c1[1]
        #if (dx < 100 and dx > -100) and (dy < 100 and dy > -100):
        #    if self.car.tracer_down:
        #        pygame.draw.line(self.trace, self.car.tracer_color, c1, c2, 2)
        #surface.blit(self.surface, self.surface.get_rect())
