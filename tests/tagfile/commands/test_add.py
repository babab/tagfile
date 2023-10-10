# file: tests/tagfile/commands/test_add.py

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
import pytest

import tagfile.output
from tagfile.commands.add import AddCommand as Command

TAGFILE_CONFIG_HOME = os.environ['TAGFILE_CONFIG_HOME']
TAGFILE_DATA_HOME = os.environ['TAGFILE_DATA_HOME']
TAGFILEDEV_MEDIA_PATH = os.environ['TAGFILEDEV_MEDIA_PATH']


output_help = '''usage: tagfile add [-q | --quiet] [--scan] <media-path>
   or: tagfile add [-h | --help]

Add a directory to media paths (to be scanned later or right away)

Options:
-h, --help   show this help information
--scan       scan path now (this may take a long time)
-q, --quiet  print nothing except fatal errors

'''

output_noargs = '''error: command add requires argument

To add and scan current dir, use `tagfile add --scan .`
See `tagfile help add` OR `tagfile add -h` for more info.
'''

output_add_tmp_tagfiletests = '''Added media path: {}
'''.format(TAGFILEDEV_MEDIA_PATH)

output_doesnotexist = '''Could not add media path: /tagfile/OhhcJ11KPwWqfLb4

error: media path does not exist
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


def test_pycommand_bool_flags_with_2_options():
    cmd = Command(['-h', '--scan'])
    assert cmd.flags['help'] is True
    assert cmd.flags['scan'] is True


def test_pycommand_flags_are_accessible_by_attribute():
    cmd = Command(['-h'])
    assert cmd.flags.help is True
    assert cmd.flags.scan is None


def test_pycommand_optionerror_on_unset_flags_attributes():
    cmd = Command(['-h'])
    with pytest.raises(pycommand.OptionError):
        assert cmd.flags.doesnotexist is None


def test_pycommand_command_shows_message_when_no_args(capfd):
    cmd = Command([])
    cmd.run()
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == output_noargs


def test_pycommand_command_help_flag_shows_help_message(capfd):
    cmd = Command(['-h'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help == cap.out


def test_media_path_arg_will_add_path_to_repos_if_valid(capfd):
    import tagfile
    cmd = Command([TAGFILEDEV_MEDIA_PATH])
    cmd.run()
    cap = capfd.readouterr()
    assert output_add_tmp_tagfiletests == cap.out
    assert tagfile.core.tfman.paths[0].startswith(TAGFILEDEV_MEDIA_PATH)


def test_media_path_arg_will_show_error_if_not_exists(capfd):
    cmd = Command(['/tagfile/OhhcJ11KPwWqfLb4'])
    returncode = cmd.run()
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == output_doesnotexist
    assert returncode == 4


def test_quiet_flag_blocks_output_and_cascades_to_consoles_correctly(capfd):
    # check default value
    assert tagfile.output.flags.quiet is False
    assert tagfile.output.consout.quiet is False
    assert tagfile.output.conserr.quiet is False
    # set quiet through command flag
    cmd = Command(['-q'])
    exitcode = cmd.run()
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''
    assert cmd.flags.quiet is True
    assert exitcode == 1
    assert tagfile.output.flags.quiet is True
    assert tagfile.output.consout.quiet is True
    assert tagfile.output.conserr.quiet is True
    cmd = Command(['--quiet'])
    exitcode = cmd.run()
    assert cmd.flags.quiet is True
    assert exitcode == 1
    assert tagfile.output.flags.quiet is True
    assert tagfile.output.consout.quiet is True
    assert tagfile.output.conserr.quiet is True
    # reset to default value
    tagfile.output.flags.quiet = False
    assert tagfile.output.flags.quiet is False
