# file: src/tagfile/commands/clones.py

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

import tagfile.core
import tagfile.output


class ClonesCommand(pycommand.CommandBase):
    '''Show files with matching checksums.'''
    usagestr = (
        'usage: tagfile clones [-s | --show-size] [-t | --show-type] '
        '[-m | --show-mime]\n'
        '   or: tagfile clones [-h | --help]'
    )
    description = __doc__
    description = (
        'Show files with matching checksums. In this overview the column\n'
        'with hashes is always printed. Add `-stm` flags to display more\n'
        'columns.\n\n'
        'By default, an extra line is printed after each list of clones,\n'
        'showing the total number of duplicates. This can be hidden with\n'
        '`--hide-sum`.'
    )
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('show-size', ('s', False, 'display column with filesizes')),
        ('show-type', ('t', False, 'display column with MIME type')),
        ('show-mime', ('m', False, 'display column with MIME type/subtype')),
        ('hide-sum', ('', False, 'do not print "X clones/duplicates" line')),
    )

    def run(self):
        if self.flags.help:
            tagfile.output.lnout(self.usage, hl=False)
            return 0
        tagfile.core.clones(flags=self.flags)
        return 0
