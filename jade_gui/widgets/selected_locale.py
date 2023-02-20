# selected_locale.py

#
# Copyright 2022 axtlos <axtlos@getcryst.al>

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

@Gtk.Template(resource_path="/al/getcryst/jadegui/widgets/selected_locale.ui")
class SelectedLocale(Adw.ActionRow):
    __gtype_name__ = "SelectedLocale"

    remove_locale = Gtk.Template.Child()

    def __init__(self, page, window, locale, application, **kwargs):
        super().__init__(**kwargs)

        self.window = window
        self.page = page
        self.locale = locale

        self.set_title(locale)
        self.remove_locale.connect("clicked", self.remove_locale_clicked)

    def remove_locale_clicked(self, button):
        self.page.update_selected_locale_list(remove=self.locale, row=self)
