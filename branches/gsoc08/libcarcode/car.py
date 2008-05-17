import os, time
from math import sin, cos, radians

import pygame
from OpenGL.GL import *

import helpers

CAR_DEBUG = False
TRACER_CAR_DEBUG = True

class Light(object):
    """ A car light.
    A light is rectangle with an off color and an on color. You can change or
    query its current color.
    """
    def __init__(self, on_color, off_color, rect):
        self.on_color, self.off_color = on_color, off_color
        self.on = False
        self.cc = off_color   # current color
        self.rect = rect

    def turn_on(self):
        self.on = True
        self.cc = self.on_color

    def turn_off(self):
        self.on = False
        self.cc = self.off_color

    def onoff_flip(self):
        if self.on:
            self.turn_off()
        else:
            self.turn_on()

    def color(self):
        return self.cc
    

class Blinker(Light):
    """ Blinks by flipping the light color every  blink_count calls to color().
    Of course, in reality, a blinking light usually blinks by time increments, so if
    for some reason color() is called more frequently or less frequently than
    normal, the blinking could be too slow or fast.
    """
    def __init__(self, on_color, off_color, rect, blinking = False, blink_count = 50):
        Light.__init__(self, on_color, off_color, rect)  # call superclass constructor
        self.blink_count = blink_count  # change color after this many updates
        self.count = 0

    def color_flip(self):
        if self.cc == self.on_color:
            self.cc = self.off_color
        else:
            self.cc = self.on_color

    def color(self):
        if not self.on:
            return self.cc
        else:
            self.count += 1
            if self.count == self.blink_count:
                self.color_flip()
                self.count = 0
            return self.cc

class Car:
    def __init__(self, screen, x_init = 0, y_init = 0, angle_init = 0.0,
                 running_init = True,
                 body_color = (131, 111, 255),  # SlateBlue1
                 tracer_color = (255, 0, 0),  # red
                 tracer_down = False,
                 tracer_width = 1,
                 show_rect = False
                 ):
        #pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        #self.original_image = pygame.Surface((48, 25)).convert_alpha() # 48 wide, 25 high

        #self.image = self.original_image.copy()
        self.body_color = body_color
        self.rect = pygame.Rect(x_init, y_init,0,0)
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

        # is the car engine on?
        self.running = running_init
        
        # set the light colors
        brake_off_color = (255, 99, 71) # tomato
        brake_on_color = (255, 0, 0) # red
        turn_off_color = (255, 165, 0) # orange
        turn_on_color = (255, 69, 0)  # orange red

        # create the lights
        self.rear_brake = Light(brake_off_color, brake_on_color,
                                pygame.Rect(0, 8, 3, 9))  # (left, top, width, height)
        
        self.fl_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(0, 0, 8, 5))
        self.fr_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(0, 20, 8, 5))
        self.bl_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(40, 0, 8, 5))
        self.br_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(40, 20, 8, 5))

        # store all the lights in a list for easy processing
        self.lights = [self.rear_brake, self.fl_turn, self.fr_turn,
                       self.bl_turn, self.br_turn]

        # load sound effects
        self.horn_sound = helpers.load_sound('carhornshort.wav')
        self.start_sound = helpers.load_sound('Carstart.wav')
        self.idle_sound = helpers.load_sound('car_idle.wav', volume = 0.05)
        # or: hotidle.wav

        # tracer
        self.tracer_color = tracer_color
        self.tracer_down = tracer_down
        self.tracer_width = tracer_width
        self.start, self.end = self.rect, self.rect
        
        # flags
        self.ltime = time.time()
        self.show_rect = show_rect
        self.x = 0
        self.y = 0
        glEnable(GL_TEXTURE_2D)
        self.texture = glGenTextures(1)
        
        self.img, rect = helpers.load_image("carcode-carsm.png")
        data = pygame.image.tostring(self.img, "RGBA")

        glBindTexture(GL_TEXTURE_2D, self.texture)
        w = self.img.get_width()
        h = self.img.get_height()
        
        # Bind data to texture
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        #Set texture parametes, wraping and filters
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        if CAR_DEBUG: print 'Car __init__ finished'

    def flip_engine(self):
        if self.running:
            self.engine_off()
        else:
            self.engine_on()
            
    def engine_on(self):
        if not self.running:            
            self.running = True
            self.start_sound.play()
            # wait until the starting sound finishes 
            # before playing the idling sound
            time.sleep(self.start_sound.get_length())
            self.idle_sound.play(-1)  # loop sound forever
            
    def engine_off(self):
        if self.running:
            self.running = False
            self.idle_sound.stop()
            # turn off all the lights
            for light in self.lights:
                light.turn_off()

    def speed(self): return self.speed

    def moving(self): return abs(self.speed) > self.eps

    def accelerate(self, s = 2):
        if self.running:
            if self.forward_gear:
                self.speed += s
            else:
                self.speed -= s

    def brake(self, s = 2):
        if self.running and self.moving():
            if self.forward_gear:
                self.speed -= s
            else:
                self.speed += s

    def flip_tracer(self):
        self.tracer_down = not self.tracer_down
    
    def set_tracer_down(self):
        self.tracer_down = True

    def set_tracer_up(self):
        self.tracer_down = False
    
    def set_gear_reverse(self):
        self.forward_gear = False

    def set_gear_forward(self):
        self.forward_gear = True

    def flip_gear(self):
        self.forward_gear = not self.forward_gear

    def honk(self):
        self.horn_sound.play()
    
    def steer_left(self, deg = 7.0):
        if self.running and self.moving(): self.angle = round(self.angle + deg) % 360
            
    def steer_right(self, deg = -7.0):
        if self.running and self.moving(): self.angle = round(self.angle + deg) % 360

    # turn on/off left indicator lights
    def blinker_left_flip(self):
        if self.running:
            self.fl_turn.onoff_flip()
            self.bl_turn.onoff_flip()

        
    # turn on/off right indicator lights
    def blinker_right_flip(self):
        if self.running:
            self.fr_turn.onoff_flip()
            self.br_turn.onoff_flip()
    
    def draw(self):
        self.update()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(360, 280, 0.0)
        glRotatef(-self.angle, 0.0, 0.0, 1.0)
        #glTranslatef(-400, -300, 0.0)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        glBegin(GL_QUADS)
        #glColor3i(131, 111, 255)
        glColor4f(0.0,0.0,0.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex2i(-45, -20)
        glTexCoord2f(1.0, 0.0)
        glVertex2i(45, -20)
        glTexCoord2f(1.0, 1.0)
        glVertex2i(45, 20)
        glTexCoord2f(0.0, 1.0)
        glVertex2i(-45, 20)
        glEnd()
        #surface.fill((255,255,255), self.image.get_rect(topleft=self.rect.topleft))
        
    def update(self):
        # copy the original unrotated car body
        #self.image = self.original_image.copy()
        
        # draw the lights
        #for light in self.lights:
        #    self.image.fill(light.color(), light.rect)
	
    	#self.image = pygame.transform.rotozoom(self.image, self.angle, 2.8)
        
        # move to new position
        if self.moving():
            # remember starting position
            self.start = (self.x, self.y)
            
            ctime = time.time() - self.ltime
            rad = radians(self.angle)
            self.dx = self.speed * cos(rad) * ctime
            self.dy = -self.speed * sin(rad) * ctime
            
            self.y = (round(self.y + self.dy)) % self.screen.get_height()
            self.x = (round(self.x + self.dx)) % self.screen.get_width()

            self.start = (self.x, self.y)
            self.ltime = ctime
            
            # remember ending position
            #self.end = self.rect
            
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


## class TraceCar(Car):
##     def __init__(self, screen, x_init = 0, y_init = 0, angle_init = 0.0,
##                  running_init = True,
##                  body_color = (131, 111, 255),  # SlateBlue1
##                  tracer_color = (255, 0, 0),    # red
##                  tracer_down = True
##                  ):
##         Car.__init__(self, screen, x_init, y_init,   # call Car initializer
##                      angle_init, running_init, body_color)
##         self.tracer_color = tracer_color
##         self.tracer_down = tracer_down
##         self.start, self.end = self.rect, self.rect

##     def update(self):
##         # copy the original unrotated car body
##         self.image = self.original_image.copy()
        
##         # draw the lights
##         for light in self.lights:
##             self.image.fill(light.color(), light.rect)
	
##         # rotate the car around the axel point
## 	##self.image = pygame.transform.scale2x(self.image)
##         self.image = pygame.transform.rotate(self.image, self.angle)
## 	##self.image = pygame.transform.rotozoom(self.image, self.angle, 2.8)

##         # move to new position
##         if self.moving():
##             # remember starting position
##             self.start = self.rect.move(0, 0)  # better way to copy a rect?
            
##             # calculate new dx, dy values
##             rad = radians(self.angle)
##             self.dx = self.speed * cos(rad)
##             self.dy = -self.speed * sin(rad)
            
##             self.rect.top = (round(self.rect.top + self.dy)) % self.screen.get_height()
##             self.rect.left = (round(self.rect.left + self.dx)) % self.screen.get_width()

##             # remember ending position
##             self.end = self.rect.move(0, 0)  # better way to copy a rect?

##             # deccelerate the car
##             self.speed *= self.decel  
##         else:
##             self.speed = 0

