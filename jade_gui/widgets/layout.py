# layout.py

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

from gi.repository import Gtk, GLib, Adw
from gettext import gettext as _
from jade_gui.widgets.variant import KeyboardVariant


@Gtk.Template(resource_path="/al/getcryst/jadegui/widgets/layout.ui")
class KeyboardLayout(Adw.ExpanderRow):
    __gtype_name__ = "KeyboardLayout"

    variants = []
    rows = []

    def __init__(
        self, window, country, country_shorthand, keymap, application, **kwargs
    ):
        super().__init__(**kwargs)
        self.window = window
        self.country = country
        self.country_shorthand = country_shorthand

        self.set_title(country)
        self.set_subtitle(country_shorthand)
        self.variants = keymap.variants
        self.connect("activate", self.selected)

        firstvariant = KeyboardVariant(
            window=window,
            variant=keymap.variants[0],
            country=self.country,
            country_shorthand=self.country_shorthand,
            button_group=None,
            application=application,
            **kwargs
        )

        self.add_row(firstvariant)

        for variant in keymap.variants:
            if variant != firstvariant.variant:
                self.add_row(
                    KeyboardVariant(
                        window=window,
                        country=self.country,
                        country_shorthand=self.country_shorthand,
                        variant=variant,
                        button_group=firstvariant.select_variant,
                        application=application,
                        **kwargs
                    )
                )

    def add_row(self, row):
        super().add_row(row)
        self.rows.append(row)

    def selected(self, widget):
        print("selected")
        self.window.keyboard_screen.selected_layout(widget=widget, row=self)
