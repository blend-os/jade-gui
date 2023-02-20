# desktop_screen.py

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


import subprocess, shutil
from gi.repository import Gtk, Adw, GtkSource, Gdk
from gettext import gettext as _
from jade_gui.utils.command import CommandUtils
from jade_gui.classes.jade_screen import JadeScreen


class LogWindow(Adw.Window):
    def __init__(self, window, title, content, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.title = title
        self.content = content
        self.create_window()
        self.set_default_size(700, 700)

    def create_window(self):
        headerbar = Gtk.HeaderBar()
        copy_button = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scrolled_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        style_scheme_manager = GtkSource.StyleSchemeManager.get_default()
        text_buffer = GtkSource.Buffer(
            highlight_syntax=False,
            style_scheme=style_scheme_manager.get_scheme("oblivion"),
        )
        text_view = GtkSource.View(
            buffer=text_buffer, show_line_numbers=True, monospace=True
        )
        text_buffer = text_view.get_buffer()
        headerbar.set_title_widget(Gtk.Label.new(self.title))
        headerbar.pack_end(copy_button)
        buffer_iter = text_buffer.get_end_iter()
        text_buffer.insert(buffer_iter, self.content)
        scrolled_view.set_child(text_view)
        contentbox.append(headerbar)
        contentbox.append(scrolled_view)
        self.set_content(contentbox)
        copy_button.connect("clicked", self.copy_content)

    def copy_content(self, widget):
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set_content(Gdk.ContentProvider.new_for_value(self.content))


@Gtk.Template(resource_path="/al/getcryst/jadegui/pages/finished_screen.ui")
class FinishedScreen(JadeScreen, Adw.Bin):
    __gtype_name__ = "FinishedScreen"

    reboot_button = Gtk.Template.Child()
    output_button = Gtk.Template.Child()

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.reboot_button.connect("clicked", self.reboot)
        self.output_button.connect("clicked", self.output)

        self.set_valid(True)

    def reboot(self, widget):
        CommandUtils.run_command(["gnome-session-quit", "--reboot"])

    def output(self, widget):
        with open("/tmp/jade-gui-output.txt", "r") as f:
            output = f.read()
        LogWindow(window=self.window, title="Jade log view", content=output).present()
