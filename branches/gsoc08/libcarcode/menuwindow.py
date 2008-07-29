import glob
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

- h  Honk
- t  Turn tracer lines
- z  Turn left blinker light
- c  Turn right blinker light

- p  Pause
- q  Quit
"""

class dlgScriptSelect(widgets.Window):
    def __init__(self, callback):
        widgets.Window.__init__(self, "Choose Car Script",  modal=True,  pos=(0, 0),  size=(450, 320),  backcolor=(0.2, 0.2, 0.2))
        self.centered = True
        self.callback = callback
        
        self.layout = widgets.Pack(orientation=widgets.HORIZONTAL, margin=3, padding=3, size=self.size)
        self.layout_buttons = widgets.Pack(margin=3, padding=5, size=(120, 10))
        
        self.lstFiles = widgets.ListBox(backcolor=self.backcolor)
        
        self.btnNew = widgets.Button(widgets.Label("New Script"))
        self.btnAdd = widgets.Button(widgets.Label("Add From File"))
        self.btnEdit = widgets.Button(widgets.Label("Edit File"))
        self.btnLoad = widgets.Button(widgets.Label("Load Selected"))
        self.btnClose = widgets.Button(widgets.Label("Close"))
        
        self.btnNew.onClick.subscribe(self.on_new)
        self.btnAdd.onClick.subscribe(self.on_add)
        self.btnEdit.onClick.subscribe(self.on_edit)
        self.btnLoad.onClick.subscribe(self.on_load)
        self.btnClose.onClick.subscribe(self.on_close)
        
        self.layout_buttons.add_entity(self.btnNew)
        self.layout_buttons.add_entity(self.btnAdd)
        self.layout_buttons.add_entity(self.btnEdit)
        self.layout_buttons.add_entity(self.btnLoad)
        self.layout_buttons.add_entity(self.btnClose)
        
        self.layout.add_entity(self.lstFiles)
        self.layout.add_entity(self.layout_buttons, expand = False)
        
        self.add_entity(self.layout)
        
    def on_new(self, btn):
        pass
    def on_add(self, btn):
        pass
    def on_edit(self, btn):
        pass
    def on_load(self, btn):
        pass
    def on_close(self, btn):
        self.parent.remove_entity(self)

class dlgLevelSelect(widgets.Window):
    def __init__(self,  callback = None):
        widgets.Window.__init__(self, "Choose Level",  modal=True,  pos=(0, 0),  size=(300, 240),  backcolor=(0.2, 0.2, 0.2))
        self.centered = True
        self.callback = callback
        self.layout = widgets.Pack(margin=3, padding=5, size=self.size)
        
        self.btnFile = widgets.Button(widgets.Label("From file"), size=(80, 24))
        self.toplayout = widgets.Pack(orientation = widgets.HORIZONTAL, size=(10, 24))
        self.toplayout.add_entity(self.btnFile, expand=False)
        self.btnFile.onClick.subscribe(self.cbFromFile)
        
        self.lstLevels = widgets.ListBox(backcolor=self.backcolor)
        self.btnOk = widgets.Button(widgets.Label("Ok"), size=(32, 32))
        
        self.btnOk.onClick.subscribe(self.cbOk)
        
        self.loader = helpers.Loader()
        lpath = self.loader.get_base_level_paths()[0]
        ll = glob.glob(os.path.join(lpath, '*.py'))
        self.flist = [os.path.basename(filename) for filename in ll]
        
        self.lstLevels.add_list(self.flist)
        
        self.layout.add_entity(self.toplayout, expand=False)
        self.layout.add_entity(self.lstLevels)
        self.layout.add_entity(self.btnOk,  expand=False)
        self.add_entity(self.layout)
        
    def cbFromFileDlg(self, filename):
        self.parent.remove_entity(self)
        if self.callback is not None:
            self.callback(filename)
    
    def cbFromFile(self, btn):
        fdialog = widgets.FileDialog("Open File", pos=(100, 100), size=(320, 240), callback=self.cbFromFileDlg)
        self.parent.add_entity(fdialog)
        
    def cbOk(self, btn):
        self.parent.remove_entity(self)
        if self.callback is not None:
            if self.lstLevels.selected >= 0:
                filename = self.flist[self.lstLevels.selected]
                filepath = self.loader.get_level_path(filename)
                print filename, filepath
            else:
                filepath = ""
            self.callback(filepath)
            
class dlgHelp(widgets.Window):
    def __init__(self):
        widgets.Window.__init__(self, "Carcode Help",  modal=True,  pos=(0, 0),  size=(350, 300),  backcolor=(0.2, 0.2, 0.2))
        self.centered = True
        self.layout = widgets.Pack(padding=10,  margin=5,  pos=(0, 0),  size=self.size)
        
        self.txtHelp = widgets.TextArea(backcolor=self.backcolor)
        self.txtHelp.readonly = True
        
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
        
        loader = helpers.Loader()
        
        self.logo = widgets.Image(loader.get_image_path("carcode.png"),  pos=(4,  4))
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
        w = dlgHelp()
        self.parent.add_entity(w)
        
    def cbLoad(self, filename):
        self.level = filename
        
    def OnLoad(self, button):
        fdialog = dlgLevelSelect(callback=self.cbLoad)
        self.parent.add_entity(fdialog)
        
    def cbScript(self, filename):
        self.script = filename
        
    def OnScript(self, button):
        #fdialog = widgets.FileDialog("Open Script", pos=(100, 100), size=(320, 240), callback=self.cbScript)
        fdialog = dlgScriptSelect(self.cbScript)
        self.parent.add_entity(fdialog)
