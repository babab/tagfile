#!/usr/bin/env python

'''Search, index and tag your files and find duplicates'''

# Copyright (c) 2015-2023  Benjamin Althues <benjamin@babab.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import hashlib
import logging
import os
import sys

import colors
import peewee as pw
import pycommand
import yaml

__docformat__ = 'restructuredtext'
__author__ = "Benjamin Althues"
__copyright__ = "Copyright (C) 2015-2023  Benjamin Althues"
__version_info__ = (0, 1, 0, 'alpha', 0)
__version__ = '0.1.0'

defaultconfig = '''
log-file:   ~/.tagfile/tagfile.log
load-bar:   yes
ignore:
    - .git
    - .hg
    - .svn
    - .pyc
    - .virtualenv
    - __pycache__
    - node_modules
ignore-empty:   yes
hash-algo:      sha1
hash-buf-size:  1024
'''

config = yaml.safe_load(defaultconfig)

# Set base path and initially create config and data files
BASE_PATH = os.path.expanduser('~/.tagfile')

# initialize data path
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)
    fn = os.path.join(BASE_PATH, 'config.yaml')
    with open(fn, 'w') as f:
        f.write(defaultconfig[1:])
    print(colors.green('Created config file in {}\n'.format(fn)))

# Read from default user config file
fn = os.path.join(BASE_PATH, 'config.yaml')
if os.path.exists(fn):
    config.update(yaml.safe_load(open(fn).read()))

# Init sqlite database - used in peewee models
DB = pw.SqliteDatabase(os.path.join(BASE_PATH, 'index.db'))


class Model(pw.Model):
    '''Database model for peewee ORM'''
    class Meta:
        database = DB


class Index(Model):
    filehash = pw.CharField()
    filepath = pw.CharField()
    basename = pw.CharField()


class Repository(Model):
    filepath = pw.CharField()


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


class TagFile:
    '''Search, index and tag your files and find duplicates'''
    def __init__(self):
        DB.connect()
        if not Index.table_exists():
            DB.create_tables([Index, Repository])
        self.paths = []

    def addPath(self, path):
        '''Walk path and add all found files'''
        self.paths.extend(Files.walkdir(path))
        Repository.get_or_create(filepath=path)
        return self

    def find(self, substring):
        res = Index.select().where(Index.basename.contains(substring))
        for i in res:
            print(i.filepath)

    def stats(self):
        files = colors.green(str(Index.select().count()))
        repos = colors.green(str(Repository.select().count()))
        duplos = colors.green(str(self.same(return_count=True)))
        print('{}\tfiles indexed\n{}\trepositories (main paths)\n'
              '{}\tduplicate files'.format(files, repos, duplos))

    def re_index(self):
        Index.delete().execute()
        for i in Repository.select():
            self.addPath(i.filepath)
        self.scan()

    def same(self, return_count=False):
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
        total = len(self.paths)
        try:
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

                if config['ignore-empty'] and not os.path.getsize(path):
                    file_is_valid = False

                if file_is_valid:
                    try:
                        Index.get(Index.filepath == path)
                    except Index.DoesNotExist:
                        inew += 1
                        Index.create(
                            filehash=Files.hashfile(path), filepath=path,
                            basename=os.path.basename(path)
                        )
                        logging.debug('Added ' + path)
        finally:
            if inew:
                print(colors.green('\rAdded {} new files'.format(inew)))
            if iignore:
                print(colors.cyan('\rIgnored {} files'.format(iignore)))
            if not inew and not iignore:
                print('\r                         ')
        return self


class Command(pycommand.CommandBase):
    '''Argument handler based on pycommand'''
    usagestr = 'Usage: tagfile <options>'
    description = TagFile.__doc__
    optionList = (
        ('help', ('h', False, 'show this help information')),
        ('version', ('', False, 'show version information')),
        ('config', ('', '<filename>', 'use specified config file')),
    )
    usageTextExtra = (
        'Commands:\n'
        '  scan               scan current directory and add to index\n'
        '  add <directory>    scan <directory> and add to index\n'
        '  find <string>      find all filenames for <string>\n'
        '  same               show all indexed duplicate files\n'
        '  stats              show statistics for index, repos and tags\n'
        '  re-index           re-index all repos'
    )

    def run(self):
        '''Run from shell; main application program flow.'''

        # Flags that will print and exit
        if self.flags['help']:
            print(self.usage)
            return
        elif self.flags['version']:
            print('Python version ' + sys.version.split()[0])
            return

        # Update config with file
        if self.flags['config']:
            fn = self.flags['config']
            if os.path.exists(fn):
                config.update(yaml.safe_load(open(fn).read()))
            else:
                print('ERROR: file does not exist')
                return 2

        # Setup logging
        logging.basicConfig(
            filename=os.path.expanduser(config['log-file']),
            level=logging.INFO, style='{',
            format='{asctime}:{levelname}: {message}'
        )

        # Setup TagFile
        tf = TagFile()

        try:
            command = self.args[0]
        except IndexError:
            command = None
        try:
            arg = self.args[1]
        except IndexError:
            arg = None

        if command == 'scan':
            tf.addPath(os.getcwd())
            tf.scan()
        elif command == 'add':
            if arg:
                tf.addPath(os.path.expanduser(arg))
                tf.scan()
            else:
                print('error: command add requires argument')
        elif command == 'find':
            if arg:
                tf.find(arg)
            else:
                print('error: command find requires argument')
        elif command == 'same':
            tf.same()
        elif command == 'stats':
            tf.stats()
        elif command == 're-index':
            tf.re_index()
        else:
            print(self.usage)

if __name__ == '__main__':
    try:
        cmd = Command(sys.argv[1:])
        if cmd.error:
            print('error: {0}'.format(cmd.error))
            sys.exit(1)
        else:
            sys.exit(cmd.run())
    except KeyboardInterrupt:
        print('\nOk, well... see you later then I guess.')
