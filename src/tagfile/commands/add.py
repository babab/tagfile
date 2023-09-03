# file: src/tagfile/commands/add.py

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

import pycommand

from tagfile.core import tfman


class AddCommand(pycommand.CommandBase):
    '''Add a directory to media paths (to be scanned later or right away)'''
    usagestr = 'usage: tagfile add [options] <media-path>'
    description = __doc__
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('scan', ('', False, 'scan (all) media path(s) afterwards')),
    )

    def run(self):
        if self.flags.help:
            print(self.usage)
            return 0

        try:
            arg = self.args[0]
        except IndexError:
            arg = None

        if arg:
            filepath = os.path.expanduser(arg)
            if filepath == '.':
                try:
                    filepath = os.environ['PWD']
                except KeyError:
                    print('error: could not find PWD from shell environment')
                    return 2
            if not filepath:
                print('error: could not determine media path')
                return 3

            tfman.addPath(filepath)
            print('Added media path: {}'.format(filepath))
            if self.flags.scan:
                tfman.scan()
        else:
            print('error: command add requires argument')
            print()
            print('To add and scan current dir, use `tagfile add --scan .`')
            print('See `tagfile help add` OR `tagfile add -h` for more info.')
