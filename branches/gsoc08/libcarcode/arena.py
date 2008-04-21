# arena.py
import pygame, sys, os
import car
from pygame.locals import *

import helpers

DEBUG_EVENTS = False
DEBUG_ARENA = True

WHITE = (250, 250, 250)

class Arena:
    def __init__(self, parent, width, height):
        self.parent = parent
        self.surface = pygame.Surface((width, height))
        self.surface.fill((0,0,0))
        
        self.trace = pygame.Surface((width, height))
        self.trace.fill((32,32,32))
        self.trace.set_colorkey((32,32,32))
        
        self.entities = []
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
    
    def add_entity(self, entity):
        self.entities.append(entity)
        
    def draw(self, surface):
        self.surface.fill((0,0,0))
        for entity in self.entities:
            entity.draw(self.surface)
        self.surface.blit(self.trace, self.trace.get_rect())
        c1 = self.car.rect.center
        self.car.draw(self.surface)
        c2 = self.car.rect.center
        dx = c2[0] - c1[0]
        dy = c2[1] - c1[1]
        if (dx < 100 and dx > -100) and (dy < 100 and dy > -100):
            pygame.draw.line(self.trace, (0, 0, 255), c1, c2, 2)
        surface.blit(self.surface, self.surface.get_rect())
