
def onVisit(obj,  col_evt):
    if not obj.visited:
        obj.visited = True
        obj.collisionable = False

def onFinish(obj,  col_evt):
    if road1.visited and road2.visited and road3.visited and road4.visited:
        print 'Finished!'
    else:
        print 'Did not visit all the paths'
road1 = Box((0, 0),  (500,  30), (0.4,0.4,0.4),  True)
road2 = Box((500, 0),  (30,  500), (0.4,0.4,0.4),  True)
road3 = Box((0, 470),  (500,  30), (0.4,0.4,0.4),  True)
road4 = Box((0, 0),  (30,  500), (0.4,0.4,0.4),  True)

road1.evt_collision.subscribe(onVisit)
road2.evt_collision.subscribe(onVisit)
road3.evt_collision.subscribe(onVisit)
road4.evt_collision.subscribe(onVisit)

finish = Box((0,  35), (30,  20),  (0.0,  0.0,  1.0,  0.5),  True)
finish.evt_collision.subscribe(onFinish)

road1.visited = False
road2.visited = False
road3.visited = False
road4.visited = False

Arena.add_entity(road1)
Arena.add_entity(road2)
Arena.add_entity(road3)
Arena.add_entity(road4)
Arena.add_entity(finish)

blacksensor1 = ColorSensor(24, 12, (0, 0, 0))
blacksensor2 = ColorSensor(24, -12, (0, 0, 0))

car = Arena.get_car()

car.add_sensor("fl_sensor", blacksensor1)
car.add_sensor("fr_sensor", blacksensor2)
