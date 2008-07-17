# arena.py
import pygame, sys, os
import car
from pygame.locals import *

from OpenGL.GL import *

import helpers
from widgets.events import EventDispatcher

WHITE = (250, 250, 250)
        
class Arena:
    def __init__(self,  pe):
        self.entities = []
        self.lines = []
        self.segments = []
        self.on_collision = EventDispatcher()
        self.pe = pe
    
    def set_car(self, car):
        self.car = car
        self.pe.add_entity(car)
    
    def add_entity(self, entity):
        self.entities.append(entity)
        self.pe.add_entity(entity)
    
    def update(self):
        for entity in self.entities:
            entity.update()
        self.car.update()
        #for entity in self.entities:
          #  if entity.collisionable:
            #    if self.car.bbox.collide(entity.bbox):
              #      self.on_collision.dispatch(entity)
        
    def draw(self, surface):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(400 -self.car.pos[0], 300-self.car.pos[1], 0)
        
        for entity in self.entities:
            entity.draw()
        
        self.car.draw()
        
