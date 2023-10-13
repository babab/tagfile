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

import pycommand

import tagfile.core
import tagfile.files
from tagfile.models import Index
import tagfile.output


class ListCommand(pycommand.CommandBase):
    '''Show all indexed files.'''
    usagestr = (
        'usage: tagfile list [-s | --size] [-c | --cat] [-m | --mime]\n'
        '                    [-S COL | --sort=COL]\n'
        '   or: tagfile list [-h | --help]'
    )
    description = f'{__doc__}\nBy default, the list is sorted on file path.'
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('size', ('s', False, 'display column with filesizes')),
        ('cat', ('c', False, 'display column with media categories')),
        ('mime', ('m', False, 'display column with full mimetypes')),
        ('sort', ('S', 'COL', 'sort on: name, hash, size, cat or mime')),
    )

    def run(self):
        if self.flags.help:
            tagfile.output.echo(self.usage)
            return 0

        if self.flags.sort == 'name':
            query = Index.select().order_by(Index.basename)
        elif self.flags.sort == 'hash':
            query = Index.select().order_by(Index.filehash, Index.filepath)
        elif self.flags.sort == 'size':
            query = Index.select().order_by(Index.filesize)
        elif self.flags.sort == 'cat':
            query = Index.select().order_by(Index.cat, Index.filepath)
        elif self.flags.sort == 'mime':
            query = Index.select().order_by(Index.mime, Index.filepath)
        else:  # same as self.flags.sort == 'path'
            query = Index.select().order_by(Index.filepath)

        for i in query:
            _hash = i.filehash[:5]
            _size = ' {}'.format(
                tagfile.files.sizefmt(i.filesize)
            ) if self.flags.size else ''
            _cat = ' {}'.format(i.cat) if self.flags.cat else ''
            _mime = ' {}'.format(i.mime) if self.flags.mime else ''
            tagfile.output.lnout('[green]{}{}[/green]{}{} {}'.format(
                _hash, _size, _cat, _mime, i.filepath
            ))
        return 0
