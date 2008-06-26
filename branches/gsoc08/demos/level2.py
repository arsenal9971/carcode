
Arena.add_entity(Box(0, 0, 30, 500, (100,100,100)))
Arena.add_entity(Box(500, 0, 500, 30, (100,100,100)))
Arena.add_entity(Box(0, 470, 30, 500, (100,100,100)))
Arena.add_entity(Box(0, 0, 500, 30, (100,100,100)))

blacksensor1 = ColorSensor(24, 12, (0, 0, 0))
blacksensor2 = ColorSensor(24, -12, (0, 0, 0))

car = Arena.get_car()

car.add_sensor("fl_sensor", blacksensor1)
car.add_sensor("fr_sensor", blacksensor2)