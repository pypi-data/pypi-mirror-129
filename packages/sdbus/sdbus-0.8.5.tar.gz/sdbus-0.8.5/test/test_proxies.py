# SPDX-License-Identifier: LGPL-2.1-or-later

# Copyright (C) 2020, 2021 igo95862

# This file is part of python-sdbus

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
from __future__ import annotations

from unittest import main

from sdbus_async.dbus_daemon import FreedesktopDbus

from .common_test_util import TempDbusTest


class TestFreedesktopDbus(TempDbusTest):
    async def test_connection(self) -> None:
        dbus_object = FreedesktopDbus(self.bus)

        await dbus_object.dbus_ping()
        await dbus_object.dbus_introspect()
        await dbus_object.dbus_machine_id()
        self.assertIsInstance(await dbus_object.get_id(), str)
        self.assertIsInstance(await dbus_object.features, list)


if __name__ == "__main__":
    main()
