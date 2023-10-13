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
import rich.console
import rich.theme

import tagfile
import tagfile.output
from tagfile.common import ConfigError

DEFAULT_CONFIG_LOGLEVEL = logging.WARNING


def test_var_theme():
    assert isinstance(tagfile.output.theme, rich.theme.Theme)


def test_flags_quiet():
    assert tagfile.output.flags.quiet is False


def test_flags_verbose():
    assert tagfile.output.flags.verbose is False


def test_var_consout():
    assert isinstance(tagfile.output.consout, rich.console.Console)


def test_var_conserr():
    assert isinstance(tagfile.output.conserr, rich.console.Console)


def test_function_update_consoles_with_default_flags_dot_quiet_value():
    tagfile.output.flags.update_consoles()
    assert tagfile.output.consout.quiet is False
    assert tagfile.output.conserr.quiet is False


def test_function_update_consoles_is_called_when_quiet_is_changed():
    '''update_consoles is called in the setter for quiet'''
    tagfile.output.flags.quiet = True
    assert tagfile.output.consout.quiet is True
    assert tagfile.output.conserr.quiet is True
    # reset
    tagfile.output.flags.quiet = False
    assert tagfile.output.consout.quiet is False
    assert tagfile.output.conserr.quiet is False


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
    with pytest.raises(ConfigError):
        assert tagfile.output.configlvl() == DEFAULT_CONFIG_LOGLEVEL
    tagfile.cfg['logging'] = _logging_bak  # re-insert section
    assert tagfile.output.configlvl() == DEFAULT_CONFIG_LOGLEVEL


# generic functions for printing to console without logging  #################

# function sout
def test_function_sout_regular(capfd):
    tagfile.output.sout('this is a string without ending newline')
    cap = capfd.readouterr()
    assert cap.out == 'this is a string without ending newline'
    assert cap.err == ''


def test_function_sout_regular_multiple_args(capfd):
    tagfile.output.sout('this is a', 'string without', 'ending newline')
    cap = capfd.readouterr()
    assert cap.out == 'this is a string without ending newline'
    assert cap.err == ''


def test_function_sout_regular_when_quiet(capfd):
    tagfile.output.flags.quiet = True
    tagfile.output.sout('this is a string without ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''
    tagfile.output.flags.quiet = False


def test_function_sout_colored_string_supressed(capfd):
    tagfile.output.sout('[red]red colored output[/]')
    cap = capfd.readouterr()
    assert cap.out == 'red colored output'
    assert cap.err == ''


def test_function_sout_colored_string_forced(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.sout('[red]red colored output[/]')
    cap = capfd.readouterr()
    assert cap.out == '\x1b[31mred colored output\x1b[0m'
    assert cap.err == ''
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


def test_function_sout_colored_string_forced_hl_is_True(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.sout('/tmp/tagfile/sample-3.mp4', hl=True)
    cap = capfd.readouterr()
    assert cap.out == (
        '\x1b[38;5;143m/tmp/tagfile/\x1b[0m\x1b[38;5;185msample-3.mp4\x1b[0m'
    )
    assert cap.err == ''
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


# function lnout
def test_function_lnout_regular(capfd):
    tagfile.output.lnout('this is a string with ending newline')
    cap = capfd.readouterr()
    assert cap.out == 'this is a string with ending newline\n'
    assert cap.err == ''


def test_function_lnout_regular_multiple_args(capfd):
    tagfile.output.lnout('this is a', 'string with', 'ending newline')
    cap = capfd.readouterr()
    assert cap.out == 'this is a string with ending newline\n'
    assert cap.err == ''


def test_function_lnout_regular_when_quiet(capfd):
    tagfile.output.flags.quiet = True
    tagfile.output.lnout('this is a string with ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''
    tagfile.output.flags.quiet = False


def test_function_lnout_colored_string_supressed(capfd):
    tagfile.output.lnout('[blue]blue colored output line[/]')
    cap = capfd.readouterr()
    assert cap.out == 'blue colored output line\n'
    assert cap.err == ''


def test_function_lnout_colored_string_forced(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.lnout('[blue]blue colored output line[/]')
    cap = capfd.readouterr()
    assert cap.out == '\x1b[34mblue colored output line\x1b[0m\n'
    assert cap.err == ''
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


def test_function_lnout_colored_string_forced_hl_is_True(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.lnout('/tmp/tagfile/sample-3.mp4', hl=True)
    cap = capfd.readouterr()
    assert cap.out == (
        '\x1b[38;5;143m/tmp/tagfile/\x1b[0m\x1b[38;5;185msample-3.mp4\x1b[0m\n'
    )
    assert cap.err == ''
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


# function serr
def test_function_serr_regular(capfd):
    tagfile.output.serr('this is a string without ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'this is a string without ending newline'


def test_function_serr_regular_multiple_args(capfd):
    tagfile.output.serr('this is a', 'string without', 'ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'this is a string without ending newline'


def test_function_serr_regular_when_quiet(capfd):
    tagfile.output.flags.quiet = True
    tagfile.output.serr('this is a string without ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''
    tagfile.output.flags.quiet = False


def test_function_serr_regular_when_quiet_with_ignore_quiet_override(capfd):
    tagfile.output.flags.quiet = True
    tagfile.output.serr('this is a string without ending newline',
                        ignore_quiet=True)
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'this is a string without ending newline'
    tagfile.output.flags.quiet = False
    assert tagfile.output.flags.quiet is False


def test_function_serr_colored_string_supressed(capfd):
    tagfile.output.serr('[cyan]cyan colored output[/]')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'cyan colored output'


def test_function_serr_colored_string_forced(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.serr('[cyan]cyan colored output[/]')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == '\x1b[36mcyan colored output\x1b[0m'
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


def test_function_serr_colored_string_forced_hl_is_True(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.serr('/tmp/tagfile/sample-3.mp4', hl=True)
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == (
        '\x1b[38;5;143m/tmp/tagfile/\x1b[0m\x1b[38;5;185msample-3.mp4\x1b[0m'
    )
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


# function lnerr
def test_function_lnerr_regular(capfd):
    tagfile.output.lnerr('this is a string with ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'this is a string with ending newline\n'


def test_function_lnerr_regular_multiple_args(capfd):
    tagfile.output.lnerr('this is a', 'string with', 'ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'this is a string with ending newline\n'


def test_function_lnerr_regular_when_quiet(capfd):
    tagfile.output.flags.quiet = True
    tagfile.output.lnerr('this is a string with ending newline')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == ''
    tagfile.output.flags.quiet = False


def test_function_lnerr_regular_when_quiet_with_ignore_quiet_override(capfd):
    tagfile.output.flags.quiet = True
    tagfile.output.lnerr('this is a string with ending newline',
                         ignore_quiet=True)
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'this is a string with ending newline\n'
    tagfile.output.flags.quiet = False


def test_function_lnerr_colored_string_supressed(capfd):
    tagfile.output.lnerr('[magenta]magenta colored output line[/]')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == 'magenta colored output line\n'


def test_function_lnerr_colored_string_forced(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.lnerr('[magenta]magenta colored output line[/]')
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == '\x1b[35mmagenta colored output line\x1b[0m\n'
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


def test_function_lnerr_colored_string_forced_hl_is_True(capfd):
    tagfile.output.flags.update_consoles_for_testing(force_term=True)
    tagfile.output.lnerr('/tmp/tagfile/sample-3.mp4', hl=True)
    cap = capfd.readouterr()
    assert cap.out == ''
    assert cap.err == (
        '\x1b[38;5;143m/tmp/tagfile/\x1b[0m\x1b[38;5;185msample-3.mp4\x1b[0m\n'
    )
    tagfile.output.flags.update_consoles_for_testing(force_term=False)


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
    tagfile.output.flags.verbose = True

    tagfile.output.vecho('debug', 'some debug thing happened')
    cap = capfd.readouterr()
    assert cap.out == ''
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

    tagfile.output.flags.verbose = False
