# file: tests/tagfile/commands/test_find.py

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

from tagfile.commands.find import FindCommand as Command


output_help = (
    '''usage: tagfile find [--type=TYPE] [--mime=MIMETYPE] [--size-gt=BYTES]
                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]
                    [--name=NAME | --in-name=STRING] [-H | --show-hash]
                    [-s | --show-size] [-t | --show-type] [-m | --show-mime]
                    [-a | --show-all] [-S COL | --sort=COL]

   or: tagfile find [--type=TYPE] [--mime=MIMETYPE] [--size-gt=BYTES]
                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]
                    [--name=NAME | --in-name=STRING] [-0 | --print0]
                    [-S COL | --sort=COL]

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
-0, --print0        end lines with null instead of newline

''')

output_noargs = '''error: command find requires one or more options

''' + output_help


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


def test_bool_flag_for_help():
    cmd = Command(['-h'])
    assert cmd.flags['help'] is True
    cmd = Command(['--help'])
    assert cmd.flags['help'] is True


def test_type_option_string_as_2_args():
    cmd = Command(['--type', 'text'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] == 'text'
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_type_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--type=text'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] == 'text'
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_mime_option_string_as_2_args():
    cmd = Command(['--mime', 'video/mp4'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] == 'video/mp4'
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_mime_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--mime=video/mp4'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] == 'video/mp4'
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_sizegt_option_string_as_2_args():
    cmd = Command(['--size-gt', '6000'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] == '6000'
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_sizegt_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--size-gt=6000'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] == '6000'
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_sizelt_option_string_as_2_args():
    cmd = Command(['--size-lt', '1_024_000'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] == '1_024_000'
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_sizelt_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--size-lt=1_024_000'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] == '1_024_000'
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_hash_option_string_as_2_args():
    cmd = Command(['--hash', '0d7'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] == '0d7'
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_hash_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--hash=0d7'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] == '0d7'
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_inpath_option_string_as_2_args():
    cmd = Command(['--in-path', 'cache/media'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] == 'cache/media'
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_inpath_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--in-path=cache/media'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] == 'cache/media'
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] is None


def test_name_option_string_as_2_args():
    cmd = Command(['--name', 'sample3.mp4'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] == 'sample3.mp4'
    assert cmd.flags['in-name'] is None


def test_name_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--name=sample3.mp4'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] == 'sample3.mp4'
    assert cmd.flags['in-name'] is None


def test_inname_option_string_as_2_args():
    cmd = Command(['--in-name', 'sample3'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] == 'sample3'


def test_inname_option_string_as_1_arg_with_equals_sign():
    cmd = Command(['--in-name=sample3'])
    assert cmd.flags['help'] is None
    assert cmd.flags['type'] is None
    assert cmd.flags['mime'] is None
    assert cmd.flags['size-gt'] is None
    assert cmd.flags['size-lt'] is None
    assert cmd.flags['hash'] is None
    assert cmd.flags['in-path'] is None
    assert cmd.flags['name'] is None
    assert cmd.flags['in-name'] == 'sample3'


def test_flags_are_accessible_by_attribute():
    cmd = Command(['-h'])
    assert cmd.flags.help is True


def test_optionerror_on_unset_flags_attributes():
    cmd = Command(['-h'])
    with pytest.raises(pycommand.OptionError):
        assert cmd.flags.doesnotexist is None


def test_command_shows_error_message_when_no_args(capfd):
    cmd = Command([])
    cmd.run()
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == output_noargs


def test_command_help_flag_shows_help_message(capfd):
    cmd = Command(['-h'])
    cmd.run()
    cap = capfd.readouterr()
    assert output_help == cap.out
