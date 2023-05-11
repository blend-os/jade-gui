# partition_screen.py

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

import subprocess, shutil
from gi.repository import Gtk, Adw, GtkSource, Gdk
from gettext import gettext as _
from jade_gui.utils import disks
from jade_gui.utils.command import CommandUtils
from jade_gui.widgets.partition import PartitionEntry
from jade_gui.classes.partition import Partition
from jade_gui.classes.jade_screen import JadeScreen


class GuideWindow(Adw.Window):
    def __init__(self, window, title, content, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.title = title
        self.content = content
        self.create_window()
        self.set_default_size(900, 700)

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


@Gtk.Template(resource_path="/al/getcryst/jadegui/pages/partition_screen.ui")
class PartitionScreen(JadeScreen, Adw.Bin):
    __gtype_name__ = "PartitionScreen"

    disk_list = Gtk.Template.Child()
    open_guide = Gtk.Template.Child()
    open_gparted = Gtk.Template.Child()
    partition_list = Gtk.Template.Child()
    reload_partitions = Gtk.Template.Child()
    manual_partitioning = Gtk.Template.Child()
    automatic_partitioning = Gtk.Template.Child()
    manual_partitioning_page = Gtk.Template.Child()
    automatic_partitioning_page = Gtk.Template.Child()

    selected_partition = None
    move_to_summary = False

    def __init__(self, window, application, **kwargs):
        super().__init__(**kwargs)
        self.window = window
        self.disk_list.connect("row_selected", self.row_selected)
        self.manual_partitioning.connect("clicked", self.switch_manual_partitioning)
        self.reload_partitions.connect("clicked", self.check_partitions)
        self.automatic_partitioning.connect(
            "clicked", self.switch_automatic_partitioning
        )
        self.open_guide.connect("clicked", self.guide)
        self.open_gparted.connect("clicked", self.gparted)

    def gparted(self, widget):
        CommandUtils.run_command(["pkexec", "gparted"])

    def guide(self, widget):
        guide_contents = '''
 ____            _   _ _   _             _             
|  _ \ __ _ _ __| |_(_) |_(_) ___  _ __ (_)_ __   __ _ 
| |_) / _` | '__| __| | __| |/ _ \| '_ \| | '_ \ / _` |
|  __/ (_| | |  | |_| | |_| | (_) | | | | | | | | (_| |
|_|   \__,_|_|   \__|_|\__|_|\___/|_| |_|_|_| |_|\__, |
                                                 |___/ 
 _   _                    _        
| | | | _____      __    | |_ ___  
| |_| |/ _ \ \ /\ / /____| __/ _ \       (CC-BY-SA 4.0)
|  _  | (_) \ V  V /_____| || (_) |         (by rs2009)
|_| |_|\___/ \_/\_/       \__\___/ 
                                   
=======================================================

This guide will cover different configurations, including
users who want to install blendOS alongside Windows, as
well as Linux users who would like to keep their existing
Linux distribution and install blendOS alongside.

=======================================================

   ____           _      ___         __                                    
  / __/__  ____  | | /| / (_)__  ___/ /__ _    _____   __ _____ ___ _______
 / _// _ \/ __/  | |/ |/ / / _ \/ _  / _ \ |/|/ (_-<  / // (_-</ -_) __(_-<
/_/  \___/_/     |__/|__/_/_//_/\_,_/\___/__,__/___/  \_,_/___/\__/_/ /___/

Do you want to replace your existing Windows installation
with blendOS, or install blendOS alongside Windows without
losing your files?

If the former, follow the 'Automatic Partitioning' guide below; for
the latter, you may follow the 'Manual Partitioning' guide underneath.

+------------------------+
+ Automatic Partitioning +
+------------------------+

WARNING: Automatic partitioning will erase all files on your disk.

1. Switch back to Automatic Partitioning.

2. Select your main hard drive/SSD.

3. Proceed to the next page, and continue with installation.

+---------------------+
+ Manual Partitioning +
+---------------------+

1. Select 'Create Partitions'.

2. Make sure your primary system drive is selected.

3. Create a new partition of a size of 512MB, formatted as fat32.

4. Create another partition of a size of at least 40GBs, formatted as ext4.

5. Click on the tick above to apply the changes.

6. Close the opened window, and reload the list of available partitions.

7. Select the right-most dropdown for the 512MB partition, and select 'Boot'.

8. Select the right-most dropdown for the other partition, and select 'System'.

9. Voila! You may now proceed to the next page, and continue with installation.

=======================================================

   ____           __   _                                     
  / __/__  ____  / /  (_)__  __ ____ __  __ _____ ___ _______
 / _// _ \/ __/ / /__/ / _ \/ // /\ \ / / // (_-</ -_) __(_-<
/_/  \___/_/   /____/_/_//_/\_,_//_\_\  \_,_/___/\__/_/ /___/

Do you want to replace your existing Linux installation
with blendOS, or install blendOS alongside Linux without
losing your files?

If the former, follow the 'Automatic Partitioning' guide below; for
the latter, you may follow the 'Manual Partitioning' guide underneath.

+------------------------+
+ Automatic Partitioning +
+------------------------+

WARNING: Automatic partitioning will erase all files on your disk.

1. Switch back to Automatic Partitioning.

2. Select your main hard drive/SSD.

3. Proceed to the next page, and continue with installation.

+---------------------+
+ Manual Partitioning +
+---------------------+

1. Select 'Create Partitions'.

2. Make sure your primary system drive is selected.

3. Create a new partition of a size of 512MB, formatted as fat32.

4. Create another partition of a size of at least 40GBs, formatted as ext4.

5. Click on the tick above to apply the changes.

6. Close the opened window, and reload the list of available partitions.

7. Select the right-most dropdown for the 512MB partition, and select 'Boot'.

8. Select the right-most dropdown for the other partition, and select 'System'.

9. Voila! You may now proceed to the next page, and continue with installation.

=======================================================

Thanks for taking the time to read this entire guide!

Author: Rudra Saraswat
License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
'''
        GuideWindow(window=self.window, title="Partitioning How-to", content=guide_contents).present()

    def check_partitions(self, widget):
        self.partition_list.select_all()
        print(self.partition_list.get_row_at_index(2))
        for i in range(0, len(self.window.available_partitions)):
            self.partition_list.remove(self.partition_list.get_row_at_index(0))
        self.available_partitions = disks.get_partitions()
        self.window.available_partitions = self.available_partitions
        for partition in self.available_partitions:
            self.partition_list.append(
                PartitionEntry(
                    window=self,
                    partition=Partition(
                        partition=partition,
                        mountpoint="",
                        filesystem="",
                        size=disks.get_disk_size(partition),
                    ),
                    application=None,
                )
            )

    def switch_automatic_partitioning(self, widget):
        self.automatic_partitioning_page.set_visible(True)
        self.manual_partitioning_page.set_visible(False)
        if self.selected_partition == None:
            self.set_valid(False)
        else:
            self.set_valid(True)
        self.window.partition_mode = "Auto"

    def switch_manual_partitioning(self, widget):
        self.automatic_partitioning_page.set_visible(False)
        self.manual_partitioning_page.set_visible(True)
        _system = _boot = False
        _user_count = 0
        for i in range(0, len(self.window.available_partitions)):
            _partition = self.partition_list.get_row_at_index(
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
            self.set_valid(True)
        else:
            self.set_valid(False)
        self.window.partition_mode = "Manual"

    def row_selected(self, widget, row):
        if row is not None:
            print(row.get_title())
            for disk in self.disk_list:
                if disk != row:
                    self.window.ignore_selected_disk = True
                    disk.select_button.set_active(False)
                    self.window.ignore_selected_disk = False
            row.select_button.set_active(True)
            self.selected_partition = row

            self.set_valid(True)
        else:
            print("ERROR: invalid row slected")
