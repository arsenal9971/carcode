# car.py

import pygame
from math import sin, cos, radians

CAR_DEBUG = False

class Light(object):
    """ A car light.
    A light is rectangle with an off color and an on color. You can change or
    query its current color.
    """
    def __init__(self, on_color, off_color, rect):
        self.on_color, self.off_color = on_color, off_color
        self.on = False
        self.rect = rect

    def turn_on(self): self.on = True
    def turn_off(self): self.on = False
    def onoff_flip(self): self.on = not self.on
    def color(self): 
	if self.on:
	    return self.on_color
	else:
	    return self.off_color

class BlinkingLight(Light):
    """ Simulates blinking by flipping the light on or off every
    blink_count calls to color(). Of course, in reality, a blinking
    light usually blinks by time increments, so if for some reason
    color() is called more frequently, or less frequently, than
    normal, the blinking could be too slow or fast.
    """
    def __init__(self, on_color, off_color, rect, blinking = True, blink_count = 50):
        Light.__init__(self, on_color, off_color, rect)  # call superclass constructor
        self.blinking = blinking
        self.blink_count = blink_count  # change color after this many updates
        self.count = 0

    def blink_on(self): self.blinking = True
    def blink_off(self): self.blinking = False
    def blink_flip(self): self.blinking = not self.blinking
    def color(self):
        if self.blinking:
            self.count += 1
            if self.count == self.blink_count:
                self.onoff_flip()
                self.count = 0
        return Light.color(self)

class Car(pygame.sprite.Sprite):
    def __init__(self, screen, x_init = 0, y_init = 0, angle_init = 0.0,
                 body_color = (131, 111, 255)  # SlateBlue1
                 ):
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.original_image = pygame.Surface((48, 25)).convert_alpha() # 48 wide, 25 high

        self.image = self.original_image.copy()
        self.body_color = body_color
        self.rect = self.original_image.fill(self.body_color)  
        self.rect.topleft = x_init, y_init

        # remember the screen so we can get its height/width
        self.screen = screen

        # the distance increment in the x and y directions
        self.dx, self.dy = 0.0, 0.0

        # current heading
        self.angle = angle_init

        # current speed
        self.speed = 0.0

        # decceleration
        self.decel = 0.985
        self.eps = 1.0  # values less than this are considered 0

        # gear: forward or reverse
        self.forward_gear = True
        
        # set the light colors
        brake_off_color = (255, 99, 71) # tomato
        brake_on_color = (255, 0, 0) # red
        turn_off_color = (255, 165, 0) # orange
        turn_on_color = (255, 69, 0)  # orange red

        # create the lights
        self.l_brake = Light(brake_off_color, brake_on_color,
                             pygame.Rect(0, 5, 8, 5))
        self.r_brake = Light(brake_off_color, brake_on_color,
                             pygame.Rect(0, 15, 8, 5))

        self.l_brake.turn_off()
        self.r_brake.turn_off()
        
        self.fl_turn = BlinkingLight(turn_on_color, turn_off_color,
                                     pygame.Rect(0, 0, 8, 5))
        self.fr_turn = BlinkingLight(turn_on_color, turn_off_color,
                                     pygame.Rect(0, 20, 8, 5))
        self.bl_turn = BlinkingLight(turn_on_color, turn_off_color,
                                     pygame.Rect(40, 0, 8, 5))
        self.br_turn = BlinkingLight(turn_on_color, turn_off_color,
                                     pygame.Rect(40, 20, 8, 5))
        self.fl_turn.blink_off()
        self.fr_turn.blink_off()
        self.bl_turn.blink_off()
        self.br_turn.blink_off()

        # store all the lights in a list for easy processing
        self.lights = [self.l_brake, self.r_brake, self.fl_turn, self.fr_turn,
                       self.bl_turn, self.br_turn]

        # load horn sound
        self.sound = False
        if pygame.mixer:
            pygame.mixer.music.set_volume(0.5)  # between 0.0 and 1.0
            try:
                pygame.mixer.music.load('data/carhornshort.wav')
                self.sound = True
            except:
                print 'Could not load car horn sound effect.'
        if CAR_DEBUG: print 'Car __init__ finished'

    def speed(self): return self.speed

    def moving(self): return abs(self.speed) > self.eps

    def accelerate(self, s = 2):
        if self.forward_gear:
            self.speed += s
        else:
            self.speed -= s

    def brake(self, s = 0.8):
        if self.moving():
            if self.forward_gear:
                self.speed -= s
            else:
                self.speed += s

    def set_gear_reverse(self):
        self.forward_gear = False

    def set_gear_forward(self):
        self.forward_gear = True

    def flip_gear(self):
        self.forward_gear = not self.forward_gear

    def honk(self):
        if self.sound: pygame.mixer.music.play()
    
    def steer_left(self, deg = 7.0):
        if self.moving(): self.angle = round(self.angle + deg) % 360
            
    def steer_right(self, deg = -7.0):
        if self.moving(): self.angle = round(self.angle + deg) % 360
 
    def update(self):
        # copy the original unrotated car body
        self.image = self.original_image.copy()
        
        # draw the lights
        for light in self.lights:
            self.image.fill(light.color(), light.rect)
	
        # rotate the car around the axel point
	##self.image = pygame.transform.scale2x(self.image)
        ##self.image = pygame.transform.rotate(self.image, self.angle)
	self.image = pygame.transform.rotozoom(self.image, self.angle, 2.8)

        # move to new position
        if self.moving():
            # calculate new dx, dy values
            ##self.__forward()
            rad = radians(self.angle)
            self.dx = self.speed * cos(rad)
            self.dy = -self.speed * sin(rad)
            
            self.rect.top = (round(self.rect.top + self.dy)) % self.screen.get_height()
            self.rect.left = (round(self.rect.left + self.dx)) % self.screen.get_width()
            self.speed *= self.decel  # deccelerate the car
        else:
            self.speed = 0


        if CAR_DEBUG:
            print '(speed = %s, moving = %s, forward_gear = %s, dx = %s, dy = %s, angle = %s)' % (self.speed,
                                                                                                  self.moving(),
                                                                                                  self.forward_gear,
                                                                                                  self.dx,
                                                                                                  self.dy,
                                                                                                  self.angle)