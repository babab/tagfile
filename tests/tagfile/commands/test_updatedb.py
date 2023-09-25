# file: tests/tagfile/commands/test_updatedb.py

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

from tagfile.commands.updatedb import UpdateDbCommand as Command


output_help = '''usage: tagfile updatedb [--prune] [--scan] [-v | --verbose]
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

When no options are specified, updatedb will both scan and prune.
It will always prune deleted files before scanning for new files.

'''


def test_pycommand_flags_are_None_by_default():
    cmd = Command([])
    assert cmd.flags['help'] is None


def test_pycommand_error_is_None_by_default():
    cmd = Command(['-h'])
    assert cmd.error is None


def test_pycommand_help_bool_flag_is_True_or_None():
    '''When a flag is given, it's value should be True, else None'''
    cmd = Command(['-h'])
    assert cmd.flags['help'] is True

    cmd = Command([''])
    assert cmd.flags['help'] is None


def test_pycommand_bool_flags_with_1_option():
    cmd = Command(['-h'])
    assert cmd.flags['help'] is True
    assert cmd.flags['scan'] is None
    assert cmd.flags['prune'] is None


def test_pycommand_bool_flags_with_2_options():
    cmd = Command(['-h', '--scan'])
    assert cmd.flags['help'] is True
    assert cmd.flags['scan'] is True
    assert cmd.flags['prune'] is None


def test_pycommand_bool_flags_with_3_options():
    cmd = Command(['--prune', '-h', '--scan'])
    assert cmd.flags['help'] is True
    assert cmd.flags['scan'] is True
    assert cmd.flags['prune'] is True


def test_pycommand_flags_are_accessible_by_attribute():
    cmd = Command(['--scan', '--prune', '-h'])
    assert cmd.flags.help is True
    assert cmd.flags.prune is True
    assert cmd.flags.scan is True


def test_pycommand_optionerror_on_unset_flags_attributes():
    cmd = Command(['-h'])
    with pytest.raises(pycommand.OptionError):
        assert cmd.flags.doesnotexist is None


def test_pycommand_command_help_flag_shows_help_message(capfd):
    cmd = Command(['-h'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help == cap.out
