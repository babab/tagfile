# file: tests/tagfile/test_config.py

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

import datetime
import os

import pytest
import yaml

from tagfile import common, config


_defaultconfigdict = yaml.safe_load(config.defaultconfig)
_testconfigpath = 'cache/tests/config/dir-{}'.format(
    datetime.datetime.now().toordinal()
)


def test_configuration_properties_uninitialized():
    assert config.Configuration.cfg == _defaultconfigdict
    assert config.Configuration.dirpath == common.TAGFILE_CONFIG_HOME
    assert config.Configuration.basename == 'config.yaml'
    assert config.Configuration.fullpath is None


def test_configuration_properties_initialized():
    obj = config.Configuration()
    assert obj.cfg == _defaultconfigdict
    assert obj.dirpath == common.TAGFILE_CONFIG_HOME
    assert obj.basename == 'config.yaml'
    assert obj.fullpath == os.path.join(common.TAGFILE_CONFIG_HOME,
                                        'config.yaml')


def test_configuration_method_set_paths():
    with2args = config.Configuration()
    with2args.set_paths('cache/tests/config/dirpath', 'custom.yml')
    assert with2args.dirpath == 'cache/tests/config/dirpath'
    assert with2args.basename == 'custom.yml'
    assert with2args.fullpath == 'cache/tests/config/dirpath/custom.yml'
    with1arg = config.Configuration()
    with1arg.set_paths('cache/tests/config/dirpath/tfconfig.yml')
    assert with1arg.dirpath == 'cache/tests/config/dirpath'
    assert with1arg.basename == 'tfconfig.yml'
    assert with1arg.fullpath == 'cache/tests/config/dirpath/tfconfig.yml'


def test_configuration_method_write_defaultconfig_with_makedirs_is_False():
    obj = config.Configuration()
    obj.set_paths('cache/tests/config/dirpath', 'custom.yml')
    with pytest.raises(common.ConfigError):
        obj.write_defaultconfig(makedirs=False)


def test_configuration_method_load_configfile_error_when_not_exists():
    obj = config.Configuration()
    obj.set_paths(_testconfigpath, 'custom.yml')
    with pytest.raises(common.ConfigError):
        obj.load_configfile()


def test_configuration_method_write_defaultconfig_with_makedirs_is_True():
    obj = config.Configuration()
    obj.set_paths(_testconfigpath, 'custom.yml')
    obj.write_defaultconfig()
    assert os.path.exists(obj.fullpath)


def test_configuration_method_load_configfile_error_when_exists():
    obj = config.Configuration()
    obj.set_paths(_testconfigpath, 'custom.yml')
    obj.load_configfile()
    obj.cfg = _defaultconfigdict
