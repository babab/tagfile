# file: tests/tagfile/commands/test_help.py

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
import pytest

from tagfile.commands.main_cmd import HelpCommand as Command


output_help_main = (
    '''Usage: tagfile [--config <filename>] [--db <name>] <command>
   or: tagfile [-h | --help] | [-V | --version]

Search, index and tag your files and find duplicates

Options:
--config=<filename>  use specified config file
--db=<name>          use database <name>, defined in config file
-h, --help           show this help information
-V, --version        show version and platform information

Commands:
  add        add a directory to media paths
  clones     show all indexed duplicate files
  find       find files according to certain criterias
  help       show help information
  info       show statistics for index and media paths
  list       show all indexed files
  updatedb   scan media paths and index newly added files
  version    show version and platform information

See 'tagfile help <command>' for more information on a
specific command, before using it.

''')

output_help_help = '''usage: tagfile help [<command>]

Show usage information (for subcommands)

Options:
-h, --help  show usage information for help command

'''

output_help_version = '''usage: tagfile version [-h | --help]

Show version and platform information

Options:
-h, --help  show this help information

'''

output_help_add = '''usage: tagfile add [-q | --quiet] [--scan] <media-path>
   or: tagfile add [-h | --help]

Add a directory to media paths (to be scanned later or right away)

Options:
-h, --help   show this help information
--scan       scan path now (this may take a long time)
-q, --quiet  print nothing except fatal errors

'''

output_help_clones = (
    'usage: tagfile clones [-s | --show-size] [-t | --show-type]'
    ''' [-m | --show-mime]
   or: tagfile clones [-h | --help]

Show all indexed duplicate files

Options:
-h, --help       show this help information
-s, --show-size  display column with filesizes
-t, --show-type  display column with MIME type
-m, --show-mime  display column with MIME type/subtype

''')

output_help_find = (
    '''usage: tagfile find [--type=TYPE] [--mime=MIMETYPE] [--size-gt=BYTES]
                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]
                    [--name=NAME | --in-name=STRING] [-H | --show-hash]
                    [-s | --show-size] [-t | --show-type] [-m | --show-mime]
                    [-a | --show-all] [-S COL | --sort=COL] [--reverse]

   or: tagfile find [--type=TYPE] [--mime=MIMETYPE] [--size-gt=BYTES]
                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]
                    [--name=NAME | --in-name=STRING] [-0 | --print0]
                    [-S COL | --sort=COL] [--reverse]

   or: tagfile find [-h | --help]

Find files according to certain criterias

Options:
-h, --help          show this help information
--type=TYPE         match files on 1st part of MIME type
--mime=MIMETYPE     match files on full MIME type/subtype
--size-gt=BYTES     match files where size is greater than BYTES
--size-lt=BYTES     match files where size is lesser than BYTES
--hash=HEX          match files where checksum is (or starts with) HEX
--in-path=STRING    match absolute paths with a substring of STRING
--name=NAME         match filenames that are exactly NAME
--in-name=STRING    match filenames with a substring of STRING
-H, --show-hash     display column with checksum hash
-s, --show-size     display column with filesizes
-t, --show-type     display column with MIME type
-m, --show-mime     display column with MIME type/subtype
-a, --show-all      display hash, size, mime (same as -Hsm)
-S COL, --sort=COL  sort on: name, hash, size, type or mime
--reverse           reverse sort order
-0, --print0        end lines with null instead of newline

''')

output_help_info = '''usage: tagfile info [-C | --show-config]
   or: tagfile info [-h | --help]

Show media paths, user config and statistics for index.

Options:
-h, --help         show this help information
-C, --show-config  pretty print active config in python

'''

output_help_list = (
    'usage: tagfile list [-H | --show-hash] [-s | --show-size] '
    '''[-t | --show-type]
                    [-m | --show-mime] [-a | --show-all] [-S COL | --sort=COL]
                    [--reverse]

   or: tagfile list [-0 | --print0] [-S COL | --sort=COL] [--reverse]

   or: tagfile list [-h | --help]

Output a list of all indexed files.
By default, the list is sorted on file path.

Options:
-h, --help          show this help information
-H, --show-hash     display column with checksum hash
-s, --show-size     display column with filesizes
-t, --show-type     display column with MIME type
-m, --show-mime     display column with MIME type/subtype
-a, --show-all      display hash, size, mime (same as -Hsm)
-S COL, --sort=COL  sort on: name, hash, size, type or mime
--reverse           reverse sort order
-0, --print0        end lines with null instead of newline

''')

output_help_updatedb = (
    '''usage: tagfile updatedb [--prune] [--scan] [-v, --verbose] [-q, --quiet]
   or: tagfile updatedb [-h | --help]

Scan all media paths. Index added files and prune removed files.

Use the option `--prune` if you only want to remove entries
from the index if files are missing. Use the option `--scan`
to only scan for newly added files without pruning.

Options:
-h, --help     show this help information
--prune        prune removed files only; don't scan
--scan         scan for new files only; don't prune
-v, --verbose  print message for all actions
-q, --quiet    print nothing except fatal errors

When no options are specified, updatedb will both scan and prune.
It will always prune deleted files before scanning for new files.

''')


def test_flags_are_None_by_default():
    cmd = Command([])
    assert cmd.flags['help'] is None


def test_error_is_None_by_default():
    cmd = Command(['-h'])
    assert cmd.error is None


def test_help_bool_flag_is_True_or_None():
    '''When a flag is given, it's value should be True, else None'''
    cmd = Command(['-h'])
    assert cmd.flags['help'] is True

    cmd = Command([''])
    assert cmd.flags['help'] is None


def test_bool_flags_with_1_option():
    cmd = Command(['-h'])
    assert cmd.flags['help'] is True


def test_flags_are_accessible_by_attribute():
    cmd = Command(['-h'])
    assert cmd.flags.help is True


def test_optionerror_on_unset_flags_attributes():
    cmd = Command(['-h'])
    with pytest.raises(pycommand.OptionError):
        assert cmd.flags.doesnotexist is None


def test_command_shows_main_help_when_no_args(capfd):
    cmd = Command([])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_main == cap.out


def test_command_help_flag_shows_help_message(capfd):
    cmd = Command(['-h'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_help == cap.out


def test_command_arg_help_shows_help_message(capfd):
    cmd = Command(['help'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_help == cap.out


def test_command_arg_version_shows_help_message(capfd):
    cmd = Command(['version'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_version == cap.out


def test_command_arg_add_shows_help_message(capfd):
    cmd = Command(['add'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_add == cap.out


def test_command_arg_clones_shows_help_message(capfd):
    cmd = Command(['clones'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_clones == cap.out


def test_command_arg_find_shows_help_message(capfd):
    cmd = Command(['find'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_find == cap.out


def test_command_arg_info_shows_help_message(capfd):
    cmd = Command(['info'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_info == cap.out


def test_command_arg_list_shows_help_message(capfd):
    cmd = Command(['list'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_list == cap.out


def test_command_arg_updatedb_shows_help_message(capfd):
    cmd = Command(['updatedb'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help_updatedb == cap.out


def test_invalid_command_arg(capfd):
    cmd = Command(['notacommand'])
    cmd.run()
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'error: Unknown command\n'
