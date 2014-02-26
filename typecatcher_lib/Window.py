# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Andrew Starr-Bochicchio <a.starr.b@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

### DO NOT EDIT THIS FILE ###

from gi.repository import Gtk # pylint: disable=E0611
import logging
import subprocess
logger = logging.getLogger('typecatcher_lib')

from . helpers import get_builder, show_uri, get_help_uri

# This class is meant to be subclassed by TypeCatcherWindow.  It provides
# common functions and some boilerplate.
class Window(Gtk.ApplicationWindow):
    __gtype_name__ = "Window"

    # To construct a new instance of this method, the following notable 
    # methods are called in this order:
    # __new__(cls)
    # __init__(self)
    # finish_initializing(self, builder)
    # __init__(self)
    #
    # For this reason, it's recommended you leave __init__ empty and put
    # your initialization code in finish_initializing
    
    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated BaseTypeCatcherWindow object.
        """
        builder = get_builder('TypeCatcherWindow')
        new_object = builder.get_object("typecatcher_window")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initializing should be called after parsing the UI definition
        and creating a TypeCatcherWindow object with it in order to finish
        initializing the start of the new TypeCatcherWindow instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)
        self.PreferencesDialog = None # class
        self.preferences_dialog = None # instance
        self.AboutDialog = None # class

    def on_mnu_contents_activate(self, widget, data=None):
        show_uri(self, "help:%s" % get_help_uri())

    def on_mnu_about_activate(self, widget, data=None):
        """Display the about box for typecatcher."""
        if self.AboutDialog is not None:
            about = self.AboutDialog() # pylint: disable=E1102
            response = about.run()
            about.destroy()

    def on_mnu_close_activate(self, widget, data=None):
        """Signal handler for closing the TypeCatcherWindow."""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """Called when the TypeCatcherWindow is closed."""
        # Clean up code for saving application state should be added here.
        pass

    def on_mnu_report_activate(self, button):
        try: # Use apport if we can.
            subprocess.Popen(['ubuntu-bug', 'typecatcher'])
        except OSError: # If not, just open a browser.
            bug_url = "https://bugs.launchpad.net/typecatcher/+filebug"
            Gtk.show_uri(None, bug_url, 0)

    def on_mnu_trans_activate(self, button):
        bug_url = "https://translations.launchpad.net/typecatcher"
        Gtk.show_uri(None, bug_url, 0)

    def info_dialog(self, head, message):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   head)
        dialog.format_secondary_text(message)
        dialog.set_modal(True)
        dialog.run()
        dialog.destroy()