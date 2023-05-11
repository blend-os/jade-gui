# partition.py

#
# Copyright 2022 user

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

from gi.repository import Gtk, GLib, Adw
from gettext import gettext as _
from jade_gui.manualpartitioning import filesystems, mountpoints
from jade_gui.classes.partition import Partition


@Gtk.Template(resource_path="/al/getcryst/jadegui/widgets/partition.ui")
class PartitionEntry(Adw.ActionRow):
    __gtype_name__ = "PartitionEntry"

    filesystem_dropdown = Gtk.Template.Child()
    mountpoint_dropdown = Gtk.Template.Child()

    def __init__(self, window, partition: Partition, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.partition = partition
        self.partition.filesystem = filesystems[0]
        self.partition.mountpoint = mountpoints[0]
        self.set_title(self.partition.partition)
        self.set_subtitle(self.partition.size)
        for filesystem in filesystems:
            self.filesystem_dropdown.append(filesystem, filesystem)
        self.filesystem_dropdown.set_active(0)
        for mountpoint in mountpoints:
            self.mountpoint_dropdown.append(mountpoint, mountpoint)
        self.mountpoint_dropdown.set_active(0)
        self.filesystem_dropdown.connect("changed", self.on_filesystem_select)
        self.mountpoint_dropdown.connect("changed", self.on_mountpoint_select)

    def on_filesystem_select(self, widget):
        print(self.filesystem_dropdown.get_active_text())
        self.partition.filesystem = self.filesystem_dropdown.get_active_text()
        _system = _boot = False
        _user_count = 0
        for i in range(0, len(self.window.available_partitions)):
            _partition = self.window.partition_screen.partition_list.get_row_at_index(
                i
            ).partition
            if _partition.mountpoint == 'System':
                if _system == True:
                    _system = False
                    break
                _system = True
            elif _partition.mountpoint == 'Boot':
                if _boot == True:
                    _boot = False
                    break
                _boot = True
            elif _partition.mountpoint == 'User':
                _user_count += 1
        if _system and _boot and _user_count <= 1:
            self.window.partition_screen.set_valid(True)
        else:
            self.window.partition_screen.set_valid(False)
        print("select " + self.partition.generate_jade_entry())

    def on_mountpoint_select(self, widget):
        self.partition.mountpoint = self.mountpoint_dropdown.get_active_text()
        _system = _boot = False
        _user_count = 0
        for i in range(0, len(self.window.available_partitions)):
            _partition = self.window.partition_screen.partition_list.get_row_at_index(
                i
            ).partition
            if _partition.mountpoint == 'System':
                if _system == True:
                    _system = False
                    break
                _system = True
            elif _partition.mountpoint == 'Boot':
                if _boot == True:
                    _boot = False
                    break
                _boot = True
            elif _partition.mountpoint == 'User':
                _user_count += 1
        if _system and _boot and _user_count <= 1:
            self.window.partition_screen.set_valid(True)
        else:
            self.window.partition_screen.set_valid(False)
        print("select " + self.partition.generate_jade_entry())
