#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 Samsung Electronics, Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''Package setup script'''

import glob
from distutils.core import setup

setup(
    name = 'autotwiki',
    version = '1.00',
    author = 'Bryce W. Harrington',
    author_email = 'bryce@osg.samsung.com',
    description = 'Updates status pages in Twiki',
    license = 'GPL',
    platforms = 'linux',
    requires = ['json', 'mechanize', 'argparse', 'subprocess', 'datetime'],
    packages = ['autotwiki'],
    package_data = {
        },
    data_files = [ ],
    scripts = [
        'bin/autotwiki',
        'bin/commit-stats'
        ]
    )
