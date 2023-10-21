# file: src/tagfile/common.py

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


class ConfigError(Exception):
    pass


class ProgrammingError(Exception):
    pass


class ConfigValidator:
    def __init__(self, top_dict):
        self.top_dict = top_dict

    def parse_dots(self, name):
        names = name.split('.')
        if len(names) == 1:
            struct = self.top_dict
        elif len(names) == 2:
            struct = self.top_dict[names[0]]
        elif len(names) == 3:
            struct = self.top_dict[names[0]][names[1]]
        elif len(names) == 4:
            struct = self.top_dict[names[0]][names[1]][names[2]]
        elif len(names) == 5:
            struct = self.top_dict[names[0]][names[1]][names[2]][names[3]]
        else:
            raise ProgrammingError('config structure is too nested')
        realname = names[-1]
        return (struct, realname)

    def is_bool(self, name):
        parent, realname = self.parse_dots(name)
        if realname not in parent:
            raise ConfigError(f'Missing "{name}" setting')
        if not type(parent[realname]) is bool:
            raise ConfigError(f'Value for "{name}" must be a bool')

    def is_list(self, name):
        parent, realname = self.parse_dots(name)
        if realname not in parent:
            raise ConfigError(f'Missing "{name}" setting')
        if not type(parent[realname]) is list:
            raise ConfigError(f'Value for "{name}" must be a list')

    def is_dict(self, name, min_size=None):
        parent, realname = self.parse_dots(name)
        if realname not in parent:
            raise ConfigError(f'Missing "{name}" section')
        if not type(parent[realname]) is dict:
            raise ConfigError(f'{name} is not a dictionary')
        if min_size:
            if len(parent[realname]) < min_size:
                raise ConfigError(
                    f'{name} has less than {min_size} '
                    f'item{"s" if len(min_size) > 1 else ""}'
                )

    def is_str(self, name, options=[]):
        '''Will validate if value is one of the options when not empty.'''
        parent, realname = self.parse_dots(name)
        if realname not in parent:
            raise ConfigError(f'Missing "{name}" setting')
        if not type(parent[realname]) is str:
            raise ConfigError('Value for "{name}" must be string')
        if options and parent[realname] not in options:
            raise ConfigError(
                f'Setting "{name}" is not valid.\n'
                f'Valid options are: {",".join(options)}'
            )

    def is_int(self, name, vmin=None, vmax=None):
        parent, realname = self.parse_dots(name)
        if realname not in parent:
            raise ConfigError(f'Missing "{name}" setting')
        if not type(parent[realname]) is int:
            raise ConfigError(f'Value for "{name}" must be a list')
        if vmin is not None and parent[realname] < vmin:
            raise ConfigError(f'Value for "{name}" must be >= {vmin}')
        if vmax is not None and parent[realname] > vmax:
            raise ConfigError(f'Value for "{name}" must be <= {vmax}')


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
