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

        
class CarcodeApp:
    ''' Carcode initialization and mainloop '''
    def __init__(self, width, height):
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        
        # Initialize pygame
        pygame.init()
        
        pygame.key.set_repeat(50, 50)
        
        # Create screen surface and initialize key commands
        self.screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluOrtho2D(0, width, height, 0);
        glMatrixMode(GL_MODELVIEW);
        
        self.key_commands = {K_q: self.quit}
        
        # Create the environment
        self.arena = Arena(self)
        self.running = False
        
        self.events = []
        self.console = Console()
        self.init_mappings()

    def init_mappings(self):
        self.mappings = {
        'Arena': level_proxy.ArenaProxy(self.arena),
        'Carcode': level_proxy.AppProxy(self),
        'Road': base_entities.Road,
        'Box': base_entities.Box,
        'Text': base_entities.Text,
        'Sensor': Sensor,
        'ColorSensor': ColorSensor,
        'Console': self.console,
        'EventDispatcher': events.EventDispatcher
        }
        for k in OpenGL.GL.__dict__.keys():
            self.mappings[k] = OpenGL.GL.__dict__[k]

    def run_script(self, script):
        fd = file(script, 'r')
        #fd.open()
        exec(fd, self.mappings)
        fd.close()
    
    def quit(self):
        self.running = False
        self.events.append((QUIT, time.time()))
        d = shelve.open("game1.test")
        d['events'] = self.events
        d.close()
    
    def add_key(self, key, func):
        self.key_commands[key] = func
    
    def rerun(self):
        d = shelve.open("game1.test")
        self.events = d['events']
        d.close()
        self.running = True
        cevent = self.events.pop(0)
        print cevent
        if cevent[0] == 0:
            itime = cevent[1]
        else:
            print 'Malformed event log'
            return 0
        ntime = time.time() + (cevent[1] - itime)
        while self.running:
            ctime = time.time()
            if ctime >= ntime:
                if cevent[0] == KEYDOWN:
                    eventkey = cevent[2]
                    if self.key_commands.has_key(eventkey):
                        self.key_commands[eventkey]()
                elif cevent[0] == QUIT:
                    return 0
                cevent = self.events.pop(0)
                ntime = ctime + (cevent[1] - itime)
                itime = cevent[1]
            self.arena.update()
            self.arena.draw(self.screen)
            pygame.display.flip()
            etime = time.time()
            if (etime - ctime) < 0.05:
                time.sleep(0.05 - (etime - ctime))
    
    def main_loop(self):
        '''
            Carcode Main loop, does updating, 
            rendering and event processing.
        '''
        self.running = True
        self.events.append((0, time.time()))
        while self.running:
            ttime = time.time()
            # Process Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    # We got exit signal, we quit
                    self.quit()
                elif event.type == KEYDOWN:
                    # Check the command dictionary and execute event
                    if self.key_commands.has_key(event.key):
                        self.events.append((KEYDOWN, time.time(), event.key))
                        self.key_commands[event.key]()
            # Update the Arena
            self.arena.update()
            
            # Render
            self.arena.draw(self.screen)
            
            # Render console
            self.console.draw()
            
            # Finally, flip display surface
            pygame.display.flip()
            etime = time.time()
            if (etime - ttime) < 0.05:
                time.sleep(0.05 - (etime - ttime))
