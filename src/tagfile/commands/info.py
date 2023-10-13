# file: src/tagfile/commands/info.py

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

from rich.pretty import Pretty
import pycommand

from tagfile import (
    configuration,  # instance of `tagfile.config.Configuration`
    core,    # module
    output,  # module
)
from tagfile.models import Index, Repository


class InfoCommand(pycommand.CommandBase):
    '''Show media paths, user config and statistics for index.'''
    usagestr = (
        'usage: tagfile info [-C | --show-config]\n'
        '   or: tagfile info [-h | --help]'
    )
    description = __doc__
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('show-config', ('C', False, 'pretty print active config in python')),
    )

    def run(self):
        if self.flags.help:
            print(self.usage)
            return 0

        if self.flags['show-config']:
            output.lnout('[bold]USER CONFIG[/]')
            output.lnout(f'file: {configuration.fullpath}\n')
            output.lnout(Pretty(configuration.cfg, indent_size=2))
            return 0

        output.lnout('[bold]INDEX STATS[/bold]')
        output.lnout(f'files indexed\t{Index.select().count()}')
        output.lnout(f'duplicate files\t{len(core.clones_list())}')

        qrep = Repository.select()
        repos = f'[green]{qrep.count()}[/green]'
        output.lnout(f'\n[bold]MEDIA PATHS ({repos}):[/bold]')
        for item in qrep:
            output.lnout(f'- {item.filepath}')
