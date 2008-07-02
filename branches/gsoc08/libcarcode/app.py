import time 
import shelve

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import OpenGL.GL

from arena import Arena
from car import Car
from sensors import Sensor, ColorSensor

import base_entities
import level_proxy
import events
from console import Console
from script import Script
from collision import BoundingBox
import widgets

        
class CarcodeApp:
    ''' Carcode initialization and mainloop '''
    def __init__(self, width, height):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        
        # Initialize pygame
        pygame.init()
        
        pygame.key.set_repeat(50, 50)
        
        pygame.display.gl_set_attribute(GL_STENCIL_SIZE, 1)
        
        # Create screen surface and initialize key commands
        self.screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
        
        glEnable (GL_BLEND) 
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluOrtho2D(0, width, height, 0);
        glMatrixMode(GL_MODELVIEW);
        
        self.key_commands = {K_q: self.quit}
        
        # Create the environment
        self.arena = Arena()
        self.running = False
        
        self.console = Console()
        
        car = Car()
        
        self.add_key(K_s, car.flip_engine)
        self.add_key(K_g, car.flip_gear)
        self.add_key(K_UP, car.accelerate)
        self.add_key(K_LEFT, car.steer_left)
        self.add_key(K_RIGHT, car.steer_right)
        self.add_key(K_DOWN, car.brake)
        self.add_key(K_h, car.honk)
        self.add_key(K_z, car.blinker_left_flip)
        self.add_key(K_c, car.blinker_right_flip)
        self.add_key(K_t, car.flip_tracer)
        self.add_key(K_p, self.pause)
		
        self.arena.set_car(car)
        self.car = car
        self.paused = False
        self.hud = widgets.HUD((width, height))
        
        self.quit_dialog = widgets.Dialog("Really quit carcode?", self.quit_app)
        
        self.init_mappings()

    def init_mappings(self):
        self.mappings = {
        'Arena': level_proxy.ArenaProxy(self.arena),
        'Carcode': level_proxy.AppProxy(self),
        'Road': base_entities.Road,
        'Box': base_entities.Box,
        'Text': base_entities.Text,
        'BoundingBox': BoundingBox,
        'Sensor': Sensor,
        'ColorSensor': ColorSensor,
        'Console': self.console,
        'widgets': widgets,
        'HUD': self.hud,
        'EventDispatcher': events.EventDispatcher
        }
        for k in OpenGL.GL.__dict__.keys():
            self.mappings[k] = OpenGL.GL.__dict__[k]

    def load_level(self, script):
        self.levelscript = Script(script, self.mappings, autoload=True)
    
    def load_script(self, script):
        self.car.set_script(Script(script, autoload=True))
		
    def pause(self):
        self.paused = not self.paused
		
    def quit_app(self, ans):
        if ans == "Yes":
            self.running = False
        else:
            self.paused = False
        
    def quit(self):
        self.paused = True
        self.hud.add_entity(self.quit_dialog)
    
    def add_key(self, key, func):
        self.key_commands[key] = func
    
    
    def main_loop(self):
        '''
            Carcode Main loop, does updating, 
            rendering and event processing.
        '''
        self.running = True
        while self.running:
            ttime = time.time()
            # Process Events
            for event in pygame.event.get():
                if self.hud.events(event):
                    break
                if event.type == QUIT:
                    # We got exit signal, we quit
                    self.quit()
                elif event.type == KEYDOWN:
                    if self.paused:
                        if event.key != K_q and event.key != K_p:
                            break
                    # Check the command dictionary and execute event
                    if self.key_commands.has_key(event.key):
                        self.key_commands[event.key]()
            # Update the Arena
            if not self.paused:
                self.arena.update()
            
            # Render
            self.arena.draw(self.screen)
            
            # Render console
            #self.console.draw()
            self.hud.draw()
            
            # Finally, flip display surface
            pygame.display.flip()
            etime = time.time()
            if (etime - ttime) < 0.05:
                time.sleep(0.05 - (etime - ttime))
