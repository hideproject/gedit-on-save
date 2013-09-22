# Copyright (c) 2013 Jan Pecha (http://janpecha.iunas.cz/) All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this
#   list of conditions and the following disclaimer in the documentation and/or
#   other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from gi.repository import GObject, Gtk, Gedit
import re
import subprocess
import json
import types
import fnmatch
import os
import pipes
from glob import glob

class GeditOnSaveGlobal:
    windowObject = 0


class GeditOnSavePlugin(GObject.Object, Gedit.ViewActivatable):
    """Run command after save document"""

    __gtype_name__ = "GeditOnSavePlugin"
    view = GObject.property(type=Gedit.View)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        """Activate plugin."""
        self.doc = self.view.get_buffer()
        self.setting = {}
        
        filepaths = glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '*.json'))
        for filepath in filepaths:
            try:
                f = open(filepath)
                self.setting = self.merge(self.setting, json.load(f))
                f.close()
            except IOError:
                pass
        
        self.handler_id = self.doc.connect("saved", self.on_document_saving)

    def do_deactivate(self):
        """Deactivate plugin."""
        self.doc.disconnect(self.handler_id)

    def do_update_state(self):
        """Window state updated"""
        pass

    def merge(self, x, y):
        # Link: http://stackoverflow.com/questions/9730648/merge-a-nested-dictionary-default-values
        
        # store a copy of x, but overwrite with y's values where applicable
        merged = dict(x,**y)
        
        xkeys = x.keys()
        
        # if the value of merged[key] was overwritten with y[key]'s value
        # then we need to put back any missing x[key] values
        for key in xkeys:
            # if this key is a dictionary, recurse
            if type(x[key]) is types.DictType and y.has_key(key):
                merged[key] = self.merge(x[key],y[key])
        
        return merged

    def on_document_saving(self, *args):
        """On document saving handler"""
        lang = self.doc.get_language().get_name()
        path = self.doc.get_location().get_path()
        
        for mask, cmds in self.setting.items():
            if fnmatch.fnmatch(path, mask):
                for cmd in cmds:
                    if cmd.has_key("cmd"):
                        if cmd.has_key("active") and cmd["active"] != "no":
                            self.run_command(cmd["cmd"], path, lang)

    def run_command(self, command, path, lang):
        cmdline = command.replace("%file%", "'" + pipes.quote(path) + "'").replace("%lang%", "'" + pipes.quote(lang) + "'")
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
        output, errors = p.communicate()
        
        if p.returncode:
            errorMsg = errors
            if not errors:
            	errorMsg = output
            
            #pos = errors.find('on line')
            
#            if pos != -1:
#                # extract error message
#                errorMsg = errors[0:(pos-1)].strip()
#                
#                # extract line number
#                pos = pos + 8
#                lineNum = ""
#                errors = errors[pos:]
#                
#                for letter in errors:
#                    if letter.isdigit():
#                        lineNum += letter
#                    else:
#                        break
#                
#                lineNum = int(float(lineNum))
#                
#                # select error line
#                self.doc.goto_line(lineNum)
#                self.view.scroll_to_cursor()
            if GeditOnSaveGlobal.windowObject != 0:
                GeditOnSaveGlobal.windowObject.setPanelErrorMessage(errorMsg)
        else:
            if GeditOnSaveGlobal.windowObject != 0:
                GeditOnSaveGlobal.windowObject.setPanelNoErrors()

class GeditOnSaveWindowPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GeditOnSaveWindowPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        icon = Gtk.Image.new_from_stock(Gtk.STOCK_DIALOG_ERROR, Gtk.IconSize.MENU)
        self.textBuffer = Gtk.TextBuffer()
        self._bottom_widget = Gtk.TextView()
        self._bottom_widget.set_buffer(self.textBuffer)
        #self.textBuffer = self._bottom_widget.get_buffer()
        self._bottom_widget.set_editable(False)
        self._bottom_widget.show()
        
        self.scrolledWindow = Gtk.ScrolledWindow()
        self.scrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC) # TODO: NEVER
        self.scrolledWindow.add_with_viewport(self._bottom_widget)
        
        panel = self.window.get_bottom_panel()
        panel.add_item(self.scrolledWindow, "GeditOnSaveBottomPanel", "On save", icon)
        panel.activate_item(self.scrolledWindow)
        
        self.setPanelNoErrors();
        
        GeditOnSaveGlobal.windowObject = self

    def do_deactivate(self):
        panel = self.window.get_bottom_panel()
        panel.remove_item(self.scrolledWindow)

    def do_update_state(self):
        pass

    def setPanelErrorMessage(self, msg):
        panel = self.window.get_bottom_panel()
        self.textBuffer.set_text(msg)
        panel.activate_item(self.scrolledWindow)
        panel.show()

    def setPanelNoErrors(self):
        self.textBuffer.set_text('No problems.')
        # TODO: panel.hide()

