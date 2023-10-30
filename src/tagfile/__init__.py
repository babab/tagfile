'''Search, index and tag your files and find duplicates'''

# Copyright (c) 2015-2023 Benjamin Althues <benjamin@babab.nl>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

import peewee

import tagfile.config
import tagfile.common

__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2015-2023  Benjamin Althues"
__version__ = '0.2.0a13'
versionStr = 'tagfile {}'.format(__version__)


def verboseVersionInfo():
    '''Returns a string with verbose version information
    The string shows the version of tagfile and that of Python.
    It also displays the name of the operating system/platform name.
    '''
    return '{}\n{}\n\nPython {}\nInterpreter is at {}\nPlatform is {}'.format(
        versionStr,
        __copyright__,
        sys.version.replace('\n', ''),
        sys.executable or 'unknown',
        os.name,
    )


configuration = tagfile.config.Configuration()
cfg = configuration.cfg

database = peewee.SqliteDatabase(None, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
})
'''Database handler for Peewee ORM / sqlite database.

The database gets connected in `tagfile.core.tfman.init()`, which is
called at the last appropiate time, in the shellcommands, after parsing
all options and arguments.
'''
