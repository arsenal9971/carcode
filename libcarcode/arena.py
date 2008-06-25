# arena.py
import pygame, sys, os
import car
from pygame.locals import *

from OpenGL.GL import *

import helpers

WHITE = (250, 250, 250)
        
class Arena:
    def __init__(self):
        self.entities = []
        self.lines = []
        self.segments = []
    
    def set_car(self, car):
        self.car = car
    
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
        
        self.car.draw()
        