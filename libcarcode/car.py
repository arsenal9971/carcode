import os, time
from math import sin, cos, radians, sqrt

import pygame
from OpenGL.GL import *
from collision import pyLine, BoundingBox
from events import EventDispatcher
import helpers

DEBUG = False

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
    def __init__(self, x_init = 0, y_init = 0, angle_init = 0.0,
                 running_init = True,
                 body_color = (131, 111, 255),  # SlateBlue1
                 tracer_color = (255, 0, 0),  # red
                 tracer_down = False,
                 tracer_width = 1,
                 show_rect = False
                 ):
        self.body_color = body_color

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
                                pygame.Rect(-24, -4, 3, 9))  # (left, top, width, height)
        
        self.fl_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(-24, -12, 8, 5))
        self.fr_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(-24, 8, 8, 5))
        self.bl_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(16, -12, 8, 5))
        self.br_turn = Blinker(turn_on_color, turn_off_color,
                               pygame.Rect(16, 8, 8, 5))

        # store all the lights in a list for easy processing
        self.lights = [self.rear_brake, self.fl_turn, self.fr_turn,
                       self.bl_turn, self.br_turn]

        # load sound effects
        self.horn_sound = helpers.load_sound('carhornshort.wav')
        self.start_sound = helpers.load_sound('Carstart.wav')
        self.idle_sound = helpers.load_sound('car_idle.wav', volume = 0.05)
        
        self.tracer_color = tracer_color
        self.tracer_down = tracer_down
        self.tracer_width = tracer_width
        
        # flags
        self.show_rect = show_rect
        self.x = 0
        self.y = 0
        
        self.sensors = {}
        self.lines = []
        self.script = None
        self.bbox = BoundingBox(0, 0, 24, 48)
        
        self.__engine_flips__ = 0
        self.__gear_flips__ = 0
        self.__honk_count__ = 0
        
        self.on_honk = EventDispatcher()
        
        #glEnable(GL_TEXTURE_2D)
        #Set texture parametes, wraping and filters
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    
    def set_script(self, script):
        self.script = script
        
    def add_sensor(self, name, sensor):
        self.sensors[name] = sensor
        
    def flip_engine(self):
        self.__engine_flips__ += 1
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
            for light in self.lights:
                light.turn_on()
            
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
        self.__gear_flips__ += 1
        self.forward_gear = not self.forward_gear

    def honk(self):
        self.__honk_count__ += 1
        self.horn_sound.play()
        self.on_honk.dispatch(self)
    
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
        for sensor in self.sensors.values():
            sensor.update(self.angle)
            
        if self.tracer_down:
            if self.moving():
                line = pyLine(self.start, self.end)
                if len(self.lines) == 0:
                    self.lines.append(line)
                else:
                    last = self.lines[-1]
                    if last == line:
                        last += line
                    else:
                        self.lines.append(line)
        
        if len(self.lines) > 0:
            glBegin(GL_LINES)
            glColor3ub(*self.tracer_color)
            for line in self.lines:
                glVertex2f(line.x1, line.y1)
                glVertex2f(line.x2, line.y2)
            glEnd()
            
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(400, 300, 0.0)
        glRotatef(-self.angle, 0.0, 0.0, 1.0)
        
        glColor3ub(131, 111, 255)
        glRecti(-24, -12, 24, 12)
        
        for light in self.lights:
            r = light.rect
            glColor3ub(*light.color())
            glRecti(r.x, r.y, r.x + r.width, r.y+r.height)
        glPopMatrix()
        
        if DEBUG:
            self.bbox.draw()
        
    def update(self):
        # move to new position
        if self.moving():
            # remember starting position
            self.start = (self.x, self.y)
            
            rad = radians(self.angle)
            self.dx = self.speed * cos(rad) 
            self.dy = -self.speed * sin(rad)
            
            self.y = self.y + self.dy
            self.x = self.x + self.dx

            self.end = (self.x, self.y)
            
            self.speed *= self.decel  # deccelerate the car
        else:
            self.speed = 0
        self.bbox.x = self.x
        self.bbox.y = self.y
        self.bbox.angle = self.angle
        self.bbox.update()
        
        if self.script:
            self.script.call('main', self)