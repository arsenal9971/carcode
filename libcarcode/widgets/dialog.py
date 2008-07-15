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
        label = Label(label, pos=(10,10))
        height = 65
        width = label.size[0] + 20
        bWidth = (width / 2) - 10
        
        self.btnYes = Button(Label("Yes"), (5, 35), (bWidth, 20), backcolor=(0.2,0.2,0.2))
        self.btnNo = Button(Label("No"), (bWidth + 15, 35), (bWidth, 20), backcolor=(0.2,0.2,0.2))
        self.btnYes.onClick.subscribe(self.answared)
        self.btnNo.onClick.subscribe(self.answared)
        
        self.callback = callback
        
        posX = 400 - (width /2)
        posY = 300 - (height /2)
        
        Window.__init__(self, "Dialog", pos=(posX, posY), size=(width, height), backcolor=(0.5,0.5,0.5,0.8))
        
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
