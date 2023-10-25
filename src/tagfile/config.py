'''Config management'''

# file: src/tagfile/config.py

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
import tomllib

from tagfile import common

defaultconfig = '''# config created by tagfile 0.2.0a11 at {date}

# Use multiple config files to:
# - define (sets of) database locations
# - tie one ore more DB's to a set of ignore rules

# A tilde `~` in filepaths will expand to $HOME on *BSD/Linux/MacOS/Unix
# or `%USERPROFILE%` on Windows.

default_database = "main"

logging.enabled = true
logging.file = "{data_home}/tagfile.log"

# Valid levels are: "info", "warning", "error" and "fatal".
# Use "info" to log most actions, like adding and ignoring files during
# scanning, pruning files, etc. These messages are not printed to the
# console by default, unless a --verbose option flag is used.
# Level "debug" will log all database queries, impacting performance
# and should only be used when absolutely needed for debugging purposes.
# The recommended level is "warning".
logging.level = "warning"

[ui]
progressbars = true

# Colors can be "auto", "always", "never"
colors = "auto"

[databases]
# Database `main` must always be defined. You can define other sqlite DB's
# to keep separate indexes as you see fit. To use a specific
# database for a certain period of time, define it in the config as
# database.default or pass it as argument with --db, like:
#     tagfile --db=main <command> [option]

main = "{data_home}/main.db"
#custom = "{data_home}/custom.db"
#cats = "{data_home}/cat-pictures.sqlite"

[ignore.name-based]
# Will try to match paths/filenames in the order of:
# 1. paths (substrings of the absolute full path to file)
# 2. filenames (exact match with basename)
# 3. extensions (basename ends with extension)
paths = [
    "/.git/",
    "/.hg/",
    "/.idea/",
    "/node_modules/",
    "/__pycache__/",
    "/.svn/",
    "/.venv/",
    "/venv/",
    "/.virtualenv/",
]
filenames = [
    "GPATH",
    "GRTAGS",
    "GTAGS",
    "tags",
]
extensions = [
    ".7z",
    ".class",
    ".com",
    ".dll",
    ".exe",
    ".geany",
    ".gz",
    ".iso",
    ".log",
    ".o",
    ".pyc",
    ".rar",
    ".so",
    ".sqlite",
    ".swp",
    ".tar",
    ".tgz",
    ".zip",
]

[ignore.essential]
# You probably don't need to track 0 byte files.
empty-files = true

# For unixy systems that support them, symlinks to files that are in the
# same database will show up as clones. Because they are not physical
# copies / actual duplicates, you probably want to ignore them.
symlinks = true

[hashing]
# algorithm can be "md5" or "sha1"
algorithm = "sha1"
buffer-size = 1024
'''.format(
    data_home=common.invertexpanduser(common.TAGFILE_DATA_HOME),
    date=datetime.datetime.now()
)


class Configuration:
    cfg = tomllib.loads(defaultconfig)
    dirpath = common.TAGFILE_CONFIG_HOME
    basename = 'config.toml'
    fullpath = None

    def __init__(self):
        self.fullpath = os.path.join(self.dirpath, self.basename)
        self.write_defaultconfig()
        self.load_configfile()
        self.validate()
        self.apply()

    def set_paths(self, fullpath_or_dirpath, basename='>unset<'):
        if basename == '>unset<':
            self.fullpath = fullpath_or_dirpath
            self.dirpath = os.path.dirname(fullpath_or_dirpath)
            self.basename = os.path.basename(fullpath_or_dirpath)
        else:
            self.fullpath = os.path.join(fullpath_or_dirpath, basename)
            self.dirpath = fullpath_or_dirpath
            self.basename = basename

    def write_defaultconfig(self, makedirs=True):
        '''Create config home dirs and config.toml at first run'''
        if not os.path.exists(self.fullpath):
            if not os.path.exists(self.dirpath):
                if makedirs:
                    os.makedirs(self.dirpath)
                else:
                    raise common.ConfigError(
                        'dirpath "{}" does not exist'.format(self.dirpath)
                    )
            with open(self.fullpath, 'w') as _fconf:
                _fconf.write(defaultconfig)

    def load_configfile(self):
        '''Update config by parsing user's TOML config file.

        Raises common.configError if an error occurs.
        '''
        if not os.path.exists(self.fullpath):
            raise common.ConfigError(
                'File "{}" does not exist'.format(self.fullpath)
            )

        with open(self.fullpath, 'rb') as _file:
            try:
                self.cfg.update(tomllib.load(_file))
            except tomllib.TOMLDecodeError as e:
                raise common.ConfigError(f'TOML syntax: {e}')

    def validate(self, config_var=None):
        cfg = config_var if config_var else self.cfg

        if not cfg:
            raise common.ConfigError('config is empty dict or false-ish')
        if not type(cfg) is dict:
            raise common.ConfigError('config is not a dictionary')

        val = common.ConfigValidator(cfg)
        val.is_str('default_database')
        val.is_dict('logging', min_size=3)
        val.is_bool('logging.enabled')
        val.is_str('logging.file')
        val.is_str('logging.level', options=[
            'debug', 'info', 'warn', 'warning', 'error', 'fatal', 'critical',
        ])
        val.is_dict('ui')
        val.is_bool('ui.progressbars')
        val.is_str('ui.colors', options=['auto', 'always', 'never'])
        val.is_dict('databases', min_size=1)
        val.is_str('databases.main')
        val.is_dict('ignore', min_size=2)
        val.is_dict('ignore.name-based', min_size=3)
        val.is_list('ignore.name-based.paths')
        val.is_list('ignore.name-based.filenames')
        val.is_list('ignore.name-based.extensions')
        val.is_dict('ignore.essential', min_size=1)
        val.is_bool('ignore.essential.empty-files')
        val.is_bool('ignore.essential.symlinks')
        val.is_dict('hashing', min_size=2)
        val.is_str('hashing.algorithm', options=['sha1', 'md5'])
        val.is_int('hashing.buffer-size', vmin=64)

    def apply(self):
        '''Apply settings that have a global nature'''
        if self.cfg['ui']['colors'] == 'always':
            os.environ['FORCE_COLOR'] = '1'
        elif self.cfg['ui']['colors'] == 'never':
            os.environ['NO_COLOR'] = '1'
