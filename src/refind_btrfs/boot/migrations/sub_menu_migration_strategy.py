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

from typing import Optional

from refind_btrfs.common import constants
from refind_btrfs.device.subvolume import Subvolume
from refind_btrfs.utility import helpers

from ..boot_options import BootOptions
from ..sub_menu import SubMenu
from .base_migration_strategy import BaseMigrationStrategy
from .state import State


class SubMenuMigrationStrategy(BaseMigrationStrategy):
    def __init__(
        self,
        sub_menu: SubMenu,
        current_subvolume: Subvolume,
        replacement_subvolume: Subvolume,
        inherit_from_state: State,
        include_paths: bool,
        is_latest: bool,
    ) -> None:
        super().__init__(
            State(
                sub_menu.name,
                sub_menu.loader_path,
                sub_menu.initrd_path,
                sub_menu.boot_options,
                sub_menu.add_boot_options,
            ),
            current_subvolume,
            replacement_subvolume,
            include_paths,
            is_latest,
        )

        self._inherit_from_state = inherit_from_state

    def migrate(self) -> State:
        include_paths = self._include_paths
        is_latest = self._is_latest
        current_state = self._current_state
        inherit_from_state = self._inherit_from_state

        replacement_loader_path = current_state.loader_path
        replacement_initrd_path = current_state.initrd_path
        replacement_boot_options: Optional[BootOptions] = None
        replacement_add_boot_options = self.replacement_add_boot_options

        if not is_latest:
            if include_paths:
                replacement_loader_path = inherit_from_state.loader_path
                replacement_initrd_path = inherit_from_state.initrd_path

            replacement_boot_options = BootOptions.merge(
                (
                    inherit_from_state.boot_options,
                    replacement_add_boot_options,
                )
            )
            replacement_add_boot_options = BootOptions(constants.EMPTY_STR)

        if include_paths:
            replacement_loader_path_candidate = self.replacement_loader_path
            replacement_initrd_path_candidate = self.replacement_initrd_path

            if not helpers.is_none_or_whitespace(replacement_loader_path_candidate):
                replacement_loader_path = replacement_loader_path_candidate

            if not helpers.is_none_or_whitespace(replacement_initrd_path_candidate):
                replacement_initrd_path = replacement_initrd_path_candidate

        return State(
            self.replacement_name,
            replacement_loader_path,
            replacement_initrd_path,
            replacement_boot_options,
            replacement_add_boot_options,
        )
