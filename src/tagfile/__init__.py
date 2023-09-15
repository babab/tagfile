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

import datetime
import os
import sys

import colors
import peewee as pw
import yaml

__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2015-2023  Benjamin Althues"
__version__ = '0.2.0a5'
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


def invertexpanduser(path):
    '''Replaces a substring of `os.path.expanduser(path)` with ``~``.'''
    home_abspath = os.path.expanduser('~')
    if path.startswith(home_abspath):
        return path.replace(home_abspath, '~')
    return path


# Set base paths, overridable using ENV vars
TAGFILE_DATA_HOME = os.environ.get(
    'TAGFILE_DATA_HOME',
    os.path.expanduser('~/.local/share/tagfile')
)
TAGFILE_CONFIG_HOME = os.environ.get(
    'TAGFILE_CONFIG_HOME',
    os.path.expanduser('~/.config/tagfile')
)

defaultconfig = '''# config created by {versionStr} at {date}

# A tilde `~` in filepaths will expand to $HOME on *BSD/Linux/MacOS/Unix
# or %USERPROFILE% on Windows.

log-file:   {data_home}/tagfile.log
load-bar:   yes
ignore:
    - .git
    - .hg
    - .svn
    - .pyc
    - .virtualenv
    - __pycache__
    - node_modules
ignore-empty:   yes

# hash-algo can be 'md5' or 'sha1'
hash-algo:      sha1
hash-buf-size:  1024
'''.format(
    data_home=invertexpanduser(TAGFILE_DATA_HOME),
    date=datetime.datetime.now(),
    versionStr=versionStr
)

config = yaml.safe_load(defaultconfig)

# initialize data path
if not os.path.exists(TAGFILE_DATA_HOME):
    os.makedirs(TAGFILE_DATA_HOME)

# initialize config path and create config.yaml file
if not os.path.exists(TAGFILE_CONFIG_HOME):
    os.makedirs(TAGFILE_CONFIG_HOME)
    _filepath = os.path.join(TAGFILE_CONFIG_HOME, 'config.yaml')
    with open(_filepath, 'w') as _fconf:
        _fconf.write(defaultconfig)
        print(colors.green(
            'Copied default config into file "{}"\n'.format(_filepath)
        ))

# Read user config file
_filepath = os.path.join(TAGFILE_CONFIG_HOME, 'config.yaml')
if os.path.exists(_filepath):
    config.update(yaml.safe_load(open(_filepath).read()))

# Init sqlite database - used in peewee models
DB = pw.SqliteDatabase(os.path.join(TAGFILE_DATA_HOME, 'index.db'))
