import os
import glob

from OpenGL.GL import *
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13

from pygame.locals import *

from button import Button
from constants import *
from events import EventDispatcher
from label import Label
from listbox import ListBox
from window import Window

class FileDialog(Window):
    def __init__(self, title, pos, size, callback, match="*"):
        Window.__init__(self, title, pos, size, (0.2,0.2,0.2))
        self.modal = True
        self.callback = callback
        self.cwd = os.getcwd()
        self.match = match
        self.flist = ListBox((5,5), (size[0]-10, size[1]-50), (0.2,0.2,0.2))
        btnW = (self.size[0] / 2) - 30
        btnX = (self.size[0] / 4) - (btnW /2)
        self.btnCancel = Button(Label("Cancel"),(btnX, size[1]-40), (btnW, 30), (0.5,0.5,0.5))
        btnX = (self.size[0] / 2) + (self.size[0] / 4) - (btnW /2)
        self.btnOk = Button(Label("Ok"),(btnX, size[1]-40), (btnW, 30), (0.5,0.5,0.5))
        
        self.add_entity(self.flist)
        self.add_entity(self.btnCancel)
        self.add_entity(self.btnOk)
        
        self.file_list = []
        self.update()
        self.flist.onSelected.subscribe(self.Select)
        self.filename = ""
        self.btnOk.onClick.subscribe(self.btnClick)
        self.btnCancel.onClick.subscribe(self.btnClick)
    
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
    def get_filelist(self):
        try:
            files = glob.iglob(os.path.join(self.cwd, '*'))
        except:
            files = glob.glob(os.path.join(self.cwd, '*'))
        self.file_list = []
        dirs = []
        sfiles = []
        for fullpath in files:
            fname = os.path.split(fullpath)[1]
            if os.path.isdir(fullpath):
                dirs.append((fname, fullpath, True))
            else:
                sfiles.append((fname, fullpath, False))
        def pcmp(x, y):
            a = x[0]
            b = y[0]
            if a == b:
                return 0
            if a > b:
                return 1
            return -1
        dirs.sort(pcmp)
        sfiles.sort(pcmp)
        self.file_list = dirs + sfiles
        if os.path.split(self.cwd)[1] != '':
            self.file_list.insert(0, ("..", os.path.split(self.cwd)[0], True))
            
    def update(self):
        self.get_filelist()
        fl = [fname[0] for fname in self.file_list]
        self.flist.empty()
        self.flist.add_list(fl)