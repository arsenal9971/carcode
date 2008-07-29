import os
import glob

from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from button import Button
from constants import *
from events import EventDispatcher
from label import Label
from layout import Pack
from listbox import ListBox
from textbox import TextBox
from window import Window

class FileSaveDialog(Window):
    """Simple file dialog for navigating filesystem and saving files"""
    
    def __init__(self, title,  callback, match="*",  *args,  **kargs):
        """FileDialog
        
            @param title string with dialog title
            @param callback callable to be used when user finishes
            @param match filename filter
            @param pos tuple with dialog position (x, y)
            @param size tuple with dialog size (width, height)
        """
        Window.__init__(self, title, *args,  **kargs)
        self.modal = True
        self.centered = True
        self.callback = callback
        self.cwd = os.getcwd()
        self.match = match
        self.filename = ""
        self.file_list = []
        
        self.layout = Pack(margin=3, padding=5, size=self.size)
        self.layout_buttons = Pack(orientation = HORIZONTAL, padding=20, margin=5, size=(10,  35))
        self.layout_filename = Pack(orientation = HORIZONTAL, padding=20, margin=5, size=(10,  35))
        
        self.flist = ListBox((5,5), (self.size[0]-10, self.size[1]-50), backcolor=(0.2,0.2,0.2))
        
        self.lblFilename = Label("Filename:")
        self.txtFilename = TextBox()
        
        self.layout_filename.add_entity(self.lblFilename, expand=False)
        self.layout_filename.add_entity(self.txtFilename)
        
        self.btnCancel = Button(Label("Cancel"),(0, 0), (10, 10), backcolor=(0.5,0.5,0.5))
        self.btnOk = Button(Label("Ok"),(0, 0), (10, 10), backcolor=(0.5,0.5,0.5))
        
        self.flist.onSelected.subscribe(self.Select)
        self.btnOk.onClick.subscribe(self.btnClick)
        self.btnCancel.onClick.subscribe(self.btnClick)
        
        self.layout_buttons.add_entity(self.btnCancel)
        self.layout_buttons.add_entity(self.btnOk)
        
        self.layout.add_entity(self.flist)
        self.layout.add_entity(self.layout_filename, expand = False)
        self.layout.add_entity(self.layout_buttons, expand = False)
        self.add_entity(self.layout)
        
        self.update()
    
    def btnClick(self, btn):
        self.parent.remove_entity(self)
        if btn == self.btnCancel:
            self.callback("")
        else:
            filename = self.txtFilename.get_text()
            if filename:
                fullpath = os.path.join(self.cwd, filename)
            else:
                fullpath = ""
            self.callback(fullpath)
        
    def Select(self, obj):
        if self.file_list[self.flist.selected][2]:
            self.cwd = self.file_list[self.flist.selected][1]
            self.update()
            self.filename = ""
            self.txtFilename.set_text("")
        else:
            self.filename = self.file_list[self.flist.selected][1]
            self.txtFilename.set_text(os.path.basename(self.filename))
            
    # TODO: Add windows specific drive list
    def get_filelist(self):
        # Try to get glob as iterator, if not available as a list
        try:
            files = glob.iglob(os.path.join(self.cwd, '*'))
        except:
            files = glob.glob(os.path.join(self.cwd, '*'))
            
        self.file_list = []
        dirs = []
        sfiles = []
        
        # Iterate glob and separate files from directories
        for fullpath in files:
            fname = os.path.split(fullpath)[1]
            if os.path.isdir(fullpath):
                dirs.append((fname, fullpath, True))
            else:
                sfiles.append((fname, fullpath, False))
                
        # Touple aware comparision function for list sorting
        def pcmp(x, y):
            a = x[0]
            b = y[0]
            if a == b:
                return 0
            if a > b:
                return 1
            return -1
        
        # Sort filenames
        dirs.sort(pcmp)
        sfiles.sort(pcmp)
        
        # Add directories first then files
        self.file_list = dirs + sfiles
        
        # If we aren't on root directory add parent directory as double dot (..)
        if os.path.split(self.cwd)[1] != '':
            self.file_list.insert(0, ("..", os.path.split(self.cwd)[0], True))
            
    def update(self):
        self.get_filelist()
        fl = [fname[0] for fname in self.file_list]
        self.flist.empty()
        self.flist.add_list(fl)

        
class FileOpenDialog(Window):
    """Simple file dialog for navigating filesystem and choosing files"""
    
    def __init__(self, title,  callback, match="*",  *args,  **kargs):
        """FileDialog
        
            @param title string with dialog title
            @param callback callable to be used when user finishes
            @param match filename filter
            @param pos tuple with dialog position (x, y)
            @param size tuple with dialog size (width, height)
        """
        Window.__init__(self, title, *args,  **kargs)
        self.modal = True
        self.centered = True
        self.callback = callback
        self.cwd = os.getcwd()
        self.match = match
        
        self.filename = ""
        self.file_list = []
        
        self.flist = ListBox((5,5), (self.size[0]-10, self.size[1]-50), backcolor=(0.2,0.2,0.2))
        
        self.btnCancel = Button(Label("Cancel"),(0, 0), (10, 10), backcolor=(0.5,0.5,0.5))
        self.btnOk = Button(Label("Ok"),(0, 0), (10, 10), backcolor=(0.5,0.5,0.5))
        
        self.flist.onSelected.subscribe(self.Select)
        self.btnOk.onClick.subscribe(self.btnClick)
        self.btnCancel.onClick.subscribe(self.btnClick)
        
        self.btnPack = Pack(orientation= HORIZONTAL,  padding=20, margin=5,  pos=(0,  self.size[1]-40),  size=(self.size[0],  35))
        self.btnPack.add_entity(self.btnCancel)
        self.btnPack.add_entity(self.btnOk)
        
        self.add_entity(self.flist)
        self.add_entity(self.btnPack)
        
        self.update()
    
    def btnClick(self, btn):
        if btn == self.btnCancel:
            self.callback("")
        else:
            self.callback(self.filename)
        self.parent.remove_entity(self)
        
    def Select(self, obj):
        if self.file_list[self.flist.selected][2]:
            self.cwd = self.file_list[self.flist.selected][1]
            self.update()
            self.filename = ""
        else:
            self.filename = self.file_list[self.flist.selected][1]
            
    # TODO: Add windows specific drive list
    def get_filelist(self):
        # Try to get glob as iterator, if not available as a list
        try:
            files = glob.iglob(os.path.join(self.cwd, '*'))
        except:
            files = glob.glob(os.path.join(self.cwd, '*'))
            
        self.file_list = []
        dirs = []
        sfiles = []
        
        # Iterate glob and separate files from directories
        for fullpath in files:
            fname = os.path.split(fullpath)[1]
            if os.path.isdir(fullpath):
                dirs.append((fname, fullpath, True))
            else:
                sfiles.append((fname, fullpath, False))
                
        # Touple aware comparision function for list sorting
        def pcmp(x, y):
            a = x[0]
            b = y[0]
            if a == b:
                return 0
            if a > b:
                return 1
            return -1
        
        # Sort filenames
        dirs.sort(pcmp)
        sfiles.sort(pcmp)
        
        # Add directories first then files
        self.file_list = dirs + sfiles
        
        # If we aren't on root directory add parent directory as double dot (..)
        if os.path.split(self.cwd)[1] != '':
            self.file_list.insert(0, ("..", os.path.split(self.cwd)[0], True))
            
    def update(self):
        self.get_filelist()
        fl = [fname[0] for fname in self.file_list]
        self.flist.empty()
        self.flist.add_list(fl)
