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
import sys

import tagfile

VERBOSE = False
'''Used to set state of verbose output when using -v command flags'''


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
        ret = levels[level_string]
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
        ret = levels[level_string]
    except KeyError:
        ret = logging.warning
    return ret


def configlvl():
    '''Get numerical value for configured log level string'''
    ret = lvlstr2int('warning')
    try:
        ret = lvlstr2int(tagfile.config['logging']['level'])
    except KeyError:
        raise tagfile.ConfigError('No "logging.level" section found in config')
    return ret


# generic functions for verbose echo and logging #############################

def vecho(level_string, text):
    '''Print to std{out,err} or not based on level_string and `VERBOSE` var'''
    lvl = lvlstr2int(level_string)
    if lvl >= logging.FATAL:
        # always print fatal errors
        sys.stderr.write('fatal error: {}\n'.format(text))
        return
    if not VERBOSE:
        # print other levels only when VERBOSE is trueish
        return

    if lvl <= logging.INFO:
        print(text)
    elif lvl == logging.WARNING:
        sys.stderr.write('warning: {}\n'.format(text))
    elif lvl == logging.ERROR:
        sys.stderr.write('error: {}\n'.format(text))


def log(level_string, text):
    '''Generic function for logging using correct level'''
    if tagfile.config['logging']['enabled']:
        func = get_logfunc_for(level_string)
        func(text)


def logvecho(level_string, text):
    '''Generic function for combination of verbose output and logging'''
    log(level_string, text)
    vecho(level_string, text)


# level specific shortcuts for logging and verbose echo ######################

def info(text):
    '''Log info level message and print if VERBOSE is True'''
    logvecho('info', text)


def warning(text):
    '''Log warning level message and print if VERBOSE is True'''
    logvecho('warning', text)


def error(text):
    '''Log error level message and print if VERBOSE is True'''
    logvecho('error', text)


def fatal(text):
    '''Log fatal level message and print regardless of VERBOSE value'''
    logvecho('fatal', text)
