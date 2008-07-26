import os
import sys
import time 

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutInit

import OpenGL.GL

from arena import Arena
from car import Car
from sensors import Sensor, ColorSensor

import base_entities
import level_proxy
import events
from script import Script
from collision import BoundingBox
import widgets
from physics import PhysicsEngine
import physics
import helpers
from scoreboard import Scoreboard

VERSION = "3.0 Beta 1"

class MainWindow(widgets.Window):
    def __init__(self):
        widgets.Window.__init__(self, "Carcode", pos=(0,0), size=(300, 330), backcolor=(0.2,0.2,0.2, 0.5))
        self.centered = True
        
        self.logo = widgets.Image(os.path.join(helpers.IMAGE_PATH,  "carcode.png"),  pos=(4,  4))
        self.version = widgets.Label("Version: " + VERSION,  pos=(4,  self.logo.size[1] + 4))
        
        self.btnQuit = widgets.Button(widgets.Label("Quit"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnLoad = widgets.Button(widgets.Label("Load Level"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnScript = widgets.Button(widgets.Label("Load Car Script"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnStart = widgets.Button(widgets.Label("Start Carcode"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        
        self.btnLoad.onClick.subscribe(self.OnLoad)
        self.btnScript.onClick.subscribe(self.OnScript)
        
        self.vp = widgets.Pack(orientation = widgets.VERTICAL,   padding=5, margin=10,  pos=(0,self.logo.size[1] + 25), size=(300, 180))
        
        self.add_entity(self.logo)
        self.add_entity(self.version)
        
        self.vp.add_entity(self.btnStart)
        self.vp.add_entity(self.btnLoad)
        self.vp.add_entity(self.btnScript)
        self.vp.add_entity(self.btnQuit)
        
        self.add_entity(self.vp)
        self.modal = True
        self.level = ""
        self.script = ""
        
    def cbLoad(self, filename):
        self.level = filename
        
    def OnLoad(self, button):
        fdialog = widgets.FileDialog("Open Level", pos=(100, 100), size=(320, 240), callback=self.cbLoad)
        self.parent.add_entity(fdialog)
        
    def cbScript(self, filename):
        self.script = filename
        
    def OnScript(self, button):
        fdialog = widgets.FileDialog("Open Script", pos=(100, 100), size=(320, 240), callback=self.cbScript)
        self.parent.add_entity(fdialog)

class GoalWindow(widgets.Window):
    def __init__(self):
        widgets.Window.__init__(self,  "Objectives", pos=(2, 2 ),  size=(240,  100),  backcolor=(0.2, 0.2, 0.2,  0.5))
        self.layout = widgets.Pack(pos=(0, 0),  size=(240, 100),  margin=3)
        self.add_entity(self.layout)
        self.goals = {}
    
    def events(self,  event):
        return False
        
    def update_goals(self, goal,  val,  state):
        self.goals[goal].checked = val
        
    def set_goals(self,  goals):
        if type(goals) != type([]):
            self.set_goals(goals.goals)
        else:
            for goal in goals:
                self.goals[goal] = widgets.Checkbox(goal.desc,  pos=(0, 0),  size=(13, 13),)
                goal.onTest.subscribe(self.update_goals)
                self.layout.add_entity(self.goals[goal],  expand=False)
        
class CarcodeApp:
    ''' Carcode initialization and mainloop '''
    def __init__(self, width, height):
        """ CarcodeApp
        
        @param width app window width
        @param height app window height
        """
        
        if not pygame.font: print 'Warning, fonts disabled'
        if not pygame.mixer: print 'Warning, sound disabled'
        
        # Initialize pygame
        pygame.init()
        
        pygame.key.set_repeat(200, 50)
        
        pygame.display.gl_set_attribute(GL_STENCIL_SIZE, 1)
        
        # Create screen surface and initialize key commands
        self.screen = pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
        
        #Initialize GLUT, requiered in some platforms
        glutInit([])
        
        pygame.display.set_caption("Carcode " + VERSION)
        
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
        self.pe = PhysicsEngine()
        self.arena = Arena(self.pe)
        self.running = False
        
        self.msgWindow = widgets.Window("Messages",  pos=(3, 3),  size=(260,  60),  backcolor=(0.2,  0.2,  0.2,  0.4))
        self.msgWindow.visible = False
        self.console = widgets.Console((0,  0),  (260,  40),  3)
        self.msgWindow.add_entity(self.console)
        
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
        self.paused = True
        self.hud = widgets.HUD((width, height))
        
        self.winScoreboard = Scoreboard(lambda : self.quit_app("Yes"))
        
        self.quit_dialog = widgets.Dialog("Really quit carcode?", self.quit_app)
        
        self.mw = MainWindow()
        self.mw.btnQuit.onClick.subscribe(self.quit)
        self.mw.btnStart.onClick.subscribe(self.start)
        self.hud.add_entity(self.winScoreboard)
        self.hud.add_entity(self.mw)
        self.hud.add_entity(self.msgWindow)
        
        self.goalWindow = GoalWindow()
        self.goalWindow.visible = False
        self.hud.add_entity(self.goalWindow)
        
        self.init_mappings()
        self.state = 0
        self.condition = None
        self.scoreboard = []
        self.levelscript = None
        self.game_time = 0.0
        
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
        'ccEntity': physics.ccEntity, 
        'BoxGeometry': physics.BoxGeometry, 
        'EventDispatcher': widgets.EventDispatcher, 
        'AND': events.AND, 
        'OR': events.OR, 
        'Goal': events.Goal, 
        'Chain': events.Chain, 
        'Score': events.Score
        }
        for k in OpenGL.GL.__dict__.keys():
            self.mappings[k] = OpenGL.GL.__dict__[k]

    def load_level(self, script):
        """ Load a level script file
        
        @param script filename of the script
        """
        lscode = Script(script, self.mappings, autoload=True)
        ls = lscode.get("LevelScript")
        self.levelscript = ls()
    
    def load_script(self, script):
        """ Load a car script file
        
        @param script filename of the script
        """
        
        self.car.carscript = Script(script, autoload=True)
        CarScript =  self.car.carscript.get("CarScript")
        
        self.car.attach_script(CarScript(self.car))
		
    def start(self, button):
        if self.mw.level:
            self.load_level(self.mw.level)
        if self.mw.script:
            self.load_script(self.mw.script)
        self.hud.remove_entity(self.mw)
        #self.msgWindow.visible = True
        self.goalWindow.visible = True
        self.paused = False
        
    def pause(self):
        self.paused = not self.paused
		
    def quit_app(self, ans):
        if ans == "Yes":
            self.running = False
        else:
            self.paused = False
        
    def quit(self, obj = None):
        self.paused = True
        self.mw.modal = False
        self.hud.add_entity(self.quit_dialog)
    
    def add_key(self, key, func):
        self.key_commands[key] = func
    
    def main_loop(self):
        '''
            Carcode Main loop, does updating, 
            rendering and event processing.
        '''
        self.running = True
        
        ltime = time.time()
        ttime = ltime + 0.05
        
        while self.running:
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
            # Render
            #self.arena.draw(self.screen)
            
            # Render console
            #self.console.draw()
            #self.hud.draw()
            
            # Finally, flip display surface
            #pygame.display.flip()
            
            etime = time.time()
            
            # Try to keep update code running
            # at 24fps without sleeping, we lose
            # events when sleeping.
            if etime >= ttime:
                # Update the Arena
                if not self.paused:
                    self.game_time +=  etime-ltime 
                    ltime = time.time()
                    
                    self.arena.update()
                    self.pe.update()
                    
                    if self.levelscript:
                        self.levelscript.update()
                        
                    if self.condition is not None:
                        condition,  self.state = self.condition.test()
                        if condition:
                            self.paused = True
                            self.console.clear()
                            self.console.write("Task completed!")
                            self.winScoreboard.show_scoring(self.scoreboard)
                    
                # Render
                self.arena.draw(self.screen)
            
                # Render console
                #self.console.draw()
                self.hud.draw()
            
                # Finally, flip display surface
                pygame.display.flip()
                
                ttime = time.time() + 0.05
