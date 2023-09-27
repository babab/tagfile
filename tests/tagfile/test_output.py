# file: tests/tagfile/test_output.py

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

import pytest

import tagfile

DEFAULT_CONFIG_LOGLEVEL = logging.WARNING


def test_var_VERBOSE():
    assert tagfile.output.VERBOSE is False


# mappings for strings to values of logging.* constants ######################

def test_function_lvlstr2int():
    assert tagfile.output.lvlstr2int('debug') == logging.DEBUG
    assert tagfile.output.lvlstr2int('info') == logging.INFO
    assert tagfile.output.lvlstr2int('warn') == logging.WARNING
    assert tagfile.output.lvlstr2int('warning') == logging.WARNING
    assert tagfile.output.lvlstr2int('error') == logging.ERROR
    assert tagfile.output.lvlstr2int('fatal') == logging.FATAL
    assert tagfile.output.lvlstr2int('critical') == logging.FATAL
    assert tagfile.output.lvlstr2int('abcdef') == logging.WARNING
    assert tagfile.output.lvlstr2int('banana') == logging.WARNING


def test_function_get_logfunc_for():
    assert tagfile.output.get_logfunc_for('debug') == logging.debug
    assert tagfile.output.get_logfunc_for('info') == logging.info
    assert tagfile.output.get_logfunc_for('warn') == logging.warning
    assert tagfile.output.get_logfunc_for('warning') == logging.warning
    assert tagfile.output.get_logfunc_for('error') == logging.error
    assert tagfile.output.get_logfunc_for('fatal') == logging.fatal
    assert tagfile.output.get_logfunc_for('critical') == logging.fatal
    assert tagfile.output.get_logfunc_for('abcdef') == logging.warning
    assert tagfile.output.get_logfunc_for('banana') == logging.warning


def test_function_configlvl():
    assert tagfile.output.configlvl() == DEFAULT_CONFIG_LOGLEVEL
    _logging_bak = tagfile.cfg['logging']  # save section
    del tagfile.cfg['logging']  # delete section
    with pytest.raises(tagfile.ConfigError):
        assert tagfile.output.configlvl() == DEFAULT_CONFIG_LOGLEVEL
    tagfile.cfg['logging'] = _logging_bak  # re-insert section
    assert tagfile.output.configlvl() == DEFAULT_CONFIG_LOGLEVEL


# generic functions for verbose echo and logging #############################

def test_function_vecho_fatal_level(capfd):
    '''Always output regardless of verbose'''
    tagfile.output.vecho('fatal', 'some fatal thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'fatal error: some fatal thing happened\n'


def test_function_vecho_other_levels_not_verbose(capfd):
    '''No output when not verbose'''
    tagfile.output.vecho('debug', 'some debug thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''

    tagfile.output.vecho('info', 'some info thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''

    tagfile.output.vecho('warning', 'some warning thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''

    tagfile.output.vecho('error', 'some error thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''


def test_function_vecho_other_levels_verbose(capfd):
    '''Output when verbose'''
    tagfile.output.VERBOSE = True

    tagfile.output.vecho('debug', 'some debug thing happened')
    cap = capfd.readouterr()
    assert cap.out == 'some debug thing happened\n'
    assert cap.err == ''

    tagfile.output.vecho('info', 'some info thing happened')
    cap = capfd.readouterr()
    assert cap.out == 'some info thing happened\n'
    assert cap.err == ''

    tagfile.output.vecho('warning', 'some warning thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'warning: some warning thing happened\n'

    tagfile.output.vecho('error', 'some error thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'error: some error thing happened\n'

    tagfile.output.VERBOSE = False
