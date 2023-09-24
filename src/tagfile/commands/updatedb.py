# file: src/tagfile/commands/updatedb.py

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

import tagfile.output
from tagfile.core import tfman


class UpdateDbCommand(pycommand.CommandBase):
    '''Scan all media paths. Index added files and prune removed files.'''
    usagestr = (
        'usage: tagfile updatedb [--prune] [--scan] [-v | --verbose]\n'
        '   or: tagfile updatedb [-h | --help]'
    )
    description = (
        '{}\n\n'
        'Use the option `--prune` if you only want to remove entries\n'
        'from the index if files are missing. Use the option `--scan`\n'
        'to only scan for newly added files without pruning.'
    ).format(__doc__)
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('prune', ('', False, "prune removed files only; don't scan")),
        ('scan', ('', False, "scan for new files only; don't prune")),
        ('verbose', ('v', False, 'print message for all actions')),
    )
    usageTextExtra = (
        'When no options are specified, updatedb will both scan and prune.\n'
        'It will always prune deleted files before scanning for new files.\n'
    )

    def run(self):
        if self.flags.help:
            print(self.usage)
            return 0

        tagfile.output.VERBOSE = self.flags.verbose

        # All options that reach here are valid. We need the repos for
        # everything that follows.
        tfman.init()
        tfman.loadKnownRepos()

        # support flagging of both options; don't skip or exit early with elif
        if self.flags.prune or self.flags.scan:
            if self.flags.prune:
                tfman.prune()
            if self.flags.scan:
                tfman.scan()
            return 0

        # default, without options
        tfman.prune()
        tfman.scan()
        return 0
