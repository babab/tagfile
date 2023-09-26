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
import sys

import colors
import magic

from tagfile import (
    DB,
    ProgrammingError,
    config,
    files,
    output,
)
from tagfile.models import Index, Repository


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
            filename=os.path.expanduser(config['logging']['file']),
            level=output.configlvl(), style='{',
            format='{asctime}:{levelname}: {message}'
        )
        DB.connect()
        if not Index.table_exists():
            DB.create_tables([Index, Repository])
        self._initialized = True
        return self

    def loadKnownRepos(self, silent=False):
        '''Load known media paths into `self.paths`'''
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        if not silent:
            print('Browsing media paths for files, please wait...')
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
        qrep = Repository.select()
        files = colors.green(str(Index.select().count()))
        repos = colors.green(str(qrep.count()))
        duplos = colors.green(str(self.clones(return_count=True)))
        print('{}\tfiles indexed\n{}\tduplicate files'.format(files, duplos))
        print('\nMEDIA PATHS ({}):'.format(repos))

        for item in qrep:
            print(item.filepath)

    def re_index(self):
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        Index.delete().execute()
        for i in Repository.select():
            self.addPath(i.filepath)
        self.scan()

    def prune(self):
        if not self._initialized:
            raise ProgrammingError("_TagFileManager was not initialized")
        print(colors.bold('\nPRUNING STARTS'))
        print('Checking index for entries with missing files...')
        res = Index.raw('''SELECT * FROM `index`''')
        npruned = 0
        for i in res:
            if not os.path.exists(i.filepath):
                Index.delete().where(Index.id == i.id).execute()
                print('Removed {}'.format(i.filepath))
                npruned += 1
        print('DONE. {} files were removed from the index'.format(npruned))

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
        changed = ''
        toggler = False
        for i in res:
            if changed != i.filehash:
                toggler = False if toggler else True

            _hash = i.filehash[:5]
            _size = ' {}'.format(files.sizefmt(i.filesize)) if sizes else ''
            _cat = ' {}'.format(i.cat) if categories else ''
            _mime = ' {}'.format(i.mime) if mimetypes else ''
            if toggler:
                print('{}{}{}{} {}'.format(
                    colors.green(_hash), _size, _cat, _mime, i.filepath
                ))
            else:
                print('{}{}{}{} {}'.format(
                    colors.magenta(_hash),
                    colors.bold(_size),
                    colors.bold(_cat),
                    colors.bold(_mime),
                    colors.bold(i.filepath)
                ))
            changed = i.filehash

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
            print(colors.bold('\nSCANNING STARTS'))
            for path in self.paths:
                file_is_valid = True
                iall += 1
                if config['load-bar'] and not output.VERBOSE:
                    sys.stdout.write('\r  {} / {}'.format(iall, total))

                # see if filename matches any configured ignore patterns
                for ignorepatt in config['ignore']:
                    if ignorepatt in path:
                        file_is_valid = False
                        iignore += 1
                        output.info('scan: Ignored path ' + path)
                        break

                # get filesize, this might raise a few exceptions
                try:
                    filesize = os.path.getsize(path)
                    if config['ignore-empty'] and not filesize:
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
                        output.info('scan: Added ' + path)
                    except UnicodeEncodeError:
                        ierrunicode += 1
        finally:
            if output.VERBOSE:
                print('')
            print('\rTotal files     {:>12}'.format(total))
            print('Already indexed {:>12}'.format(iexisting))
            print('Ignored files   {:>12}'.format(iignore))
            print(colors.green('Newly added     {:>12}'.format(inew)))

            if ierrunicode or ierrpermission:
                print(colors.bold('\nERRORS'))
            if ierrunicode:
                print(colors.red('Filenames with unicode errors: {}'
                                 .format(ierrunicode)))
            if ierrpermission:
                print(colors.red('File locations with permission errors: {}'
                                 .format(ierrpermission)))


tfman = _TagFileManager()
'''A single public instance of the private `_TagFileManager` object to
use. The class `_TagFileManager` should not be used directly.'''
