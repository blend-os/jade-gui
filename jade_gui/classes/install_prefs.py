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
        timezone,
        locale,
        layout,
        variant,
        fullname,
        username,
        password,
        enable_sudo,
        hostname,
    ):
        self.timezone = timezone
        self.locale = locale
        self.layout = layout
        self.variant = variant
        self.fullname = fullname
        self.username = username
        self.password = password
        self.enable_sudo = enable_sudo
        self.hostname = hostname if len(hostname) != 0 else "crystal"

    def generate_json(self):
        prefs = {
            "locale": {
                "locale": self.locale,
                "keymap": self.layout.country_shorthand,
                "timezone": self.timezone.region + "/" + self.timezone.location,
            },
            "networking": {"hostname": self.hostname, "ipv6": False},
            "users": [
                {
                    "fullname": self.fullname,
                    "name": self.username,
                    "password": self.password,
                    "shell": "bash",
                }
            ],
            "flatpak": True,
            "kernel": "linux",
        }
        return json.dumps(prefs)
