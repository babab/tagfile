# file: src/tagfile/commands/listcmd.py

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

import sys

import pycommand

import tagfile.core
import tagfile.files
from tagfile.models import Index
import tagfile.output
import tagfile.repeat


class ListCommand(pycommand.CommandBase):
    '''Output a list of all indexed files.'''
    usagestr = (
        'usage: tagfile list [-H | --show-hash] [-s | --show-size] '
        '[-t | --show-type]\n'
        '                    [-m | --show-mime] [-a | --show-all] '
        '[-S COL | --sort=COL]\n\n'
        '   or: tagfile list [-0 | --print0] [-S COL | --sort=COL]\n\n'
        '   or: tagfile list [-h | --help]'
    )
    description = f'{__doc__}\nBy default, the list is sorted on file path.'
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('show-hash', ('H', False, 'display column with checksum hash')),
        ('show-size', ('s', False, 'display column with filesizes')),
        ('show-type', ('t', False, 'display column with MIME type')),
        ('show-mime', ('m', False, 'display column with MIME type/subtype')),
        ('show-all', ('a', False, 'display hash, size, mime (same as -Hsm)')),
        ('sort', ('S', 'COL', 'sort on: name, hash, size, type or mime')),
        ('print0', ('0', False, 'end lines with null instead of newline')),
    )

    def run(self):
        if self.flags.help:
            tagfile.output.echo(self.usage)
            return 0

        if self.flags['show-all']:
            self.flags['show-hash'] = True
            self.flags['show-size'] = True
            self.flags['show-mime'] = True

        if self.flags.sort == 'name':
            query = Index.select().order_by(Index.basename)
        elif self.flags.sort == 'hash':
            query = Index.select().order_by(Index.filehash, Index.filepath)
        elif self.flags.sort == 'size':
            query = Index.select().order_by(Index.filesize, Index.filepath)
        elif self.flags.sort == 'type':
            query = Index.select().order_by(Index.cat, Index.filepath)
        elif self.flags.sort == 'mime':
            query = Index.select().order_by(Index.mime, Index.filepath)
        else:  # default / self.flags.sort == 'path'
            query = Index.select().order_by(Index.filepath)

        for i in query:
            if self.flags['print0']:
                sys.stdout.write(f'{i.filepath}\0')
                continue

            tagfile.repeat.print_filelist_row(self.flags, i)
        return 0
