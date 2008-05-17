
class ArenaProxy:
    def __init__(self, arena):
        self.arena = arena
    def add_entity(self, entity):
        self.arena.add_entity(entity)

class AppProxy:
    def __init__(self, app):
        self.__app__ = app
    def add_key(self, key, action):
        self.__app__.add_key(key, action)