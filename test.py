# -*- coding: utf-8 -*-

from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Gedit
import time

timeDelay = 5
timeoutDelay = 500

class SelectWrittingMode(GObject.Object, Gedit.AppActivatable):

    app = GObject.Property(type=Gedit.App)
    
    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        self.menu_item = self.extend_menu("tools-section")
        menu_item = Gio.MenuItem.new(_("Productive Writting Mode"), "win.writting")
        self.menu_item.prepend_menu_item(menu_item)

class OpenWrittingMode(GObject.Object, Gedit.WindowActivatable):

    window = GObject.Property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        self.time = None
        self.timer = None
        
    def updateTime(self, data=None):
        self.time = time.time()
        
    def do_activate(self):
        action = Gio.SimpleAction(name="writting")
        action.connect('activate', self.startWrittingMode)
        self.window.add_action(action)
        
    def startWrittingMode(self, action, argument, data=None):
        self.document = self.window.get_active_document()
        self.document.connect("cursor-moved", self.updateTime)
        self.time = time.time()
        self.timer = GObject.timeout_add(timeoutDelay, self.checkIfTime)
        
    def checkIfTime(self, data=None):
        if self.time + timeDelay < time.time():
            self.deleteLastCharacter()
        return True

    def deleteLastCharacter(self):
        time = self.time
        start = self.document.get_end_iter()
        end = start.copy()
        end.backward_char()
        self.document.delete(start, end)
        self.time = time
