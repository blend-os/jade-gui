# window.py

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

import time
import socket
from gi.repository import Gtk, Gdk, GLib, Adw
from jade_gui.classes.partition import Partition
from jade_gui.widgets.disk import DiskEntry
from jade_gui.widgets.partition import PartitionEntry
from jade_gui.functions.keyboard_screen import KeyboardScreen
from jade_gui.functions.timezone_screen import TimezoneScreen
from jade_gui.functions.locale_screen import LocaleScreen
from jade_gui.functions.user_screen import UserScreen
from jade_gui.functions.partition_screen import PartitionScreen
from jade_gui.functions.summary_screen import SummaryScreen
from jade_gui.functions.install_screen import InstallScreen
from jade_gui.functions.finished_screen import FinishedScreen
from jade_gui.functions.welcome_screen import WelcomeScreen
from jade_gui.classes.jade_screen import JadeScreen
from jade_gui.locales.locales_list import locations
from jade_gui.keymaps import keymaps
from jade_gui.utils import disks
from jade_gui.utils.threading import RunAsync


@Gtk.Template(resource_path="/al/getcryst/jadegui/window.ui")
class JadeGuiWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "JadeGuiWindow"

    event_controller = Gtk.EventControllerKey.new()
    carousel = Gtk.Template.Child()

    #   quit_button = Gtk.Template.Child()
    about_button = Gtk.Template.Child()
    # no_internet = Gtk.Template.Child()

    next_button = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    revealer = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finished_screen = FinishedScreen(
            window=self, set_valid=self.page_valid, **kwargs
        )
        self.installer_screen = InstallScreen(
            window=self, set_valid=self.page_valid, **kwargs
        )
        self.user_screen = UserScreen(window=self, set_valid=self.page_valid, **kwargs)
        self.keyboard_screen = KeyboardScreen(
            window=self, set_valid=self.page_valid, keymaps=keymaps, **kwargs
        )
        self.timezone_screen = TimezoneScreen(
            window=self, set_valid=self.page_valid, locations=locations, **kwargs
        )
        self.locale_screen = LocaleScreen(
            window=self, set_valid=self.page_valid, locations=locations, **kwargs
        )
        self.welcome_screen = WelcomeScreen(
            window=self,
            set_valid=self.page_valid,
            next_page=self.next,
            online=self.online,
            **kwargs
        )

        self.summary_screen = SummaryScreen(
            window=self, set_valid=self.page_valid, **kwargs
        )
        self.carousel.append(self.welcome_screen)
        self.carousel.append(self.keyboard_screen)
        self.carousel.append(self.timezone_screen)
        self.carousel.append(self.locale_screen)
        self.carousel.append(self.user_screen)
        self.carousel.append(self.summary_screen)
        self.carousel.append(self.installer_screen)
        self.carousel.append(self.finished_screen)
        ### Widgets for first page (welcome screen)
        # self.quit_button.connect("clicked", self.confirmQuit)
        # self.summary_screen.connect_buttons()
        self.about_button.connect("clicked", self.show_about)
        self.partition_mode = "Auto"
        ### ---------

        self.next_button.connect("clicked", self.next)
        self.back_button.connect("clicked", self.back)

        RunAsync(self.welcome_screen.check_internet)

    def online(self):
        if self.timezone_screen.guessed_timezone is None:
            self.timezone_screen.ip_request_timezone()

    def _get_current_page(self, offset=0) -> JadeScreen:
        current_index = self.carousel.get_position()
        return self.carousel.get_nth_page(current_index + offset)

    def on_page_change(self, page: JadeScreen):
        self.next_button.set_sensitive(page.is_valid())

        disable_next = page not in [self.welcome_screen, self.finished_screen]
        disable_back = page not in [
            self.welcome_screen,
            self.installer_screen,
            self.finished_screen,
        ]

        if disable_back == disable_next:
            self.revealer.set_reveal_child(disable_next)
            self.next_button.set_visible(True)
            self.back_button.set_visible(True)
        else:
            self.next_button.set_visible(disable_next)
            self.back_button.set_visible(disable_back)

        page.on_show()

    def next(self, *_):
        previous_page = self._get_current_page()
        page = self._get_current_page(1)
        self.carousel.scroll_to(page, True)

        previous_page.on_complete()
        self.on_page_change(page)

    def back(self, *_):
        page = self._get_current_page(-1)
        self.carousel.scroll_to(page, True)

        self.on_page_change(page)

    def page_valid(self, valid: bool):
        self.next_button.set_sensitive(valid)

    def show_page(self, _, page, *__):
        self.carousel.scroll_to(page, True)

    def show_about(self, *_):
        builder = Gtk.Builder.new_from_resource("/al/getcryst/jadegui/about.ui")
        about_window = builder.get_object("aboutWindow")
        about_window.set_transient_for(self)
        about_window.present()
