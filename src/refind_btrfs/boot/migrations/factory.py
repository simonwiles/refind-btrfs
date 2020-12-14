# region Licensing
# SPDX-FileCopyrightText: 2020 Luka Žaja <luka.zaja@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

""" refind-btrfs - Generate rEFInd manual boot stanzas from btrfs snapshots
Copyright (C) 2020  Luka Žaja

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# endregion

from functools import singledispatchmethod
from typing import Any, Optional, Type

from refind_btrfs.device.subvolume import Subvolume
from refind_btrfs.utility import helpers

from ..boot_stanza import BootStanza
from ..sub_menu import SubMenu
from .base_migration_strategy import BaseMigrationStrategy
from .boot_stanza_migration_strategy import BootStanzaMigrationStrategy
from .state import State
from .sub_menu_migration_strategy import SubMenuMigrationStrategy


class Factory:
    @singledispatchmethod
    @staticmethod
    def migration_strategy(
        argument: Any,
        current_subvolume: Subvolume,
        replacement_subvolume: Subvolume,
        include_paths: bool,
        is_latest: bool,
        inherit_from_state: Optional[State] = None,
    ) -> Type[BaseMigrationStrategy]:
        # pylint: disable=unused-argument
        type_name = type(argument).__name__

        raise NotImplementedError(
            f"Cannot instantiate migration strategy for type '{type_name}'!"
        )

    @migration_strategy.register(BootStanza)
    @staticmethod
    def _(
        argument: BootStanza,
        current_subvolume: Subvolume,
        replacement_subvolume: Subvolume,
        include_paths: bool,
        is_latest: bool,
        inherit_from_state: Optional[State] = None,
    ) -> Type[BaseMigrationStrategy]:
        # pylint: disable=unused-argument
        return BootStanzaMigrationStrategy(
            argument, current_subvolume, replacement_subvolume, include_paths, is_latest
        )

    @migration_strategy.register(SubMenu)
    @staticmethod
    def _(
        argument: SubMenu,
        current_subvolume: Subvolume,
        replacement_subvolume: Subvolume,
        include_paths: bool,
        is_latest: bool,
        inherit_from_state: Optional[State] = None,
    ) -> Type[BaseMigrationStrategy]:
        # pylint: disable=unused-argument
        return SubMenuMigrationStrategy(
            argument,
            current_subvolume,
            replacement_subvolume,
            helpers.none_throws(inherit_from_state),
            include_paths,
            is_latest,
        )
