import sys, os

import pygame
from pygame.locals import *

CARCODE_PATH = os.path.dirname(sys.modules[__name__].__file__)
IMAGE_PATH = os.path.join(CARCODE_PATH, 'media', 'images')
SOUND_PATH = os.path.join(CARCODE_PATH, 'media', 'sound')

def load_sound(filename, volume = 0.5):
    try:
        fullname = os.path.join(SOUND_PATH, filename)
        sound = pygame.mixer.Sound(fullname)
        sound.set_volume(volume)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message

    return sound

def load_image(filename, colorkey = None):
    """ Utility function for loading images.
    Returns (image, rectangle).
    """
    fullname = os.path.join(IMAGE_PATH, filename)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
