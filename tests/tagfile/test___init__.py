# file: tests/tagfile/test___init__.py

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

import tagfile
from tagfile import common

TFVERSION = '0.2.0a13'


def test_tagfile_package_version_author_copyright_in_namespace():
    assert tagfile.__version__ == TFVERSION
    assert tagfile.versionStr == 'tagfile {}'.format(TFVERSION)
    assert tagfile.__author__ == "Benjamin Althues"
    assert tagfile.__copyright__ == "Copyright (C) 2015-2023  Benjamin Althues"


def test_verboseVersionInfo():
    valid_output = '''{0}
{1}

Python {2}
Interpreter is at {3}
Platform is {4}'''.format(
        tagfile.versionStr,
        tagfile.__copyright__,
        sys.version.replace('\n', ''),
        sys.executable or 'unknown',
        os.name,
    )
    assert tagfile.verboseVersionInfo() == valid_output


def test_config_and_data_home_envvars_are_altered_for_testenvironment():
    assert os.environ.get('TAGFILE_DATA_HOME') is not None
    assert os.environ.get('TAGFILE_CONFIG_HOME') is not None


def test_defaultconfig_logging_settings():
    cfg = tagfile.cfg
    assert cfg['logging']['enabled'] is True
    assert cfg['logging']['level'] == 'warning'


def test_defaultconfig_logfile_is_altered_according_to_TAGFILE_DATA_HOME():
    tildepath = common.invertexpanduser(common.TAGFILE_DATA_HOME)
    cfg = tagfile.cfg
    assert cfg['logging']['file'] == '{}/tagfile.log'.format(tildepath)
