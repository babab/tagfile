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

import hashlib
import logging
import os
import sys

import colors

from tagfile import DB, config
from tagfile.models import Index, Repository


class Files:
    '''Filesystem functions'''
    @staticmethod
    def walkdir(directory):
        paths = []
        for root, directories, files in os.walk(os.path.expanduser(directory)):
            for filename in files:
                filepath = os.path.join(root, filename)
                paths.append(filepath)
        return paths

    @staticmethod
    def hashfile(filepath):
        if config['hash-algo'] == 'md5':
            h = hashlib.md5()
        elif config['hash-algo'] == 'sha1':
            h = hashlib.sha1()
        else:
            raise Exception('Invalid "hash-algo" in configuration')

        with open(filepath, 'rb') as f:
            while True:
                data = f.read(config['hash-buf-size'])
                if not data:
                    break
                h.update(data)
        return h.hexdigest()


class _TagFileManager:
    '''Private _TagFileManager class. Instance available as
       `tagfile.core.tfman`'''

    paths = []
    '''paths is empty on init. Use setter functions. Reading directly is fine.

    Use `loadKnownRepos()` to populate with latest known media paths.
    Use `addPath(path)` to add new media path (recursively adding files).
    '''

    def __init__(self):
        DB.connect()
        if not Index.table_exists():
            DB.create_tables([Index, Repository])

    def loadKnownRepos(self, silent=False):
        '''Load known media paths into `self.paths`'''
        if not silent:
            print('Browsing media paths for files, please wait...')
        qrep = Repository.select()
        for item in qrep:
            self.addPath(item.filepath)

    def addPath(self, path):
        '''Walk path and add all found files'''
        self.paths.extend(Files.walkdir(path))
        Repository.get_or_create(filepath=path)
        return self

    def find(self, substring):
        res = Index.select().where(Index.basename.contains(substring))
        for i in res:
            print(i.filepath)

    def info(self):
        qrep = Repository.select()
        files = colors.green(str(Index.select().count()))
        repos = colors.green(str(qrep.count()))
        duplos = colors.green(str(self.clones(return_count=True)))
        print('{}\tfiles indexed\n{}\tduplicate files'.format(files, duplos))
        print('\nMEDIA PATHS ({}):'.format(repos))

        for item in qrep:
            print(item.filepath)

    def re_index(self):
        Index.delete().execute()
        for i in Repository.select():
            self.addPath(i.filepath)
        self.scan()

    def prune(self):
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

    def clones(self, return_count=False):
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
            if toggler:
                print('{} {}'.format(colors.green(i.filehash[:5]), i.filepath))
            else:
                print('{} {}'.format(colors.magenta(i.filehash[:5]),
                                     colors.bold(i.filepath)))
            changed = i.filehash

    def scan(self):
        '''Check if filepaths are in database, otherwise hash file and save'''
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
                if config['load-bar']:
                    sys.stdout.write('\r  {} / {}'.format(iall, total))

                for ignorepatt in config['ignore']:
                    if ignorepatt in path:
                        file_is_valid = False
                        iignore += 1
                        logging.debug('Ignored ' + path)
                        break

                if config['ignore-empty']:
                    try:
                        if not os.path.getsize(path):
                            file_is_valid = False
                    except FileNotFoundError:
                        file_is_valid = False
                    except PermissionError:
                        file_is_valid = False
                        ierrpermission += 1
                        logging.error('PermissionError(getsize) for: ' + path)

                if file_is_valid:
                    try:
                        Index.get(Index.filepath == path)
                        iexisting += 1
                    except Index.DoesNotExist:
                        try:
                            Index.create(
                                filehash=Files.hashfile(path), filepath=path,
                                basename=os.path.basename(path)
                            )
                        except PermissionError:
                            ierrpermission += 1
                            logging.error(
                                'PermissionError(hashfile) for: ' + path
                            )
                            break
                        inew += 1
                        logging.debug('Added ' + path)
                    except UnicodeEncodeError:
                        ierrunicode += 1
        finally:
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
        return self


tfman = _TagFileManager()
'''A single public instance of the private `_TagFileManager` object to
use. The class `_TagFileManager` should not be used directly.'''
