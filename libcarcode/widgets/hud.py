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
        try: 
            if entity.centered:
                x = (self.size[0] / 2) - (entity.size[0] / 2)
                y = (self.size[1] / 2) - (entity.size[1] / 2)
                entity.pos = [x, y]
        except:
            pass
        self.entities.append(entity)
    def remove_entity(self, entity):
        self.entities.remove(entity)