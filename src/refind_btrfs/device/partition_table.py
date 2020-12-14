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

from __future__ import annotations

from copy import deepcopy
from typing import Iterable, List, Optional

from more_itertools import only

from refind_btrfs.utility import helpers

from .partition import Partition
from .subvolume import Subvolume


class PartitionTable:
    def __init__(self, uuid: str, pt_type: str) -> None:
        self._uuid = uuid
        self._pt_type = pt_type
        self._partitions: Optional[List[Partition]] = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PartitionTable):
            return self.uuid == other.uuid

        return False

    def __hash__(self) -> int:
        return hash(self.uuid)

    def with_partitions(self, partitions: Iterable[Partition]) -> PartitionTable:
        self._partitions = list(partitions)

        return self

    def has_been_migrated_to(self, replacement_subvolume: Subvolume) -> bool:
        root = helpers.none_throws(self.root)
        filesystem = helpers.none_throws(root.filesystem)
        mount_options = helpers.none_throws(filesystem.mount_options)

        return mount_options.is_matched_with(replacement_subvolume)

    def as_migrated_from_to(
        self, current_subvolume: Subvolume, replacement_subvolume: Subvolume
    ) -> PartitionTable:
        replacement = deepcopy(self)
        root = helpers.none_throws(replacement.root)
        filesystem = helpers.none_throws(root.filesystem)
        mount_options = helpers.none_throws(filesystem.mount_options)

        mount_options.migrate_from_to(current_subvolume, replacement_subvolume)

        return replacement

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def pt_type(self) -> str:
        return self._pt_type

    @property
    def esp(self) -> Optional[Partition]:
        return only(partition for partition in self._partitions if partition.is_esp())

    @property
    def root(self) -> Optional[Partition]:
        return only(partition for partition in self._partitions if partition.is_root())

    @property
    def boot(self) -> Optional[Partition]:
        return only(partition for partition in self._partitions if partition.is_boot())
