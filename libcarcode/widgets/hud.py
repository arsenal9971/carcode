from OpenGL.GL import *

class HUD:
    def __init__(self):
        self.entities = []
    def events(self, event):
        for entity in self.entities:
            if entity.events(event):
                return True
        return False
    def draw(self):
        glPushMatrix()
        glLoadIdentity()
        for entity in self.entities:
            entity.draw()
        glPopMatrix()
    def add_entity(self, entity):
        entity.parent = self
        self.entities.append(entity)
    def remove_entity(self, entity):
        self.entities.remove(entity)