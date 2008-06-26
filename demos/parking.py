'''
    Park Test
'''                

WHITE = (255,255,255)
car = Arena.get_car()
DEBUG = False

def onCollision(entity):
    if entity.bbox.contains(car.bbox):
        Console.clear()
        Console.write('Parked ok!')
        
class ParkPlace:
    def __init__(self, x, y, color=(0,0,0), col = False):
        self.x = x
        self.y = y
        self.l1 = Box(0, 0, 5, 70, WHITE)
        self.l2 = Box(0, 50, 5, 70, WHITE)
        self.l3 = Box(70, 0, 55, 5, WHITE)
        self.l4 = Box(0, 5, 45, 70, color)
        self.bbox = BoundingBox(x+35, y+25, 50, 70)
        self.bbox.update()
        self.collisionable = col
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.0)
        self.l1.draw()
        self.l2.draw()
        self.l3.draw()
        self.l4.draw()
        glPopMatrix()
        if DEBUG:
            self.bbox.draw()
    def update(self):
        pass
    
Arena.add_entity(ParkPlace(100, 0))
Arena.add_entity(ParkPlace(100, 50, color=(200,0,0), col=True))
Arena.add_entity(ParkPlace(100, 100))
Arena.add_entity(ParkPlace(100, 150))
Arena.on_collision.subscribe(onCollision)
Console.write("Park over the red zone")

