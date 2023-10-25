# file: src/tagfile/output.py

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

from rich import console
from rich.theme import Theme

import tagfile
from tagfile.common import ConfigError


class OutputSettings:
    verbose = False
    '''Used to set state of verbose output when using -v command flags'''

    def __init__(self):
        self._quiet_bool = False

    @property
    def quiet(self):
        '''Used to supress all output, except fatal errors.'''
        return self._quiet_bool

    @quiet.setter
    def quiet(self, yesno):
        self._quiet_bool = bool(yesno)
        self.update_consoles()

    def update_consoles(self):
        '''Set properties of rich consoles to {en,dis}able progessbars etc.'''
        consout.quiet = self.quiet
        conserr.quiet = self.quiet

    def update_consoles_for_testing(self, force_term=None):
        '''Override console instances for unit and integration testing.

        - Use ``force_term=True`` to update the consoles.
        - Use ``force_term=False`` to reset the consoles after test is done.

        This is the only funtion in tagfile as a whole where the global
        keyword is used. It is essentially only ever used to force override
        colored output in `consout` and `conserr` for testing the prescence
        of ANSI escape sequences in the output with pytest. This is not to
        be used in regular program flow. Use `update_consoles()` instead.
        '''
        global consout, conserr
        if force_term is not None:
            terminal = True if force_term else None
            interactive = False if force_term else None
            consout = console.Console(theme=theme, force_terminal=terminal,
                                      force_interactive=interactive)
            conserr = console.Console(theme=theme, stderr=True,
                                      force_terminal=terminal,
                                      force_interactive=interactive)
        self.update_consoles()


theme = Theme({
    'repr.path': 'dark_khaki',
    'repr.filename': 'khaki3',
})
'''Theme overrides for rich console output'''

consout = console.Console(theme=theme)
'''Rich text console API for stdout'''

conserr = console.Console(theme=theme, stderr=True)
'''Rich text console API for stderr'''

settings = OutputSettings()


# mappings for strings to values of logging.* constants ######################

def lvlstr2int(level_string):
    '''Transform log level string to corresponding numerical value.'''
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'fatal': logging.FATAL,
        'critical': logging.FATAL,
    }
    try:
        ret = levels[level_string.lower()]
    except KeyError:
        ret = logging.WARNING
    return ret


def get_logfunc_for(level_string):
    '''Get logging function corresponding to string'''
    levels = {
        'debug': logging.debug,
        'info': logging.info,
        'warn': logging.warning,
        'warning': logging.warning,
        'error': logging.error,
        'fatal': logging.fatal,
        'critical': logging.fatal,
    }
    try:
        ret = levels[level_string.lower()]
    except KeyError:
        ret = logging.warning
    return ret


def configlvl():
    '''Get numerical value for configured log level string'''
    ret = lvlstr2int('warning')
    try:
        ret = lvlstr2int(tagfile.cfg['logging']['level'])
    except KeyError:
        raise ConfigError('No "logging.level" section found in config')
    return ret


# generic functions for printing to console without logging  #################

def sout(*args, hl=True):
    '''Print without newline to stdout stream if not settings.quiet.'''
    if not settings.quiet:
        consout.print(*args, end='', soft_wrap=True, highlight=hl)


def lnout(*args, hl=True):
    r'''Print with newline to stdout stream if not settings.quiet.'''
    if not settings.quiet:
        consout.print(*args, soft_wrap=True, highlight=hl)


def echo(*args):
    '''Print without highlighting but while respecting settings.quiet.'''
    lnout(*args, hl=False)


def serr(*args, hl=True, ignore_quiet=False):
    '''Print without newline to stderr and optionally override quiet.'''
    if ignore_quiet:
        origval = settings.quiet
        settings.quiet = False
        conserr.print(*args, end='', soft_wrap=True, highlight=hl)
        settings.quiet = origval
    else:
        if not settings.quiet:
            conserr.print(*args, end='', soft_wrap=True, highlight=hl)


def lnerr(*args, hl=True, ignore_quiet=False):
    r'''Print with newline to stderr and optionally override quiet.'''
    if ignore_quiet:
        origval = settings.quiet
        settings.quiet = False
        conserr.print(*args, soft_wrap=True, highlight=hl)
        settings.quiet = origval
    else:
        if not settings.quiet:
            conserr.print(*args, soft_wrap=True, highlight=hl)


# generic functions for verbose echo and logging #############################

def vecho(level_string, text):
    '''Print to std{out,err} based on level_string and `settings.verbose` var.

    Always print fatal errors, but print other levels (info, warning,
    error) only when not settings.quiet and settings.verbose is trueish.
    Messages with the *debug* level print nothing here. They are
    exclusively logged.
    '''
    lvl = lvlstr2int(level_string)
    if lvl >= logging.FATAL:
        lnerr('fatal error: {}'.format(text), ignore_quiet=True)
        return
    if settings.quiet or not settings.verbose:
        return

    if lvl == logging.INFO:
        lnout(text)
    elif lvl == logging.WARNING:
        lnerr('warning: {}'.format(text))
    elif lvl == logging.ERROR:
        lnerr('error: {}'.format(text))


def log(level_string, text):
    '''Generic function for logging using correct level'''
    if tagfile.cfg['logging']['enabled']:
        func = get_logfunc_for(level_string)
        func(text)


def logvecho(level_string, text):
    '''Generic function for combination of verbose output and logging'''
    log(level_string, text)
    vecho(level_string, text)


# level specific shortcuts for logging and verbose echo ######################

def info(text):
    '''Log info level message and print if settings.verbose is True'''
    logvecho('info', text)


def warning(text):
    '''Log warning level message and print if settings.verbose is True'''
    logvecho('warning', text)


def error(text):
    '''Log error level message and print if settings.verbose is True'''
    logvecho('error', text)


def fatal(text):
    '''Log fatal level message and print regardless of settings.verbose'''
    logvecho('fatal', text)
