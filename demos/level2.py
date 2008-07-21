# Cet the car object
car = Arena.get_car()

class LevelScript:
    def __init__(self):
        # Create the road using boxes
        self.road1 = Box((0, 0),  (500,  30), (0.4,0.4,0.4),  True)
        self.road2 = Box((500, 0),  (30,  500), (0.4,0.4,0.4),  True)
        self.road3 = Box((0, 470),  (500,  30), (0.4,0.4,0.4),  True)
        self.road4 = Box((0, 0),  (30,  500), (0.4,0.4,0.4),  True)
        
        # Subscribe callback onVisit to collision event for all boxes
        self.road1.evt_collision.subscribe(self.onVisit)
        self.road2.evt_collision.subscribe(self.onVisit)
        self.road3.evt_collision.subscribe(self.onVisit)
        self.road4.evt_collision.subscribe(self.onVisit)
        
        # Create a finish line with a box
        finish = Box((0,  35), (30,  20),  (0.0,  0.0,  1.0,  0.5),  True)
        finish.evt_collision.subscribe(self.onFinish)
        
        # Set visited to false for all road parts
        self.road1.visited = False
        self.road2.visited = False
        self.road3.visited = False
        self.road4.visited = False
        
        # Add all entities to Arena
        Arena.add_entity(self.road1)
        Arena.add_entity(self.road2)
        Arena.add_entity(self.road3)
        Arena.add_entity(self.road4)
        Arena.add_entity(finish)
        
        # Create a pair of sensors to guide the car
        blacksensor1 = ColorSensor(24, 12, (0, 0, 0))
        blacksensor2 = ColorSensor(24, -12, (0, 0, 0))
        
        # Add the sensors to the car
        car.add_sensor("fl_sensor", blacksensor1)
        car.add_sensor("fr_sensor", blacksensor2)
        
        self.finished = False
        
        g1 = Goal("Visit all the track parts",  
              lambda : self.road1.visited and self.road2.visited and self.road3.visited and self.road4.visited,  0)
        
        g2 = Goal("Reach the finish line",  lambda : self.finished,  0)
        
        Carcode.set_conditions(Chain(g1,  g2))
        
        eng_score = Score("Engine Utilization",  # Score Title
                           lambda : car.__engine_flips__ ,           # Score Function
                            [(10,  5),  (4, 3), (2, 1),  (0, 0)])           # Score Ranges
                            
        time_score = Score("Time Spend",  # Score Title
                           lambda : int(Carcode.get_game_time()) ,           # Score Function
                            [(50,  35),  (34, 15), (14, 10),  (9, 0)])           # Score Ranges
        
        Carcode.add_score(eng_score)
        Carcode.add_score(time_score)
        
    def update(self):
        pass
        
    def onVisit(self,  obj,  col_evt):
        # When the car collisiones with a road part we consider
        # that part visited and disable collision tests for it
        if not obj.visited:
            obj.visited = True
            obj.collisionable = False
            
    def onFinish(self,  obj,  col_evt):
        self.finished = True
