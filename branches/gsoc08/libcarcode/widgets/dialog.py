from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from button import Button
from constants import *
from events import EventDispatcher
from label import Label
from window import Window

class Dialog(Window):
    def __init__(self, label, callback):
        height = 80
        width = 180
        label = Label(label, (0, 17), COLOR_WHITE)
        self.btnYes = Button("Yes", (15, 35), (60, 20), (0.2,0.2,0.2))
        self.btnNo = Button("No", (95, 35), (60, 20), (0.2,0.2,0.2))
        self.btnYes.onClick.subscribe(self.answared)
        self.btnNo.onClick.subscribe(self.answared)
        
        self.callback = callback
        Window.__init__(self, "Dialog", (270, 220), (width, height), (0.5,0.5,0.5,0.5))
        self.modal = True
        self.add_entity(label)
        self.add_entity(self.btnYes)
        self.add_entity(self.btnNo)
            
    def answared(self, button):
        if button == self.btnYes:
            self.callback("Yes")
        else:
            self.callback("No")
        self.parent.remove_entity(self)