# arena.py
import pygame, sys, os
import car
from pygame.locals import *

import helpers

DEBUG_EVENTS = False
DEBUG_ARENA = True

WHITE = (250, 250, 250)

class Arena(object):
    def __init__(self, width = 800, height = 800,
                 background_image = 'threeSpaces.png', caption = 'Car Arena'):
        
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        
        pygame.init()
        
        pygame.key.set_repeat(50, 50) # produce multiple key events when a
                                      # key is held down
                                      # (delay, interval) in milliseconds

        # background image
        window = pygame.display.set_mode((width, height))
        try:
            # first try to load a background image, if one has been supplied
            self.background, self.back_rect = helpers.load_image(background_image)
            window = pygame.display.set_mode((self.back_rect.width, self.back_rect.height))
            self.screen = pygame.display.get_surface()
        except Exception, inst:
            if DEBUG_ARENA: print 'Background exception: %s' % inst
            # if for some reason the background image can't be loaded, then make
            # a white background of the supplied width and height
            self.screen = pygame.display.get_surface()
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            self.background.fill(WHITE)
            
        pygame.display.set_caption(caption)
        
        # create the sprites and add them to a renderer
        self.allsprites = pygame.sprite.RenderPlain()  # a pygame sprite Group class

        # is there a keyboard controlled car in the arena?
        self.has_key_car = False
        self.key_car = None

        # list of all the cars in this arena
        self.cars = []

    def __add(self, sprite):
        self.allsprites.add(sprite)

    def add_key_car(self, x = 0, y = 0, running = True, tracer_down = False,
                    show_rect = False):
        """ Add a car controlled by the keyboard.
        """
        if not self.key_car:
            self.has_key_car = True
            self.key_car = car.Car(self.screen, x, y, running_init = running,
                                   tracer_down = tracer_down, show_rect = show_rect)
            self.__add(self.key_car)
            self.__init_key_commands()
            self.cars.append(self.key_car)

    def add_car(self, x = 0, y = 0, running = True):
        """ Add a new car to the arena. Returns a reference to the car.
        """
        c = car.Car(self.screen, x, y, running_init = running)
        self.__add(c)
        self.cars.append(c)
        return c

    def __init_key_commands(self):
        self.key_command = {K_UP:self.key_car.accelerate,
                            K_DOWN:self.key_car.brake,
                            K_LEFT:self.key_car.steer_left,
                            K_RIGHT:self.key_car.steer_right,
                            K_g:self.key_car.flip_gear,
                            K_h:self.key_car.honk,
                            K_s:self.key_car.engine_flip,
                            K_z:self.key_car.blinker_left_flip,
                            K_c:self.key_car.blinker_right_flip}

    def run_main_loop(self):
        # main animation loop
        self.allsprites.draw(self.screen)
        clock = pygame.time.Clock()  # used to help control framerate
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    print 'QUIT event ...'
                    return
                elif self.has_key_car and event.type == KEYDOWN:  # press any key to quit
                    try:
                        self.key_command[event.key]()
                    except KeyError:
                        if DEBUG_EVENTS:
                            print 'Unknown key command: %s' % event.key
                            print self.key_command 
                            print 'Exiting ...'
                        return
                else: 
                    if DEBUG_EVENTS: print event

            self.allsprites.update()
            self.screen.blit(self.background, (0, 0))
            self.allsprites.draw(self.screen)

            # draw car tracers and rectangles
            for car in self.cars:
                if car.tracer_down:
                    # draw on background so that lines are permanent
                    pygame.draw.line(self.background, car.tracer_color,
                                     car.start.center, car.end.center,
                                     car.tracer_width)
                if car.show_rect:
                    # draw on screen so rectangles move
                    pygame.draw.rect(self.screen, (255, 255, 0),
                                     car.image.get_rect(center = car.rect.center), 1)
            
            pygame.display.flip()
