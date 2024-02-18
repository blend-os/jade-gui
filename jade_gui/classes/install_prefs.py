# install_prefs.py
#
# Copyright 2022
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
#
# SPDX-License-Identifier: GPL-3.0-only

from jade_gui.utils import disks
import json


class InstallPrefs:
    def __init__(
        self,
        disk,
        hostname,
        partition_mode,
        partitions,
    ):
        if partition_mode.lower() != "manual":
            self.disk = disk.disk
        else:
            self.disk = ""
        self.hostname = hostname if len(hostname) != 0 else "blend"
        self.partition_mode = partition_mode
        self.partitions = partitions
        self.is_efi = disks.get_uefi()
        self.bootloader_type = "grub-efi" if self.is_efi else "grub-legacy"
        self.bootloader_location = "/boot/efi/" if self.is_efi else self.disk

    def generate_json(self):
        prefs = {
            "partition": {
                "device": self.disk,
                "mode": self.partition_mode,
                "efi": self.is_efi,
                "partitions": self.partitions,
            },
            "bootloader": {
                "type": self.bootloader_type,
                "location": self.bootloader_location,
            },
            "networking": {"hostname": self.hostname, "ipv6": False},
            "kernel": "linux-zen",
        }
        return json.dumps(prefs)
