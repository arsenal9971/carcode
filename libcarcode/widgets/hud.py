from OpenGL.GL import *

class HUD:
    def __init__(self, size):
        self.entities = []
        self.size = size
    def events(self, event):
        for entity in reversed(self.entities):
            if entity.visible:
                if entity.events(event):
                    return True
        return False
    def draw(self):
        glPushMatrix()
        glLoadIdentity()
        for entity in self.entities:
            if entity.visible:
                entity.draw()
        glPopMatrix()
    def add_entity(self, entity):
        entity.parent = self
        self.entities.append(entity)
    def remove_entity(self, entity):
        self.entities.remove(entity)