
class ArenaProxy:
    def __init__(self, arena):
        self.__arena__ = arena
        self.on_collision = arena.on_collision
    def add_entity(self, entity):
        self.__arena__.add_entity(entity)
    def get_car(self):
        return self.__arena__.car

class AppProxy:
    def __init__(self, app):
        self.__app__ = app
    def add_key(self, key, action):
        self.__app__.add_key(key, action)