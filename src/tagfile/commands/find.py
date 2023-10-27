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

import sys

import pycommand

from tagfile import output
import tagfile.repeat
from tagfile.models import Index


class FindCommand(pycommand.CommandBase):
    '''Find files according to certain criterias'''
    usagestr = (
        'usage: tagfile find [--type=TYPE] [--mime=MIMETYPE] '
        '[--size-gt=BYTES]\n'
        '{pad} [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]\n'
        '{pad} [--name=NAME | --in-name=STRING] [-H | --show-hash]\n'
        '{pad} [-s | --show-size] [-t | --show-type] [-m | --show-mime]\n'
        '{pad} [-a | --show-all] [-S COL | --sort=COL] [--reverse]\n\n'
        '   or: tagfile find [--type=TYPE] [--mime=MIMETYPE] '
        '[--size-gt=BYTES]\n'
        '{pad} [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]\n'
        '{pad} [--name=NAME | --in-name=STRING] [-0 | --print0]\n'
        '{pad} [-S COL | --sort=COL] [--reverse]\n\n'
        '   or: tagfile find [-h | --help]'
    ).format(pad=' ' * 19)
    description = __doc__
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('type', ('', 'TYPE',
                  'match files on 1st part of MIME type')),
        ('mime', ('', 'MIMETYPE',
                  'match files on full MIME type/subtype')),
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

        ('show-hash', ('H', False, 'display column with checksum hash')),
        ('show-size', ('s', False, 'display column with filesizes')),
        ('show-type', ('t', False, 'display column with MIME type')),
        ('show-mime', ('m', False, 'display column with MIME type/subtype')),
        ('show-all', ('a', False, 'display hash, size, mime (same as -Hsm)')),
        ('sort', ('S', 'COL', 'sort on: name, hash, size, type or mime')),
        ('reverse', ('', False, 'reverse sort order')),
        ('print0', ('0', False, 'end lines with null instead of newline')),
    )

    def run(self):
        if self.flags.help:
            output.echo(self.usage)
            return 0

        if self.flags['show-all']:
            self.flags['show-hash'] = True
            self.flags['show-size'] = True
            self.flags['show-mime'] = True

    # handle matching flags and build WHERE statement
        fields = []
        params = []
        valid_args = False
        if self.flags.type:
            valid_args = True
            fields.append('`cat` = ?')
            params.append(self.flags.type)
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

        # Stop and show error if no (valid) matching options are given
        if not valid_args:
            output.lnerr('error: command find requires one or more options\n')
            output.lnerr(self.usage, hl=False)
            return 1

    # handle sort flag and build ORDER BY statement ######################
        a_d = 'DESC' if self.flags.reverse else ''
        sortcol = f'`filepath` {a_d}'
        if self.flags.sort == 'name':
            sortcol = f'`basename` {a_d}'
        elif self.flags.sort == 'hash':
            sortcol = f'`filehash` {a_d}, `filepath`'
        elif self.flags.sort == 'size':
            sortcol = f'`filesize` {a_d}'
        elif self.flags.sort == 'type':
            sortcol = f'`cat` {a_d}, `filepath`'
        elif self.flags.sort == 'mime':
            sortcol = f'`mime` {a_d}, `filepath`'

    # all passed args are valid, create query and output rows ############
        statement = "SELECT * FROM `index` WHERE {} ORDER BY {}".format(
            ' AND '.join(fields), sortcol
        )
        output.log('debug', f'find built SQL statement: {statement}')
        query = Index.raw(statement, *params)

        for i in query:
            if self.flags['print0']:
                output.sout(f'{i.filepath}\0', hl=False)
                sys.stdout.write(f'{i.filepath}\0')
                continue

            tagfile.repeat.print_filelist_row(self.flags, i)
        return 0
