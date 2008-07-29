import widgets

class Editor(widgets.Window):
    def __init__(self, filename="", callback=None):
        widgets.Window.__init__(self, "Editor: %s" % filename, size=(700, 500), backcolor=(0.2,0.2,0.2))
        self.centered = True
        self.callback = callback
        self.filename = filename
        
        self.layout = widgets.Pack(size=self.size, margin=3, padding=4)
        self.layout_menu = widgets.Pack(widgets.HORIZONTAL, margin=3, padding=5, size=(32, 32))
        
        self.txtEditor = widgets.TextArea()
        
        if filename:
            try:
                fd = file(filename, 'r')
                self.txtEditor.set_text(fd.read())
            except:
                pass
        
        self.btnSave = widgets.Button(widgets.Label("Save"))
        self.btnClose = widgets.Button(widgets.Label("Close"))
        
        self.btnClose.onClick.subscribe(self.cbClose)
        
        self.layout_menu.add_entity(self.btnSave)
        self.layout_menu.add_entity(self.btnClose)
        
        self.layout.add_entity(self.layout_menu, expand=False)
        self.layout.add_entity(self.txtEditor)
        
        self.add_entity(self.layout)
        
    def cbClose(self, btn):
        self.parent.remove_entity(self)