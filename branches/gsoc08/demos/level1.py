'''
    Straight Path Test
    In this test you have to travel the
    straight path until you reach the
    endline colored blue, beware of
    going off the road!
'''                

def onSensor(sensor):
    if sensor.pixel:
        Console.clear()
        Console.write('Got to finish line!')
    
def onOffroad(sensor):
    if sensor.pixel:
        Console.write( 'You got off the road!')
        

Arena.add_entity(Box(-30, -25, 50, 810, (100,100,100)))
Arena.add_entity(Box(780, -25, 50, 25, (0,0,255)))

car = Arena.get_car()

sensor = ColorSensor(24, 0, (0, 0, 255))
sensor.on_update.subscribe(onSensor)

blacksensor1 = ColorSensor(24, 12, (0, 0, 0))
blacksensor2 = ColorSensor(24, -12, (0, 0, 0))
blacksensor1.on_update.subscribe(onOffroad)
blacksensor2.on_update.subscribe(onOffroad)

car.add_sensor("blacksensor1", blacksensor1)
car.add_sensor("blacksensor2", blacksensor2)
car.add_sensor("mainsensor", sensor)