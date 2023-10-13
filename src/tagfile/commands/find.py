# file: src/tagfile/commands/find.py

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

from tagfile import files, output
from tagfile.models import Index


class FindCommand(pycommand.CommandBase):
    '''Find files according to certain criterias'''
    usagestr = (
        'usage: tagfile find [--cat=CAT] [--mime=MIMETYPE] [--size-gt=BYTES]\n'
        '                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]'
        '\n                    [--name=NAME | --in-name=STRING]\n'
        '   or: tagfile find [-h | --help]'
    )
    description = __doc__
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('cat', ('', 'CAT',
                 'match on category (1st part of MIME-type)')),
        ('mime', ('', 'MIMETYPE',
                  'match files on MIME-type')),
        ('size-gt', ('', 'BYTES',
                     'match files where size is greater than BYTES')),
        ('size-lt', ('', 'BYTES',
                     'match files where size is lesser than BYTES')),
        ('hash', ('', 'HEX',
                  'match files where checksum is (or starts with) HEX')),
        ('in-path', ('', 'STRING',
                     'match absolute paths with a substring of STRING')),
        ('name', ('', 'NAME',
                  'match filenames that are exactly NAME')),
        ('in-name', ('', 'STRING',
                     'match filenames with a substring of STRING')),
    )

    def run(self):
        if self.flags.help:
            output.echo(self.usage)
            return 0

        fields = []
        params = []
        valid_args = False
        if self.flags.cat:
            valid_args = True
            fields.append('`cat` = ?')
            params.append(self.flags.cat)
        if self.flags.mime:
            valid_args = True
            fields.append('`mime` = ?')
            params.append(self.flags.mime)
        if self.flags['size-gt']:
            valid_args = True
            fields.append('`filesize` > ?')
            params.append(self.flags['size-gt'])
        if self.flags['size-lt']:
            valid_args = True
            fields.append('`filesize` < ?')
            params.append(self.flags['size-lt'])
        if self.flags.hash:
            valid_args = True
            fields.append('`filehash` LIKE ?')
            params.append(f'{self.flags.hash}%')

        # Cannot use --name and --in-name simultaneously
        if self.flags.name:
            valid_args = True
            fields.append('`basename` = ?')
            params.append(self.flags.name)
        elif self.flags['in-name']:
            valid_args = True
            fields.append('`basename` LIKE ?')
            params.append(f'%{self.flags["in-name"]}%')

        if self.flags['in-path']:
            valid_args = True
            fields.append('`filepath` LIKE ?')
            params.append(f'%{self.flags["in-path"]}%')

        # Stop and show error if no (valid) options are given
        if not valid_args:
            output.lnerr('error: command find requires one or more options\n')
            output.lnerr(self.usage, hl=False)
            return 1

        # all passed args are valid, create query
        statement = "SELECT * FROM `index` WHERE {}".format(
            ' AND '.join(fields)
        )
        output.log('debug', f'find built SQL statement: {statement}')
        query = Index.raw(statement, *params)

        for i in query:
            _hash = i.filehash[:5]
            _size = ' {}'.format(files.sizefmt(i.filesize))
            _mime = ' {}'.format(i.mime)
            output.sout(f'[green]{_hash}[/][white]{_size}[/]', hl=False)
            output.lnout('{} {}'.format(_mime, i.filepath))
        return 0
