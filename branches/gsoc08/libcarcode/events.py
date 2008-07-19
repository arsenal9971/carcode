class AND:
    """ Conditional AND for events """
    def __init__(self,  con1,  st1,  con2,  st2):
        """AND
        
        @param con1 function to evaluate condition, must return boolean
        @param st1 state to set if con1 evaluates True
        @param con2 function to evaluate condition, must return boolean
        @param st2 state to set if con2 evaluates True
        """
        self.con1 = con1,  st1
        self.con2 = con2,  st2
        
    def __call__(self):
        func,  val = self.con1
        st = 0
        
        if func():
            st = val
        else:
            return False,  st 
            
        func,  val = self.con1
        if func():
            st = val
        else:
            return False,  st 
        
        return True,  st

class OR:
    """ Conditional OR for events """
    def __init__(self,  con1,  st1,  con2,  st2):
        """AND
        
        @param con1 function to evaluate condition, must return boolean
        @param st1 state to set if con1 evaluates True
        @param con2 function to evaluate condition, must return boolean
        @param st2 state to set if con2 evaluates True
        """
        self.con1 = con1,  st1
        self.con2 = con2,  st2
        
    def __call__(self):
        rt = False
        
        func,  val = self.con1
        st = 0
        
        if func():
            st = val
            rt = True
            
        func,  val = self.con1
        if func():
            st = val
            rt = True
        
        return rt,  st

scores = ['C',  'B',  'A',  'S']

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
        
    def score(self):
        val = self.scorefunc()
        i = 0
        
        for vmin,  vmax in self.values:
            if val >= vmin and val <= vmax:
                return scores[i]
            i += 1
            if i == 4:
                return 'Out rank'
