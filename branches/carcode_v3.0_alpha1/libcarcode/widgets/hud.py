from OpenGL.GL import *

class HUD:
    """Head up display
    This class controls event passing and rendering of widgets added to it.
    """
    def __init__(self, size):
        """HUD
        
            @param size tuple with screen size (width, height)
        """
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
        """Adds a widget to the HUD object which will manage it
        
            @param entity object implementing the widget protocol
        """
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
        """Removes a widget from the HUD list"""
        self.entities.remove(entity)
