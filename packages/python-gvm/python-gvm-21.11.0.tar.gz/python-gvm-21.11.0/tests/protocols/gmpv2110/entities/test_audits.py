# -*- coding: utf-8 -*-
# Copyright (C) 2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

from ...gmpv2110 import Gmpv2110TestCase
from ...gmpv208.entities.audits import (
    GmpCloneAuditTestMixin,
    GmpCreateAuditTestMixin,
    GmpDeleteAuditTestMixin,
    GmpGetAuditsTestMixin,
    GmpGetAuditTestMixin,
    GmpModifyAuditTestMixin,
    GmpResumeAuditTestMixin,
    GmpStartAuditTestMixin,
    GmpStopAuditTestMixin,
)


class Gmpv2110CloneAuditTestCase(GmpCloneAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110CreateAuditTestCase(GmpCreateAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110DeleteAuditTestCase(GmpDeleteAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetAuditTestCase(GmpGetAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110GetAuditsTestCase(GmpGetAuditsTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110ModifyAuditTestCase(GmpModifyAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110ResumeAuditTestCase(GmpResumeAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110StartAuditTestCase(GmpStartAuditTestMixin, Gmpv2110TestCase):
    pass


class Gmpv2110StopAuditTestCase(GmpStopAuditTestMixin, Gmpv2110TestCase):
    pass
