
def main(car):
    lsensor = car.sensors["fl_sensor"]
    rsensor = car.sensors["fr_sensor"]
    
    if lsensor.pixel and not rsensor.pixel:
        car.steer_right()
    if not lsensor.pixel and rsensor.pixel:
        car.steer_left()
    if lsensor.pixel and rsensor.pixel:
        car.steer_right()
    if not car.moving() or car.speed < 2:
        car.accelerate()
