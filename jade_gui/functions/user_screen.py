# user_screen.py

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


from gi.repository import Gtk, Adw
from gettext import gettext as _
import re, subprocess, shutil
from jade_gui.classes.jade_screen import JadeScreen


@Gtk.Template(resource_path="/al/getcryst/jadegui/pages/user_screen.ui")
class UserScreen(JadeScreen, Adw.Bin):
    __gtype_name__ = "UserScreen"

    fullname_entry = Gtk.Template.Child()
    username_entry = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()
    password_confirmation = Gtk.Template.Child()

    username = ""
    fullname = ""
    sudo_enabled = True
    root_enabled = True
    username_filled = False
    fullname_filled = False
    password_filled = False
    move_to_summary = False

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.sudo_enabled = True
        self.root_enabled = True
        self.username_entry.connect("changed", self.username_passes_regex)
        self.fullname_entry.connect("changed", self.fullname_passes_regex)
        self.password_entry.connect("changed", self.verify_password)
        self.password_confirmation.connect("changed", self.verify_password)

    def fullname_passes_regex(self, widget):
        input = self.fullname_entry.get_text()
        print(input)
        if not len(input.strip()) > 0:
            print("Invalid fullname!")
            self.fullname_entry.add_css_class("error")
            self.fullname_filled = False
            self.verify_continue()
        else:
            print("Valid fullname!")
            self.fullname_entry.remove_css_class("error")
            self.fullname_filled = True
            self.verify_continue()
            self.fullname = input.strip()
            self.username_entry.set_text(self.fullname.lower().split()[0])

    def username_passes_regex(self, widget):
        input = self.username_entry.get_text()
        print(input)
        if not re.search("^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$", input) or input == 'blend':
            print("Invalid username!")
            self.username_entry.add_css_class("error")
            self.username_filled = False
            self.verify_continue()
        else:
            print("Valid username!")
            self.username_entry.remove_css_class("error")
            self.username_filled = True
            self.verify_continue()
            self.username = input

    def verify_password(self, widget):
        if (
            self.password_entry.get_text() == self.password_confirmation.get_text()
            and self.password_entry.get_text().strip()
            and "'" not in self.password_entry.get_text().strip()
            and "$" not in self.password_entry.get_text().strip()
            and len(self.password_entry.get_text().strip()) > 7
        ):
            self.password_filled = True
            self.verify_continue()
            self.password_confirmation.remove_css_class("error")
            self.password = self.encrypt_password(self.password_entry.get_text())
            self.password = (
                "'" + self.encrypt_password(self.password_entry.get_text()) + "'"
            )
        else:
            self.password_filled = False
            self.verify_continue()
            self.password_confirmation.add_css_class("error")

    def verify_continue(self):
        self.set_valid(self.password_filled and self.username_filled and self.fullname_filled)

    def encrypt_password(self, password):
        return password

    def carousel_next_summary(self, widget):
        self.next_page.move_to_summary = True
        self.carousel.scroll_to(self.next_page, True)
