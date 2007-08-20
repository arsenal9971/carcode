# arena.py
import pygame, sys, os
import car
from pygame.locals import *

DEBUG_EVENTS = False
DEBUG_ARENA = True

def load_image(name, colorkey = None, data_folder = 'data'):
    """ Utility function for loading images.
    Returns (image, rectangle).
    """
    fullname = os.path.join(data_folder, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Arena(object):
    def __init__(self, width = 800, height = 800, background_image = 'threeSpaces.png', caption = 'Car Arena'):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        
        pygame.init()
        
        pygame.key.set_repeat(50, 50) # produce multiple key events when a
                                      # key is held down
                                      # (delay, interval) in milliseconds

        # make the background
        ##self.background = pygame.Surface(self.screen.get_size())
        ##self.background = self.background.convert()
        ##self.background.fill((250, 250, 250))   # white

        # background image
        window = pygame.display.set_mode((width, height))
        try:
            # first try to load a background image, if one has been supplied
            self.background, self.back_rect = load_image(background_image)
            window = pygame.display.set_mode((self.back_rect.width, self.back_rect.height))
            self.screen = pygame.display.get_surface()
        except Exception, inst:
            if DEBUG_ARENA: print 'Background exception: %s' % inst
            # if for some reason the background image can't be loaded, then make a white background
            # of the supplied width and height
            self.screen = pygame.display.get_surface()
            self.background = pygame.Surface(self.screen.get_size())
            self.background = self.background.convert()
            self.background.fill((250, 250, 250))   # white
            
        pygame.display.set_caption(caption)
        
        # create the sprites and add them to a renderer
        self.allsprites = pygame.sprite.RenderPlain()  # a pygame sprite Group class

        # is there a keyboard controlled car in the arena?
        self.key_car = False

        # list of all the cars in this arena
        self.cars = []

    def __add(self, sprite):
        self.allsprites.add(sprite)

    def add_key_car(self, x = 0, y = 0, running = True):
        """ Add a car controlled by the keyboard.
        """
        if not self.key_car:
            self.key_car = True
            self.kcar = car.Car(self.screen, x, y, running_init = running)
            self.__add(self.kcar)
            self.__init_key_commands()
            print self.key_command
            self.cars.append(self.kcar)

    def add_car(self, x = 0, y = 0):
        """ Add a new car to the arena. Returns a reference to the car.
        """
        c = car.Car(self.screen, x, y)
        self.__add(c)
        self.cars.append(c)
        return c

    def __init_key_commands(self):
        self.key_command = {K_UP:self.kcar.accelerate,
                            K_DOWN:self.kcar.brake,
                            K_LEFT:self.kcar.steer_left,
                            K_RIGHT:self.kcar.steer_right,
                            K_g:self.kcar.flip_gear,
                            K_h:self.kcar.honk,
                            K_s:self.kcar.turn_flip}

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
                elif self.key_car and event.type == KEYDOWN:  # press any key to quit
                    try:
                        self.key_command[event.key]()
                    except KeyError:
                        print 'Unknown key command: %s' % event.key
                        print self.key_command 
                        print 'Exiting ...'
                        return

                    ## if event.key == K_UP:
##                         self.kcar.accelerate()
##                     elif event.key == K_DOWN:
##                         self.kcar.brake()
##                     elif event.key == K_LEFT:
##                         self.kcar.steer_left()
##                     elif event.key == K_RIGHT:
##                         self.kcar.steer_right()
##                     elif event.key == K_g:
##                         self.kcar.flip_gear()
##                     elif event.key == K_h:
##                         self.kcar.honk()
##                     else:
##                         sys.exit(0)
                else: 
                    if DEBUG_EVENTS: print event

            self.allsprites.update()
            self.screen.blit(self.background, (0, 0))
            self.allsprites.draw(self.screen)
            pygame.display.flip()
