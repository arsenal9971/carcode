
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
            eSize = self.size[1] - (self.margin * 2)
        else:
            eSize = self.size[0] - (self.margin * 2)
        
        ecount = 0
        for entity,  expand in self.entities:
            if expand:
                ecount += 1
            else:
                w,  h = entity.get_size()
                if self.orientation == VERTICAL:
                    eSize -= h
                else:
                    eSize -= w
        
        
        if self.orientation == VERTICAL:
            eW = self.size[0] - (self.margin * 2)
            #eH = (self.size[1] - (self.margin * 2) - ((ecount -1) * self.padding)) / ecount
            if ecount:
                eH = (eSize - ((len(self.entities)-1) * self.padding)) / ecount
            else:
                eH = 0
        else:
            #eW = (self.size[0] - (self.margin * 2) - ((ecount -1) * self.padding)) / ecount
            if ecount:
                eW = (eSize - ((len(self.entities)-1) * self.padding)) / ecount
            else:
                eW = 0
            eH = self.size[1] - (self.margin * 2) 
            
        eX = self.margin + self.pos[0]
        eY = self.margin + self.pos[1]
        for entity,  expand in self.entities:
            entity.set_pos( [eX, eY])
            
            if expand:
                entity.set_size((eW, eH))
                
                if self.orientation == VERTICAL:
                    eY += eH + self.padding
                else:
                    eX += eW + self.padding
            else:
                w,  h = entity.get_size()
                if self.orientation == VERTICAL:
                    entity.set_size((eW, h))
                    eY += h + self.padding
                else:
                    entity.set_size((w, eH))
                    eX += w + self.padding
            
    def set_size(self,  size):
        Widget.set_size(self,  size)
        self.refresh()
        
    def add_entity(self, obj,  expand = True):
        self.entities.append((obj,  expand))
        self.refresh()
    
    def events(self, event):
        for entity,  expand in self.entities:
            if entity.events(event):
                return True
        return False
        
    def draw(self):
        for entity,  expand in self.entities:
            entity.draw()
