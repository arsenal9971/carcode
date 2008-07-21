import time
from math import cos,  sin,  radians, sqrt

from widgets.events import EventDispatcher

GROUNDED = 0
MOVABLE = 1
ACTOR = 2

def BoxGeometry( x, y, width,  height):
    hw = width/2.0
    hh = height/2.0
    return [(x - hw, y + hh), (x + hw, y + hh), (x + hw, y - hh), (x - hw, y - hh)]
    
class ccEntity:
    """ Base entity class for in simulation objects """
    def __init__(self,  entity_type = 0,   pos = [0, 0],  angle=0.0,  speed=0.0, center = (0,  0)):
        """Entity
        
        @param entity_type entity type, defines entity properties
        @param pos tuple with entity position (x, y)
        @param angle entity angle in degrees
        @param speed entity speed units/sec
        @param center touple with the center point offset of the entity (x, y)
        """
        self.type = entity_type
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.script = None
        self.evt_collision = EventDispatcher()
        self.center = center
        self.collisionable = False
        self.region = []
        self.start = (0, 0)
        self.end = (0, 0)
        
    def get_center(self):
        """ Get the entity center vector in current position 
        
        @returns A tuple with entity center position (x, y)
        """
        if self.center == (0, 0):
            return self.pos 
        return (self.pos[0] + self.center[0],  self.pos[1] + self.center[1] )
        
    def get_region(self):
        """ Get the entity bounding region 
        
        @returns A list of 2d vectors representing the bounding region
        """
        if self.angle == 0.0:
            [(vec[0] + self.pos[0],  vec[1]  + self.pos[1]) for vec in self.region]
            
        rad = radians(-self.angle)
        
        c = cos(rad)
        s = sin(rad)
        
        return [((vec[0] * c) - (vec[1] * s) + self.pos[0],  (vec[0] * s) + (vec[1] * c) + self.pos[1]) for vec in self.region]
    
    def get_axis(self):
        """ Get additional axis to use for collision 
        
        @returns A pair of 2d vectors representing the additional axis
        """
        pass
        
    def attach_script(self,  script):
        """ Attaches a script to entity 
        
        @param script script object
        """
        self.script = script
    
    def deattach_script(self):
        """ Removes script from entity """
        self.script = None
        
    def update(self):
        """ Update entity state and execute script """
        if self.script is not None:
            self.script.update(self)
        
    def draw(self):
        """ Draw entity """
        pass

class PhysicsEngine:
    """ 2D Physics Engine """
    def __init__(self):
        self.entities = []
        self.centities = []
        self.itime = 0.0
        
    def add_entity(self,  entity):
        """ Add an entity to the engine 
        
        @param entity object which implements the ccEntity protocol
        """
        if entity.collisionable:
            self.centities.append(entity)
        self.entities.append(entity)
        
    def update(self):
        """ Update physics state of all entities """
        for entity in self.entities:
            # Grounded objects do not move
            if entity.type == GROUNDED:
                pass
            else:
                # Check entity speed, if not 0 the entity is moving
                if entity.speed != 0.0:
                    rad = radians(entity.angle)
                    
                    dx = entity.speed * cos(rad) 
                    dy = -entity.speed * sin(rad)
                    
                    entity.start = (entity.pos[0], entity.pos[1])
                    entity.pos[0] +=  dx 
                    entity.pos[1] +=  dy 
                    entity.end = (entity.pos[0], entity.pos[1])
                    
                    entity.speed *=  0.985
                    
                    if abs(entity.speed) < 1.0:
                        entity.speed = 0.0
                        
                found = False
                if entity.collisionable:
                    for e in self.centities:
                        if e == entity:
                            found = True
                        elif e.collisionable:
                            ret = self.test_collision(e,  entity)
                            if ret[0]:
                                e.evt_collision.dispatch(e,  ret)
    
    def get_extends_axis(self,  region,  axis):
        """ Get the extends of a region in given axis
        
        @param region list of vectors defining the region 
        @param axis unit vector indicating axis direction
        @returns tuple indictating the minimum and maximum values in given axis
        """
        Amax = 0
        Amin = 0
        t = True
        for vec in region:
            dp = (vec[0] * axis[0]) + (vec[1] * axis[1])
            x = dp * axis[0]  
            y = dp * axis[1]
            d = sqrt((x*x) + (y*y))
            if t:
                Amax = d
                Amin = d
                t = False
            else:
                if d > Amax:
                    Amax = d
                elif d < Amin:
                    Amin = d
        
        return (Amin,  Amax)
            
    def get_extends(self,  region):
        """ Get the extends of a region in x and y axis
        
        @param region list of vectors difining the region 
        @returns pair of tuples with minimum and maximum values in each axis (x, y)
        """
        Xmax = region[0][0]
        Xmin = region[0][0]
        Ymax = region[0][1]
        Ymin = region[0][1]
        
        for vec in region:
            if vec[0] > Xmax:
                Xmax = vec[0]
            elif vec[0] < Xmin:
                Xmin = vec[0]
            if vec[1] > Ymax:
                Ymax = vec[1]
            elif vec[1] < Ymin:
                Ymin = vec[1]
        return ((Xmin,  Xmax),  (Ymin,  Ymax))
        
    def test_collision(self,  e1,  e2):
        """ Test collision between two entities
        
        @param e1 first entity
        @param e2 second entity 
        @return boolean indicating if the entities overlap
        """
        r1 = e1.get_region()
        c1 = e1.get_center()
        
        r2 = e2.get_region()
        c2 = e2.get_center()
        
        Xe1,  Ye1 = self.get_extends(r1)
        Xe2,  Ye2 = self.get_extends(r2)
        
        Xin = False
        if Xe2[0] > Xe1[0]:
            if Xe2[0] > Xe1[1]:
                return (False, False)
            if Xe2[1] <= Xe1[1]:
                Xin = True
        else:
            if Xe2[1] < Xe1[0]:
                return (False, False)
        
        Yin = False
        if Ye2[0] > Ye1[0]:
            if Ye2[0] > Ye1[1]:
                return (False, False)
            if Ye2[1] <=Ye1[1]:
                Yin = True
        else:
            if Ye2[1] < Ye1[0]:
                return (False, False)
                
        d = sqrt((c1[0]*c2[0]) + (c1[1] * c2[1]))
        
        if d == 0:
            return True,  False
            
        x = (c1[0] - c2[0]) / d
        y = (c1[1] - c2[1]) / d
        
        Ze1 = self.get_extends_axis(r1,  (x, y))
        Ze2 = self.get_extends_axis(r2,  (x, y))
        
        Zin = False
        if Ze2[0] > Ze1[0]:
            if Ze2[0] > Ze1[1]:
                return (False, False)
            if Ze2[1] <=Ze1[1]:
                Zin = True
        else:
            if Ze2[1] < Ze1[0]:
                return (False, False)
                
        return True,  Xin and Yin and Zin
