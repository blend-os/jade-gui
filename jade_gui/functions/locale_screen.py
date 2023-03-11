# locale_screen.py

#
# Copyright 2022 axtlos <axtlos@getcryst.al>

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License only.
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
import time, locale
from jade_gui.classes.jade_screen import JadeScreen
from jade_gui.widgets.locale import LocaleEntry
from jade_gui.widgets.selected_locale import SelectedLocale
from jade_gui.utils.gtk_helpers import set_list_text



@Gtk.Template(resource_path="/al/getcryst/jadegui/pages/locale/locale_screen.ui")
class LocaleScreen(JadeScreen, Adw.Bin):
    __gtype_name__ = "LocaleScreen"

    event_controller = Gtk.EventControllerKey.new()

    ### Page and widgets on timezone screen
    locale_search_button = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    main_locale_list = Gtk.Template.Child()
    other_locale_list = Gtk.Template.Child()

    empty_locales = Gtk.Template.Child()

    style_provider = Gtk.CssProvider()
    date_preview = Gtk.Template.Child()
    datespreview = Gtk.Template.Child()
    number_preview = Gtk.Template.Child()
    numberpreview = Gtk.Template.Child()
    chosen_locales = []
    other_locales = []
    move_to_summary = False

    def __init__(self, window, locations, set_valid, application, **kwargs):
        super().__init__(set_valid=set_valid, **kwargs)
        self.window = window
        self.application = application
        self.kwargs = kwargs
        self.style_provider.load_from_data(".emptyLocales { font-style: italic; font-size: 15px; }", -1)
        Gtk.StyleContext.add_provider(
            self.empty_locales.get_style_context(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        builder = Gtk.Builder.new_from_resource(
            "/al/getcryst/jadegui/pages/locale/locale_dialog.ui"
        )
        self.search_dialog = builder.get_object("search_dialog")

        self.search_dialog.set_transient_for(self.window)
        self.search_dialog.set_modal(self.window)

        self.locale_entry_search = builder.get_object("locale_entry_search")
        self.locale_list = builder.get_object("locale_list")
        self.locale_search = builder.get_object("locale_search")

        self.event_controller.connect("key-released", self.search_locales)
        self.locale_entry_search.add_controller(self.event_controller)
        self.locale_list.connect("row-selected", self.select_locale)
        self.locale_search_button.connect("clicked", self.present_dialog)

        self._locale_list_length = 1
        try:
            self.chosen_locales = [self.window.timezone_screen.chosen_timezone.locale]
        except:
            self.chosen_locales = ["en_US.UTF-8 UTF-U"]

        en_US = LocaleEntry(
            page=self,
            window=window,
            locale="en_US.UTF-8 UTF-8",
            button_group=None,
            application=application,
            **kwargs,
        )
        self.locale_list.append(en_US)
        if(len(self.chosen_locales) <= 0):
            self.chosen_locales.append("en_US.UTF-8 UTF-8")
        set_list_text(self.main_locale_list, self.chosen_locales[0])
        locales=["en_US.UTF-8 UTF-8"] # Keep a list of added locales to avoid duplicates
        for i in locations:
            for locale in i:
                if locale.locales not in locales:
                    row = LocaleEntry(
                        page=self,
                        window=window,
                        locale=locale.locales,
                        button_group=en_US.main_locale_button,
                        application=application,
                        **kwargs,
                    )
                    locales.append(locale.locales)
                    if row.locale in self.chosen_locales[0]:
                        row.main_locale_button.set_active(True)
                    self.locale_list.append(row)
                    self._locale_list_length += 1
        self.update_locale_preview()

    def present_dialog(self, *_):
        self.search_dialog.present()

    def update_from_row(self, row):
        if row.main_locale_button.get_active():
            set_list_text(self.main_locale_list, row.locale)
            for i in self.other_locales:
                if i.locale == row.locale:
                    self.update_selected_locale_list(remove=i.locale, row=i)
                    if self.other_locales == []:
                        self.empty_locales.show()
            self.update_selected_locale_list(main=row.locale)
        else:
            self.empty_locales.set_visible(False)
            locale = SelectedLocale(
                page=self,
                window=self.window,
                locale=row.locale,
                application=self.application,
                **self.kwargs,
            )
            self.update_selected_locale_list(add=row.locale, row=locale)

    def update_locale_preview(self):
        locale.setlocale(locale.LC_ALL, self.chosen_locales[0][:-6])
        self.datespreview.set_label(time.strftime(locale.nl_langinfo(locale.D_T_FMT)))
        self.numberpreview.set_label(locale.format_string("%.2f", 1234567.89, grouping=True)+"  -  "+locale.currency(1234.56, grouping=True))

    def update_selected_locale_list(self, add=None, remove=None, main=None, row=None):
        if main:
            self.chosen_locales[0] = main
            self.set_valid(True)
            self.update_locale_preview()
        if add:
            if add not in self.chosen_locales:
                self.chosen_locales.append(add)
                if row is not None:
                    self.other_locales.append(row)
                    self.other_locale_list.add_row(row)
        if remove:
            if remove != self.chosen_locales[0]:
                self.chosen_locales.remove(remove)
                if row is not None:
                    self.other_locales.remove(row)
                    self.other_locale_list.remove(row)
                if self.other_locales == []:
                    self.empty_locales.show()
            else:
                print("Tried to remove main locale!!")
                return
        print(self.chosen_locales)

    def select_locale(self, widget, row):
        self.search_dialog.hide()

        self.status_page.set_description("")
        self.update_from_row(row)

    def search_locales(self, *args):
        terms = self.locale_entry_search.get_text()
        self.locale_list.set_filter_func(self.filter_locales, terms)

    def on_show(self):
        self.chosen_locales = [self.window.timezone_screen.chosen_timezone.locale]
        set_list_text(self.main_locale_list, self.chosen_locales[0])
        self.update_locale_preview()
        if self.chosen_locales != []:
            self.set_valid(True)

    @staticmethod
    def filter_locales(row, terms=None):
        try:
            text = row.get_title()
            text = text.lower() + row.get_subtitle().lower()
            if terms.lower() in text:
                return True
        except:
            return True
        return False
