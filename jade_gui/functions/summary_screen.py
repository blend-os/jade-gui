# summary_screen.py

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

import os
from jade_gui.utils import disks
from jade_gui.classes.install_prefs import InstallPrefs
from jade_gui.utils.threading import RunAsync
from jade_gui.classes.jade_screen import JadeScreen
from gi.repository import Gtk, Adw
from gettext import gettext as _


@Gtk.Template(resource_path="/al/getcryst/jadegui/pages/summary_screen.ui")
class SummaryScreen(JadeScreen, Adw.Bin):
    __gtype_name__ = "SummaryScreen"

    partition_label = Gtk.Template.Child()
    partition_button = Gtk.Template.Child()
    uefi_label = Gtk.Template.Child()
    # unakite_label = Gtk.Template.Child()

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window

        self.set_valid(True)

        self.partition_button.connect(
            "clicked", self.window.show_page, self.window.partition_screen
        )

    def on_show(self):

        if self.window.partition_mode == "Manual":
            self.partition_label.set_title("Manual partitioning selected")
            self.partition_label.set_subtitle("")
        else:
            self.partition_label.set_title(
                self.window.partition_screen.selected_partition.disk
            )
            self.partition_label.set_subtitle(
                self.window.partition_screen.selected_partition.disk_size
            )
        self.uefi_label.set_title("UEFI" if disks.get_uefi() else "Legacy BIOS")

        # self.unakite_label.set_title("Unakite enabled "+"enabled" if self.window.misc_screen.)

        partitions = []
        for i in range(0, len(self.window.available_partitions)):
            partition = self.window.partition_screen.partition_list.get_row_at_index(
                i
            ).partition
            partitions.append(partition.generate_jade_entry())

        self.installprefs = InstallPrefs(
            disk=self.window.partition_screen.selected_partition,
            hostname='blend',
            partition_mode=self.window.partition_mode,
            partitions=partitions,
        )
        print(self.installprefs.generate_json())
