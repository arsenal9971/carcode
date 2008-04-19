import pygame
from pygame.locals import *

from arena import Arena

class CarcodeApp:
    ''' Carcode initialization and mainloop '''
    def __init__(self, width, height):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        
        # Initialize pygame
        pygame.init()
        
        pygame.key.set_repeat(50, 50)
        
        # Create screen surface and initialize key commands
        self.screen = pygame.display.set_mode((width, height))
        self.key_commands = {K_q: self.quit}
        
        # Create the environment
        self.arena = Arena(self, width, height)
        self.running = False
    
    def quit(self):
        self.running = False

    def add_key(self, key, func):
        self.key_commands[key] = func
    
    def main_loop(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    onRun = False
                elif event.type == KEYDOWN:
                    if self.key_commands.has_key(event.key):
                        self.key_commands[event.key]()
            self.arena.draw(self.screen)
            pygame.display.flip()
