
class ArenaProxy:
    def __init__(self, arena):
        self.__arena__ = arena
        self.on_collision = arena.on_collision
    def add_entity(self, entity):
        self.__arena__.add_entity(entity)
    def get_car(self):
        return self.__arena__.car

class AppProxy:
    """ Carcode application interface for scripts """
    def __init__(self, app):
        self.__app__ = app
        
    def add_key(self, key, action):
        """ Add a key binding
        
        @param key pygame key code
        @param action function to call when key is pressed
        """
        self.__app__.add_key(key, action)
        
    def quit(self):
        """ Send the quit signal to the application """
        self.__app__.quit()
        
    def set_goals(self,  goals):
        """ Set the level goals 
        
        @param goals list of Goal objects
        """
        self.__app__.goals = goals
        self.__app__.goalWindow.set_goals(goals)
        
    def set_scores(self,  scores):
        """ Set level score criteria 
        
        @param scores list of Score objects
        """
        self.__app__.scoreboard = scores
        
    def get_state(self):
        """ Get current state as defined by goals
        
        @returns state return code from last accomplished goal
        """
        return self.__app__.state
        
    def get_game_time(self):
        """ Get the time the simulation has been on 
        
        @returns time in seconds that the simulation has been on.
        """
        return self.__app__.game_time
