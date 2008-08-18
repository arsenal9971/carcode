
class LevelScript:
    name = "Simple Paths"
    description = """
    """
    def __init__(self):
        self.finished = False
        
        road_points = [(-50,  -20),  (400,  -20), (400, 400), (-50, 400), (-50, -70)]
        road = Road(road_points)
        Arena.add_entity(road)
        
        self.finishline = Box((-100, 30), (100, 25),  (0,0,1.0), True) 
        self.finishline.evt_collision.subscribe(self.on_finish)
        
        Arena.add_entity(self.finishline)
        
        car = Arena.get_car()
        
        self.rsensor = ColorSensor(24, -12, (0, 0, 0))
        self.lsensor = ColorSensor(24, 12, (0, 0, 0))
        
        car.add_sensor("left_sensor", self.lsensor)        
        car.add_sensor("right_sensor", self.rsensor)
        
        g1 = Goal("Reach the finish line", 
                  lambda : self.finished == True,  0)
                  
        Carcode.set_goals([g1])
        
        eng_score = Score("Engine Utilization",  # Score Title
                           lambda : car.__engine_flips__ ,           # Score Function
                            [(10,  5),  (4, 3), (2, 1),  (0, 0)])           # Score Ranges
                            
        time_score = Score("Time Spend",  # Score Title
                           lambda : int(Carcode.get_game_time()) ,           # Score Function
                            [(10,  5),  (4, 2), (2, 1),  (1, 0)])           # Score Ranges
        
        Carcode.set_scores([eng_score,  time_score])

    def on_finish(self, obj, evt):
        print "Finished"
        self.finished = True
        
    def update(self):
        pass
