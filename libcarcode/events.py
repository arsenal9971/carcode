from widgets.events import EventDispatcher

scores = [1,  2,  3,  4]

class Goal:
    """ Class describing a certain goal """
    def __init__(self,  desc,  testfunc,  state = 0):
        """Goal
        
        @param desc string describing the objective
        @param testfunc function that test of a given condition returning a boolean
        @param state state number to set if condition is true
        """
        self.desc = desc
        self.testfunc = testfunc
        self.state = 0
        self.onTest = EventDispatcher()
        
    def test(self):
        """ Test goal function 
        
        @returns tuple of boolean and state
        """
        res = self.testfunc()
        
        self.onTest.dispatch(self,  res,  self.state)
        return res, self.state
        
class Score:
    def __init__(self,  name,  scorefunc,  values):
        """ Score
        
        @param name string with the name of the scole
        @param scorefunc function that returns a score in numbers
        @param values list of tuples which contains min and max values range for a given score
        """
        self.name = name
        self.scorefunc = scorefunc
        self.values = values
        
        # Check in which order are the values in the tuple
        vmin,  vmax = self.values[0]
        if vmin > vmax:
            self.inverse = True
        else:
            self.inverse = False
        
    def score(self):
        val = self.scorefunc()
        i = 0
        
        # Create a lambda function to act as an 
        # accesor for the score range tuple in correct order
        if self.inverse:
            vfunc = lambda x: (x[1], x[0])
        else:
            vfunc =  lambda x: (x[0], x[1])
        
        for vrange in self.values:
            vmin,  vmax = vfunc(vrange)
            if val >= vmin and val <= vmax:
                return scores[i]
            i += 1
            if i == 4:
                return 5
