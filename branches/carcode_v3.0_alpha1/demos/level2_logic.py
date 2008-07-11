
# main function
def main(car):
    # Obtain the car sensors (left, right)
    lsensor = car.sensors["fl_sensor"]
    rsensor = car.sensors["fr_sensor"]

    # Check if the left sensor detected that we
    # are offroad and steer right
    if lsensor.pixel and not rsensor.pixel:
        car.steer_right()
        
    # Check if the right sensor detected that we
    # are offroad and steer left
    if not lsensor.pixel and rsensor.pixel:
        car.steer_left()
    
    # Check if both sensors detect we are offroad
    # try to steer right until we find the road back
    if lsensor.pixel and rsensor.pixel:
        car.steer_right()
        
    # Accelerate constantly
    if not car.moving() or car.speed < 2:
        car.accelerate()
