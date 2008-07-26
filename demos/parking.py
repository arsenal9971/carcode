'''
    Park Test
'''                

WHITE = (255,255,255)
car = Arena.get_car()
DEBUG = False

class ParkPlace(ccEntity):
    def __init__(self, x, y, color=(0,0,0), col = False):
        ccEntity.__init__(self,  0)
        self.x = x
        self.y = y
        self.l1 = Box((x, y), (70, 5), WHITE)
        self.l2 = Box((x, y+50), (70,  5), WHITE)
        self.l3 = Box((x+ 70, y), (5,  55), WHITE)
        self.l4 = Box((x, y+5), (70,  45), color,  True)
        
        self.collisionable = col
        
        self.get_region = self.l4.get_region
        self.get_center = self.l4.get_center
        self.evt_collision = self.l4.evt_collision
        
    def draw(self):
        self.l1.draw()
        self.l2.draw()
        self.l3.draw()
        self.l4.draw()
        
    def update(self):
        pass

class LevelScript:
    def __init__(self):
        self.inParking = False
        park = ParkPlace(100, 50, color=(200,0,0), col=True)
        
        Arena.add_entity(ParkPlace(100, 0))
        Arena.add_entity(park)
        Arena.add_entity(ParkPlace(100, 100))
        Arena.add_entity(ParkPlace(100, 150))
        
        park.evt_collision.subscribe(self.onCollision)
        g1 = Goal("Park in the red zone",  lambda : self.inParking and not car.running,  1)
        g2= Goal("Park horizontally",  lambda : abs(car.angle) < 1.8,  2 )
        Carcode.set_conditions(Chain(g1,  g2))
        
        Console.write("Park over the red zone")
        
        eng_score = Score("Engine Utilization",  # Score Title
                           lambda : car.__engine_flips__ ,           # Score Function
                            [(10,  5),  (4, 3), (2, 1),  (0, 0)])           # Score Ranges
                            
        time_score = Score("Time Spend",  # Score Title
                           lambda : int(Carcode.get_game_time()) ,           # Score Function
                            [(50,  10),  (9, 5), (4, 3),  (2, 0)])           # Score Ranges
        
        Carcode.add_score(eng_score)
        Carcode.add_score(time_score)
    
    def update(self):
        st = Carcode.get_state()
        if st == 0:
            Console.clear()
            Console.write("Park over the red zone")
        elif st == 1:
            Console.clear()
            Console.write('Now park the car horizontally!')
        else:
            Console.clear()
            Console.write('Parked ok!')
            
    def onCollision(self,  entity,  event):
        if event[1]:
            self.inParking = True
        else:
            self.inParking = False
