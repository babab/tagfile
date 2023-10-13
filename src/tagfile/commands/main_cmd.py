# file: src/tagfile/commands/main_cmd.py

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

import pycommand

import tagfile
from tagfile import __doc__ as main_description
from tagfile.output import (
    lnerr,
    lnout,
)
from tagfile.commands.add import AddCommand
from tagfile.commands.clones import ClonesCommand
from tagfile.commands.find import FindCommand
from tagfile.commands.info import InfoCommand
from tagfile.commands.updatedb import UpdateDbCommand


def entry(argv='sys_argv'):
    '''Defining a param with a default like ``argv=sys.argv[1:]`` can
    throw off documentation generators. As a workaround, a string of
    sys_argv is interpreted as an alias for ``sys.argv[1:]``.
    In all other cases, argv should be of type list.
    '''
    argv = sys.argv[1:] if argv == 'sys_argv' else argv
    try:
        cmd = Command(argv)
        if cmd.error:
            lnerr('error: {0}'.format(cmd.error))
            return 1
        else:
            return cmd.run()
    except KeyboardInterrupt:
        lnerr('\nUser interrupted. Tagfile successfully exited.')
        return 0


class HelpCommand(pycommand.CommandBase):
    usagestr = 'usage: tagfile help [<command>]'
    description = 'Show usage information (for subcommands)'
    optionList = (
        ('help', ('h', False, 'show usage information for help command')),
    )

    def run(self):
        if self.flags['help']:
            print(self.usage)
            return 0

        if self.args:
            if self.args[0] == 'help':
                print(self.usage)
            elif self.args[0] == 'version':
                print(VersionCommand([]).usage)
            elif self.args[0] == 'add':
                print(AddCommand([]).usage)
            elif self.args[0] == 'clones':
                print(ClonesCommand([]).usage)
            elif self.args[0] == 'find':
                print(FindCommand([]).usage)
            elif self.args[0] == 'info':
                print(InfoCommand([]).usage)
            elif self.args[0] == 'updatedb':
                print(UpdateDbCommand([]).usage)
            else:
                lnerr('error: Unknown command')
                return 1
        else:
            print(Command([]).usage)
        return 0


class VersionCommand(pycommand.CommandBase):
    usagestr = 'usage: tagfile version [-h | --help]'
    description = 'Show version and platform information'
    optionList = (
        ('help', ('h', False, 'show this help information')),
    )

    def run(self):
        if self.flags['help']:
            print(self.usage)
            return 0

        print(tagfile.verboseVersionInfo())
        return 0


class Command(pycommand.CommandBase):
    '''Argument handler based on pycommand'''
    usagestr = (
        'Usage: tagfile [--config <filename>] <command>\n'
        '   or: tagfile [-h | --help] | [-V | --version]'
    )
    description = main_description
    commands = {
        # from this module
        'help': HelpCommand,
        'version': VersionCommand,
        # from commands package
        'add': AddCommand,
        'clones': ClonesCommand,
        'find': FindCommand,
        'info': InfoCommand,
        'updatedb': UpdateDbCommand,
    }
    optionList = (
        ('config', ('', '<filename>', 'use specified config file')),
        ('help', ('h', False, 'show this help information')),
        ('version', ('V', False, 'show version and platform information')),
    )
    usageTextExtra = (
        'Commands:\n'
        '  add        add a directory to media paths\n'
        '  clones     show all indexed duplicate files\n'
        '  find       find files according to certain criterias\n'
        '  help       show help information\n'
        '  info       show statistics for index and media paths\n'
        '  updatedb   scan media paths and index newly added files\n'
        '  version    show version and platform information\n'

        "\nSee 'tagfile help <command>' for more information on a\n"
        'specific command, before using it.\n'
    )

    def run(self):
        '''Run from shell; main application program flow.'''

        # Flags that will print and exit
        if self.flags['help']:
            print(self.usage)
            return 0
        elif self.flags['version']:
            print(tagfile.verboseVersionInfo())
            return 0

        # Update cfg with file
        if self.flags['config']:
            _fpath = os.path.abspath(self.flags['config'])
            if os.path.exists(_fpath):
                tagfile.configuration.set_paths(_fpath)
                tagfile.configuration.load_configfile()
            else:
                lnerr(f'error: file {_fpath} does not exist.')
                return 2

        # temporary handling of old commands, the super call will catch
        # and handle these further with 'error: unknown command'
        try:
            command = self.args[0]
        except IndexError:
            command = None
        if command == 'scan':
            lnout(
                "Command 'scan' is removed. The equivalent to 'scan' is\n"
                "now 'tagfile add --scan .'. Use 'tagfile updatedb --scan'\n"
                'to scan all known media-paths regardless of current dir.\n'
            )
        elif command == 'same':
            lnout("Command 'same' is renamed. Please use 'clones' instead.")
        elif command == 'stats':
            lnout("Command 'stats' is renamed. Please use 'info' instead.")
        elif command == 'prune':
            lnout(
                "Command 'prune' is removed. The equivalent to 'prune' is\n"
                "now 'tagfile updatedb --prune'.\n"
            )

        # parse commands in pycommand style
        try:
            cmd = super(Command, self).run()
        except pycommand.CommandExit as e:
            return e.err

        cmd.registerParentFlag('config', self.flags.config)

        if cmd.error:
            lnerr('tagfile {cmd}: {error}'
                  .format(cmd=self.args[0], error=cmd.error))
            return 1
        else:
            return cmd.run()


if __name__ == '__main__':
    sys.exit(entry())
