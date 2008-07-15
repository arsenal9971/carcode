
from constants import *
from widget import Widget

class Pack(Widget):
    """ Widget packing
    Aligns and resizes a list of widgets in a vertical or horizontal fashion.
    """
    def __init__(self, orientation = VERTICAL,  padding = 1, margin = 1,  *args,  **kargs):
        """ Pack
        
        @param orientation packing orientation, VERTICAL by default
        @param padding interwidget padding, 1 by default
        @param margin pack margin, 1 by default
        @param pos tuple with widget position (x, y)
        @param size tuple with widget size (width, height)
        """
        Widget.__init__(self,  *args,  **kargs)
        
        self.entities = []
        self.orientation = orientation
        self.padding = padding
        self.margin = margin
        self.visible = True
            
    # TODO: replace orientation checks with lambdas
    def refresh(self):
        ecount = len(self.entities)
        
        if self.orientation == VERTICAL:
            eW = self.size[0] - (self.margin * 2)
            eH = (self.size[1] - (self.margin * 2) - ((ecount -1) * self.padding)) / ecount
        else:
            eW = (self.size[0] - (self.margin * 2) - ((ecount -1) * self.padding)) / ecount
            eH = self.size[1] - (self.margin * 2) 
            
        eX = self.margin + self.pos[0]
        eY = self.margin + self.pos[1]
        for entity in self.entities:
            entity.set_pos( [eX, eY])
            entity.set_size((eW, eH))
            
            if self.orientation == VERTICAL:
                eY += eH + self.padding
            else:
                eX += eW + self.padding
            
    def set_size(self,  size):
        Widget.set_size(self,  size)
        self.refresh()
        
    def add_entity(self, obj):
        self.entities.append(obj)
        self.refresh()
    
    def events(self, event):
        for entity in self.entities:
            if entity.events(event):
                return True
        return False
        
    def draw(self):
        for entity in self.entities:
            entity.draw()
