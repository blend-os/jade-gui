# installer_Screen.py

#
# Copyright 2022 user

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess, os, sys, shutil
import asyncio
from gi.repository import Gtk, GLib, Adw, Vte, Pango
from gettext import gettext as _
from jade_gui.utils.command import CommandUtils
from jade_gui.classes.jade_screen import JadeScreen
import time


@Gtk.Template(resource_path="/al/getcryst/jadegui/pages/install_screen.ui")
class InstallScreen(JadeScreen, Adw.Bin):
    __gtype_name__ = "InstallScreen"

    log_box = Gtk.Template.Child()

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window

        # Vte instance
        self.vte_instance = Vte.Terminal()
        self.vte_instance.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.vte_instance.set_mouse_autohide(True)
        self.vte_instance.set_font(Pango.FontDescription("Source Code Pro Regular 12"))
        self.log_box.append(self.vte_instance)
        self.vte_instance.connect("child-exited", self.on_vte_child_exited)

        self.set_valid(False)

    def on_show(self):
        prefs = self.window.summary_screen.installprefs.generate_json()
        with open(os.getenv("HOME") + "/.config/jade.json", "w") as f:
            f.write(prefs)

        prefs = self.window.summary_screen.installprefs.generate_json()

        self.vte_instance.spawn_async(
            Vte.PtyFlags.DEFAULT,
            ".",  # working directory
            ["bash", "/usr/share/jade-gui/jade_gui/scripts/install.sh"],
            [],  # environment
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None,
        )

        self.window.connect('close-request', self.confirm_quit)

    def confirm_quit(self, *_):
        dialog = Adw.MessageDialog.new(
            self.window,
            'Close',
        )
        dialog.set_body("Closing the blendOS installer during installation isn't supported.")
        dialog.add_response("okay", "Ok")
        dialog.set_default_response("okay")
        dialog.set_close_response("okay")

        def response(dialog, answer):
            dialog.destroy()

        dialog.connect("response", response)
        dialog.show()

        try:
            self.window.install_success
            return False
        except:
            return True

    def on_vte_child_exited(self, terminal, status):
        self.set_valid(True)
        
        if status == 0:
            self.window.install_success = True
        else:
            self.window.install_success = False
