
class Script:
    ''' Script - Dinamycally load python code from files
    '''
    def __init__(self, filename, mappings = {}, autoload = False):
        self.filename = filename
        self.script = mappings
        self.functions = {}
        if autoload:
            self.load_script()
            
    def load_script(self):
        fd = open(self.filename, 'r')
        exec (fd, self.script)
        fd.close()
        for k in self.script.keys():
            item = self.script[k]
            if '__call__' in dir(item):
                self.functions[k] = item
    
    def get(self, attrib):
        ''' 
            Get an object from the script environment
        '''
        return self.script[attrib]
    
    def set(self, attrib, value):
        ''' 
            Set an attribute or value in the script environment
        '''
        self.script[attrib] = value
    
    def call(self, func_name, *args, **kargs):
        '''
            Call a function from the environment with given arguments
        '''
        if self.functions.has_key(func_name):
            func = self.functions[func_name]
            return func(*args, **kargs)