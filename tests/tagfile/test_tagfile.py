# file: tests/tagfile/test_tagfile.py

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

import tagfile
from tagfile import common
from tagfile.commands.main_cmd import entry


output_help_help = '''usage: tagfile help [<command>]

Show usage information (for subcommands)

Options:
-h, --help  show usage information for help command

'''


def test_default_cfg_structure():
    cfg = tagfile.cfg
    assert cfg['logging']['enabled'] is True
    assert cfg['logging']['file']
    assert cfg['logging']['level'] == 'warning'
    assert cfg['show']
    assert type(cfg['show']) is dict
    assert len(cfg['show']) == 1
    assert cfg['show']['progressbars'] is True
    assert cfg['ignore']
    assert type(cfg['ignore']) is dict
    assert len(cfg['ignore']) == 2
    assert cfg['ignore']['empty-files'] is True
    assert cfg['ignore']['name-based']
    assert type(cfg['ignore']['name-based']) is dict
    assert len(cfg['ignore']['name-based']) == 3
    assert cfg['ignore']['name-based']['paths']
    assert type(cfg['ignore']['name-based']['paths']) is list
    assert cfg['ignore']['name-based']['filenames']
    assert type(cfg['ignore']['name-based']['filenames']) is list
    assert cfg['ignore']['name-based']['extensions']
    assert type(cfg['ignore']['name-based']['extensions']) is list


def test_location_variables():
    assert common.TAGFILE_DATA_HOME is not None
    assert common.TAGFILE_CONFIG_HOME is not None


def test_location_paths_have_been_created():
    assert os.path.exists(common.TAGFILE_DATA_HOME)
    assert os.path.exists(common.TAGFILE_CONFIG_HOME)


def test_entry_help_help(capfd):
    exitcode = entry(['help', 'help'])
    assert exitcode == 0
    cap = capfd.readouterr()
    assert cap.out == output_help_help
    assert cap.err == ''


def test_entry_invalid_flag(capfd):
    exitcode = entry(['-Z'])
    assert exitcode == 1
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'error: option -Z not recognized\n'
