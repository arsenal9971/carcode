import os
import helpers
import widgets
VERSION = "3.0 Beta 1"

help_text = """Keyboard Controls

Arrows:
  - Up:    Accelerate
  - Down:  Brake
  - Left:  Steer car left
  - Right: Steer car right

- s  Start/stop engine
- g  Change gears (forward/reverse)

- q  Quit
"""

class winHelp(widgets.Window):
    def __init__(self):
        widgets.Window.__init__(self, "Carcode Help",  modal=True,  pos=(0, 0),  size=(300, 400),  backcolor=(0.2, 0.2, 0.2))
        self.centered = True
        self.layout = widgets.Pack(padding=10,  margins=5,  pos=(0, 0),  size=self.size)
        
        self.txtHelp = widgets.TextArea(backcolor=self.backcolor)
        self.btnClose = widgets.Button(widgets.Label("Close"),  size=(32,  32))
        self.btnClose.onClick.subscribe(self.cbClose)
        
        self.layout.add_entity(self.txtHelp)
        self.layout.add_entity(self.btnClose, expand=False)
        self.add_entity(self.layout)
        
        self.txtHelp.set_text(help_text)
        
    def cbClose(self, btn):
        self.visible = False
        self.parent.remove_entity(self)
        
class MainWindow(widgets.Window):
    def __init__(self):
        widgets.Window.__init__(self, "Carcode", pos=(0,0), size=(300, 330), backcolor=(0.2,0.2,0.2, 0.5))
        self.centered = True
        
        self.logo = widgets.Image(os.path.join(helpers.IMAGE_PATH,  "carcode.png"),  pos=(4,  4))
        self.version = widgets.Label("Version: " + VERSION,  pos=(4,  self.logo.size[1] + 4))
        
        self.btnQuit = widgets.Button(widgets.Label("Quit"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnLoad = widgets.Button(widgets.Label("Load Level"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnScript = widgets.Button(widgets.Label("Load Car Script"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnStart = widgets.Button(widgets.Label("Play"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        self.btnHelp = widgets.Button(widgets.Label("Help"), (0,0), (10,10), backcolor=(0.2,0.2,0.2))
        
        self.btnHelp.onClick.subscribe(self.cbHelp)
        self.btnLoad.onClick.subscribe(self.OnLoad)
        self.btnScript.onClick.subscribe(self.OnScript)
        
        self.vp = widgets.Pack(orientation = widgets.VERTICAL,   padding=5, margin=10,  pos=(0,self.logo.size[1] + 25), size=(300, 180))
        
        self.add_entity(self.logo)
        self.add_entity(self.version)
        
        self.vp.add_entity(self.btnStart)
        self.vp.add_entity(self.btnLoad)
        self.vp.add_entity(self.btnScript)
        self.vp.add_entity(self.btnHelp)
        self.vp.add_entity(self.btnQuit)
        
        self.add_entity(self.vp)
        self.modal = True
        self.level = ""
        self.script = ""
        
    def cbHelp(self,  btn):
        w = winHelp()
        self.parent.add_entity(w)
        
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
