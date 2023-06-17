# file: src/tagfile/commands/main.py

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

import logging
import os
import sys

import pycommand
import yaml

from tagfile import config, verboseVersionInfo, __doc__ as main_description
from tagfile.core import tfman
from tagfile.commands.add import AddCommand


def main():
    try:
        cmd = Command(sys.argv[1:])
        if cmd.error:
            print('error: {0}'.format(cmd.error))
            return 1
        else:
            return cmd.run()
    except KeyboardInterrupt:
        print('\nTagfile successfully exited.')
        return 0


class HelpCommand(pycommand.CommandBase):
    usagestr = 'usage: tagfile help [<command>]'
    description = 'Show help information'

    def run(self):
        if self.args:
            if self.args[0] == 'help':
                print(self.usage)
            elif self.args[0] == 'add':
                print(AddCommand([]).usage)
        else:
            print(Command([]).usage)


class Command(pycommand.CommandBase):
    '''Argument handler based on pycommand'''
    usagestr = 'Usage: tagfile <options>'
    description = main_description
    commands = {
        'add': AddCommand,
        'help': HelpCommand,
    }
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('version', ('', False, 'show version information')),
        ('config', ('', '<filename>', 'use specified config file')),
    )
    usageTextExtra = (
        'Commands:\n'
        '  help               show help information\n'
        '  scan               scan current directory and add to index\n'
        '  add <directory>    scan <directory> and add to index\n'
        '  find <string>      find all filenames for <string>\n'
        '  same               show all indexed duplicate files\n'
        '  stats              show statistics for index, repos and tags\n'
        '  prune              remove entries from index if files are missing'
    )

    def run(self):
        '''Run from shell; main application program flow.'''

        # Flags that will print and exit
        if self.flags['help']:
            print(self.usage)
            return
        elif self.flags['version']:
            print(verboseVersionInfo())
            return

        # Update config with file
        if self.flags['config']:
            fn = self.flags['config']
            if os.path.exists(fn):
                config.update(yaml.safe_load(open(fn).read()))
            else:
                print('ERROR: file does not exist')
                return 2

        # Setup logging
        logging.basicConfig(
            filename=os.path.expanduser(config['log-file']),
            level=logging.INFO, style='{',
            format='{asctime}:{levelname}: {message}'
        )

        try:
            command = self.args[0]
        except IndexError:
            command = None
        try:
            arg = self.args[1]
        except IndexError:
            arg = None

        if command == 'scan':
            tfman.addPath(os.getcwd())
            tfman.scan()
        elif command == 'find':
            if arg:
                tfman.find(arg)
            else:
                print('error: command find requires argument')
        elif command == 'same':
            tfman.same()
        elif command == 'stats':
            tfman.stats()
        elif command == 'prune':
            tfman.prune()

        # parse commands in pycommand style
        try:
            cmd = super(Command, self).run()
        except pycommand.CommandExit as e:
            return e.err

        cmd.registerParentFlag('config', self.flags.config)

        if cmd.error:
            print('tagfile {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()


if __name__ == '__main__':
    sys.exit(main())
