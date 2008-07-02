
class VerticalPack:
    def __init__(self, pos, size, padding =10, margin =10):
        self.pos = pos
        self.size = size
        self.entities = []
        self.padding = padding
        self.margin = margin
        self.visible = True
        
    def refresh(self):
        ecount = len(self.entities)
        eW = self.size[0] - (self.margin * 2)
        eH = (self.size[1] - (self.margin * 2) - ((ecount -1) * self.padding)) / ecount
        eX = self.margin + self.pos[0]
        eY = self.margin + self.pos[1]
        for entity in self.entities:
            entity.resize((eW, eH))
            entity.pos = [eX, eY]
            eY += eH + self.padding
            
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
            

class HorizontalPack:
    def __init__(self, pos, size, padding =10, margin =10):
        self.pos = pos
        self.size = size
        self.entities = []
        self.padding = padding
        self.margin = margin
        self.visible = True
        
    def refresh(self):
        ecount = len(self.entities)
        eW = self.size[0] - (self.margin * 2) - ((ecount -1) * self.padding)) / ecount
        eH = (self.size[1] - (self.margin * 2) 
        eX = self.margin + self.pos[0]
        eY = self.margin + self.pos[1]
        for entity in self.entities:
            entity.resize((eW, eH))
            entity.pos = [eX, eY]
            eX += eW + self.padding
            
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