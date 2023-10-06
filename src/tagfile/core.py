# file: src/tagfile/core.py

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
import os

import magic
from rich.progress import track

from tagfile import (
    cfg,     # dict - from `tagfile.config.Configuration().cfg`
    DB,      # var - Database handler for Peewee
    files,   # module
    output,  # module
)
from tagfile.output import (
    consout as c,  # instance - from `rich.console.Console()`
    lnout,         # function
)
from tagfile.common import ProgrammingError
from tagfile.models import Index, Repository

# NAMESPACE SHORTCUTS
# output = tagfile.output
# c      = tagfile.output.consout
# lnout  = tagfile.output.lnout


class _TagFileManager:
    '''Private _TagFileManager class. Instance available as
       `tagfile.core.tfman`'''

    paths = []
    '''paths is empty on init. Use setter functions. Reading directly is fine.

    Use `loadKnownRepos()` to populate with latest known media paths.
    Use `addPath(path)` to add new media path (recursively adding files).
    '''

    _initialized = False

    def init(self):
        '''Connect the `tagfile.DB` database handler and setup tables.

        This is to make sure the database is only initialized once, and
        can receive arguments in the future. It can be called multiple
        times without a problem and since it returns self, you can
        directly chain any of the other methods.
        '''
        if self._initialized:
            return self
        logging.basicConfig(
            filename=os.path.expanduser(cfg['logging']['file']),
            level=output.configlvl(), style='{',
            format='{asctime}:{levelname}: {message}'
        )
        DB.connect()
        if not Index.table_exists():
            DB.create_tables([Index, Repository])
        self._initialized = True

        output.log('debug', 'tfman initialized')
        output.log('debug', 'color_system = {}'.format(c.color_system))
        return self

    def loadKnownRepos(self):
        '''Load known media paths into `self.paths`'''
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        text = 'Browsing media paths for files... '
        with c.status(text, spinner='dqpb'):
            qrep = Repository.select()
            for item in qrep:
                self.addPath(item.filepath)

    def addPath(self, path):
        '''Walk path and add all found files'''
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        self.paths.extend(files.walkdir(path))
        Repository.get_or_create(filepath=path)

    def find(self, substring):
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        res = Index.select().where(Index.basename.contains(substring))
        for i in res:
            print(i.filepath)

    def info(self):
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        lnout('[bold]INDEX STATS[/bold]')
        lnout(f'files indexed\t{Index.select().count()}')
        lnout(f'duplicate files\t{self.clones(return_count=True)}')

        qrep = Repository.select()
        repos = f'[green]{qrep.count()}[/green]'
        lnout(f'\n[bold]MEDIA PATHS ({repos}):[/bold]')

        for item in qrep:
            lnout(f'- {item.filepath}')

        lnout('\n[bold]USER CONFIG[/]')
        lnout(cfg)

    def prune(self):
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        lnout('\n[bold]PRUNING[/bold]')
        text = 'Checking index for entries with missing files... '
        with c.status(text, spinner='dqpb'):
            res = Index.raw('''SELECT * FROM `index`''')
            npruned = 0

        for i in track(res, console=output.consout,
                       disable=False if cfg['load-bar'] else True,
                       description=''):
            if not os.path.exists(i.filepath):
                Index.delete().where(Index.id == i.id).execute()
                output.info('prune: Removed {}'.format(i.filepath))
                npruned += 1
        lnout(f'DONE. {npruned} files were removed from the index.', hl=False)

    def clones(self, return_count=False, sizes=False, categories=False,
               mimetypes=False):
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        res = Index.raw('''SELECT *, COUNT(filehash) FROM `index`
                        GROUP BY filehash HAVING ( COUNT(filehash) > 1 )''')
        hashes = []
        for i in res:
            hashes.append(i.filehash)
        if return_count:
            return len(hashes)

        res = (Index.select()
                    .where(Index.filehash << hashes)
                    .order_by(Index.filehash))
        count = 0
        changed = ''
        toggler = False
        for i in res:
            if changed != i.filehash:
                toggler = False if toggler else True
                lnout(f'└──── [italic]{count:>3} clones/duplicates[/italic]')
                count = 0

            _hash = i.filehash[:5]
            _size = ' {}'.format(files.sizefmt(i.filesize)) if sizes else ''
            _cat = ' {}'.format(i.cat) if categories else ''
            _mime = ' {}'.format(i.mime) if mimetypes else ''
            if toggler:
                lnout('[green]{}{}[/green]{}{} {}'.format(
                    _hash, _size, _cat, _mime, i.filepath
                ))
            else:
                lnout('[magenta]{}{}[/magenta]{}{} {}'.format(
                    _hash, _size, _cat, _mime, i.filepath
                ))
            changed = i.filehash
            count += 1
        lnout(f'└──── [italic]{count:>3} clones/duplicates[/italic]')

    def scan(self):
        '''Check if filepaths are in database, otherwise hash file and save'''
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        iall = 0
        inew = 0
        iignore = 0
        iexisting = 0
        ierrunicode = 0
        ierrpermission = 0
        total = len(self.paths)
        try:
            lnout('\n[bold]SCANNING[/bold]')

            for path in track(self.paths, console=output.consout,
                              disable=False if cfg['load-bar'] else True,
                              description=''):
                file_is_valid = True
                iall += 1

                # see if filename matches any configured ignore patterns
                for ignorepatt in cfg['ignore']:
                    if ignorepatt in path:
                        file_is_valid = False
                        iignore += 1
                        output.info('scan: path ignored: ' + path)
                        break

                # get filesize, this might raise a few exceptions
                try:
                    filesize = os.path.getsize(path)
                    if cfg['ignore-empty'] and not filesize:
                        file_is_valid = False
                except FileNotFoundError:
                    file_is_valid = False
                except PermissionError:
                    file_is_valid = False
                    ierrpermission += 1
                    output.error('PermissionError(getsize) for: ' + path)

                if file_is_valid:
                    try:
                        Index.get(Index.filepath == path)
                        iexisting += 1
                    except Index.DoesNotExist:
                        try:
                            _mimetype = magic.from_file(path, mime=True)
                            _cat = _mimetype[:_mimetype.index('/')]
                            Index.create(
                                filehash=files.hashfile(path), filepath=path,
                                basename=os.path.basename(path),
                                filesize=filesize, cat=_cat, mime=_mimetype
                            )
                        except PermissionError:
                            ierrpermission += 1
                            output.error(
                                'PermissionError(hashfile) for: ' + path
                            )
                            break
                        inew += 1
                        output.info('scan: added ' + path)
                    except UnicodeEncodeError:
                        ierrunicode += 1
        finally:
            lnout('DONE.\n\n[bold]STATISTICS[/bold]')
            lnout('Already indexed {:>12}'.format(iexisting))
            lnout('Ignored files   {:>12}'.format(iignore))
            lnout('[green]Newly added[/]     {:>12}'.format(inew))
            lnout('-' * 28)
            lnout('Total files     {:>12}'.format(total))

            if ierrunicode or ierrpermission:
                lnout('\n[bold]ERRORS[/]')
            if ierrunicode:
                lnout('[red]Filenames with unicode errors:[/] {}'
                      .format(ierrunicode))
            if ierrpermission:
                lnout('[red]File locations with permission errors:[/] {}'
                      .format(ierrpermission))


tfman = _TagFileManager()
'''A single public instance of the private `_TagFileManager` object to
use. The class `_TagFileManager` should not be used directly.'''
