# file: tests/tagfile/commands/test_listcmd.py

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

from tagfile.commands.listcmd import ListCommand as Command


output_help = (
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


def test_command_help_flag_shows_help_message(capfd):
    cmd = Command(['-h'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help == cap.out
