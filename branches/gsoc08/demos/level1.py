'''
    Straight Path Test
    In this test you have to travel the
    straight path until you reach the
    endline colored blue, beware of
    going off the road!
'''                

def onSensor(sensor):
    if sensor.pixel:
        print 'Got to finish line!'
    
def onOffroad(sensor):
    if sensor.pixel:
        print 'You got off the road!'
        

Arena.add_entity(Box(-10, 0, 50, 810, (100,100,100)))
Arena.add_entity(Box(800, 0, 50, 25, (0,0,255)))

car = Arena.get_car()

sensor = ColorSensor(24, 0, (0, 0, 255))
sensor.events.subscribe('Sensor', onSensor)

blacksensor1 = ColorSensor(24, 12, (0, 0, 0))
blacksensor2 = ColorSensor(24, -12, (0, 0, 0))
blacksensor1.events.subscribe('Sensor', onOffroad)
blacksensor2.events.subscribe('Sensor', onOffroad)

car.add_sensor(blacksensor1)
car.add_sensor(blacksensor2)
car.add_sensor(sensor)