
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
    def quit(self):
        self.__app__.quit()
    def set_conditions(self,  condition):
        self.__app__.condition = condition
        self.__app__.goalWindow.set_goals(condition)
        
    def get_state(self):
        return self.__app__.state
    def add_score(self,  score):
        self.__app__.scoreboard.append(score)
    def get_game_time(self):
        return self.__app__.game_time
