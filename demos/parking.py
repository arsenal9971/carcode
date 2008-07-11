'''
    Park Test
'''                

WHITE = (255,255,255)
car = Arena.get_car()
DEBUG = False

def onCollision(entity,  event):
    if event[1]:
        if abs(car.angle) > 2:
            Console.clear()
            Console.write('Now park the car horizontally!')
        else:
            Console.clear()
            Console.write('Parked ok!')
    else:
        Console.clear()
        Console.write("Park over the red zone")
        
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
    
park = ParkPlace(100, 50, color=(200,0,0), col=True)

Arena.add_entity(ParkPlace(100, 0))
Arena.add_entity(park)
Arena.add_entity(ParkPlace(100, 100))
Arena.add_entity(ParkPlace(100, 150))

park.evt_collision.subscribe(onCollision)

Console.write("Park over the red zone")

