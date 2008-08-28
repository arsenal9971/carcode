class Path(ccEntity):
    def __init__(self, points, color=(255,255,255)):
        ccEntity.__init__(self)
        self.points = points
        self.color = color
    
    def draw(self):
        # Get line width and save it
        width = glGetIntegerv(GL_LINE_WIDTH)
        
        glLineWidth(3)
        glColor3ub(255,255,255)
        glBegin(GL_LINE_STRIP)
        for v in self.points:
            glVertex2i(*v)
        glEnd()
        glLineWidth(width)

class LevelScript:
    name = "Simple Paths"
    description = """
    """
    def __init__(self):
        self.finished = False
        
        road_points = [(-50,  0), (400,0), (800, 100), (800, 500), (400, 200), (100, 300), (0, 300)]
        road = Path(road_points)
        Arena.add_entity(road)
        
        startline = Box((-60, -40), (20, 80),  (0,1.0,0.0))
        Arena.add_entity(startline)
        
        self.finishline = Box((-10, 260), (20, 80),  (0,0,1.0), True) 
        self.finishline.evt_collision.subscribe(self.on_finish)
        Arena.add_entity(self.finishline)
        
        car = Arena.get_car()
        
        self.csensor = ColorSensor(5, 0, (0, 0, 0))
        self.rsensor = ColorSensor(5, -2, (0, 0, 0))
        self.lsensor = ColorSensor(5, 2, (0, 0, 0))
        
        car.add_sensor("center_sensor", self.csensor)
        car.add_sensor("left_sensor", self.lsensor)
        car.add_sensor("right_sensor", self.rsensor)
        
        g1 = Goal("Reach the blue finish line", 
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
        self.finished = True
        
    def update(self):
        pass
