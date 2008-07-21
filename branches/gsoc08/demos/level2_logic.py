
class CarScript:
    def __init__(self,  car):
        # Obtain the car sensors (left, right)
        self.lsensor = car.sensors["fl_sensor"]
        self.rsensor = car.sensors["fr_sensor"]
        self.car = car
    
    def update(self,  car):
        if self.lsensor.pixel and not self.rsensor.pixel:
            car.steer_right()
        
        # Check if the right sensor detected that we
        # are offroad and steer left
        if not self.lsensor.pixel and self.rsensor.pixel:
            car.steer_left()
    
        # Check if both sensors detect we are offroad
        # try to steer right until we find the road back
        if self.lsensor.pixel and self.rsensor.pixel:
            car.steer_right()
        
        # Accelerate constantly
        if not car.moving() or car.speed < 2:
            car.accelerate()
