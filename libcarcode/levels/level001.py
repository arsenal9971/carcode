
class LevelScript:
    name = "Entry"
    description = """
    """
    def __init__(self):
        road_points = [(-50,  -20),  (800,  -20)]
        road = Road(road_points)
        
        Arena.add_entity(road)
        Arena.add_entity(Box((780, -70),( 25, 100),  (0,0,1.0)))
        
        car = Arena.get_car()
        
        sensor = ColorSensor(24, 0, (0, 0, 255))
        car.add_sensor("mainsensor", sensor)
        
        g1 = Goal("Reach the finish line", 
                  lambda : sensor.pixel,  0)
                  
        Carcode.set_goals([g1])
        
        eng_score = Score("Engine Utilization",  # Score Title
                           lambda : car.__engine_flips__ ,           # Score Function
                            [(10,  5),  (4, 3), (2, 1),  (0, 0)])           # Score Ranges
                            
        time_score = Score("Time Spend",  # Score Title
                           lambda : int(Carcode.get_game_time()) ,           # Score Function
                            [(10,  5),  (4, 2), (2, 1),  (1, 0)])           # Score Ranges
        
        Carcode.set_scores([eng_score,  time_score])
        
    def update(self):
        pass
