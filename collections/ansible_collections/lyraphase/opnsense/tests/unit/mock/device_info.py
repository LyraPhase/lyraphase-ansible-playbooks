# -*- coding: utf-8 -*-
# Copyright 2025 LyraPhase LLC
# Copyright 2025 James Cuzella (@trinitronx)
#
# This file is part of LyraPhase OPNsense Collection
#
# LyraPhase OPNsense Collection is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LyraPhase OPNsense Collection is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with LyraPhase OPNsense Collection.
# If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function


__metaclass__ = type


class OPNsenseDeviceInfo:
    """Mock data class for OPNsense device information."""

    MOCK_DEVICE_INFO = {
        "network_os": "opnsense",
        # "network_os_model": "",
        "network_os_version": "24.4.3",
        "network_os_freebsd_version": "13.2-RELEASE-p12",
        "network_os_unbound_version": "1.20.0",
        "network_os_hostname": "OPNsense.internal",
    }
