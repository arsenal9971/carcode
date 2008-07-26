'''
    Straight Path Test
    In this test you have to travel the
    straight path until you reach the
    endline colored blue, beware of
    going off the road!
'''                

car = Arena.get_car()

class LevelScript:
    def __init__(self):
        Arena.add_entity(Box((-30, -25),  (810,  50), (0.4,0.4,0.4)))
        Arena.add_entity(Box((780, -25),( 25, 50),  (0,0,1.0)))
        
        sensor = ColorSensor(24, 0, (0, 0, 255))
        sensor.on_update.subscribe(self.onSensor)
        
        blacksensor1 = ColorSensor(24, 12, (0, 0, 0))
        blacksensor2 = ColorSensor(24, -12, (0, 0, 0))
        blacksensor1.on_update.subscribe(self.onOffroad)
        blacksensor2.on_update.subscribe(self.onOffroad)
        
        car.add_sensor("blacksensor1", blacksensor1)
        car.add_sensor("blacksensor2", blacksensor2)
        car.add_sensor("mainsensor", sensor)
        
        g1 = Goal("Reach the finish line", 
                  lambda : sensor.pixel,  0)
        Carcode.set_conditions(Chain(g1))
        
        eng_score = Score("Engine Utilization",  # Score Title
                           lambda : car.__engine_flips__ ,           # Score Function
                            [(10,  5),  (4, 3), (2, 1),  (0, 0)])           # Score Ranges
                            
        time_score = Score("Time Spend",  # Score Title
                           lambda : int(Carcode.get_game_time()) ,           # Score Function
                            [(10,  5),  (4, 2), (2, 1),  (1, 0)])           # Score Ranges
        
        Carcode.add_score(eng_score)
        Carcode.add_score(time_score)
        
    def update(self):
        pass
        
    def onSensor(self,  sensor):
        if sensor.pixel:
            Console.clear()
            Console.write('Got to finish line!')
        
    def onOffroad(self,  sensor):
        if sensor.pixel:
            Console.write( 'You got off the road!')

