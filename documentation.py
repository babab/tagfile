# flake8: noqa
# file: documentation.py

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

"""
Helper script to write documentation snippets to README and docs/* files.

This way we only have to alter one source while maintaining separate
sets of documentation for README and docs for html site generation that
differ in hierarchy and ordering of topics.
"""

snippets = [

# Introduction 1/2
    {'text': '''# Tagfile

## Introduction

Search, index and tag your files and find duplicates.

The goal of tagfile is to manage and organize any sort of file
(documents, music, pictures and videos in particular) in a way that is
not tied to any file browser program, filesystem or operating system.
The metadata that tagfile creates and uses to keep track of these
files should be portable for use in multiple computer systems and be
independent from any persistent mount points, filepaths or filenames.
''', 'destinations': ['README.md', 'docs/index.md']},

# Display logo using extended markdown syntax - docs only
    {'text': '''
![logo](https://babab.codeberg.page/tagfile/assets/logo128.png){ align=right }''',
     'destinations': ['docs/index.md']},

# Introduction 2/2
    {'text': '''Tagfile is primarily a unixy command-line application with a focus on
simplicity, interactivity and scriptabilty through (shell) scripts. It
is shaping up to be an amalgamation of features from applications such
as locate, ls, find, file, cksum, sort and grep performed in constrained
scopes of specific sets of files that are defined and controlled by the
user in one or more sqlite databases.

It also is a package for Python (but the API is unstable at this point).
''', 'destinations': ['README.md', 'docs/index.md']},


# TOC for README - created with Vim plugin
    {'text': '''## Index

<!-- vim-markdown-toc GFM -->
<!-- vim-markdown-toc -->
''', 'destinations': ['README.md']},


# Homes and Features
    {'text': '''## Homes

-   Docs: <https://babab.codeberg.page/tagfile>
-   Codeberg: <https://codeberg.org/babab/tagfile>
-   Github: <https://github.com/babab/tagfile>

## Features

-   scan all files in a directory (media-path) recursively
-   ignore files when scanning according to rules in user config
-   maintain a list of media-paths to prune/scan on a regular basis
-   index files with their checksums, size and MIME-type into a sqlite
    database
-   show a list of files in index, sortable by checksum, size and
    mimetype
-   find duplicate files, based on checksums
-   find files by matching on checksum, mimetype, size, name or
    substring of name and/or path
-   prune index from files that got moved or deleted
-   print results of *list* and *find* commands terminated with a null
    character to use for piping to other utilities like xargs.
-   configure aliases for certain commands and options (like git alias)

Features to be implemented in later versions:

-   remove duplicate files in the same directory
-   remove duplicate files interactively across directories
-   add user defined tags to files (using checksums, independent from
    filenames)

Ideas that may or may not be implemented in later versions:

-   ability to filter files using tags to create listings to use with
    other programs
-   ability to use tags to create directory structures of symlinked
    content
''', 'destinations': ['README.md', 'docs/index.md']},


# Manual part 1
    {'text': '''## Quick Manual

### Adding paths, indexing files and housekeeping

Open a terminal, and add one or more media-paths be scanned for files:

``` console
cd ~/Music
tagfile add .
tagfile add ~/Videos
```

This will only save a reference to the directory. To actually walk
through the directories and hash the files to get checksums, you can use
the `updatedb` command. This will recursively scan all media-paths
you\'ve added and may take some time, especially the first time.

For both the prune and scan actions, progressbars will be shown with
estimates of the remaining time to complete. Add a `--verbose` flag to
also output every filename and actions performed. Use Ctrl+C to cancel.
All progress already done will be saved.

``` console
tagfile updatedb
```

To see statistics of indexed files and a list of media-paths:

``` console
tagfile info
```

### Finding duplicate files with clones command

Show duplicate files using the clones command with/without option flags
(see `tagfile help clones` to see all available options):

``` console
tagfile clones
```

Show hash, path, size and full MIME-type (using long opts):

``` console
tagfile clones --show-size -show-mime
```

Show hash, path, size and first part of MIME-type (using short opts):

``` console
tagfile clones -st
```

### Usage examples: listing, searching and filtering files

The list and find commands are the most important part of tagfile and
probably the reason why you might want to use it. What follows are some
usage examples with both short and long optional arguments.

List all files sorted by filesize (showing checksum, filesize and
mimetype columns):

``` console
tagfile list -aS size
tagfile list --show-all --sort=size
```

List all files with MIME-type text/plain sorted by filesize from small
to big (showing checksum, filesize and mimetype columns):

``` console
tagfile find --mime text/plain -a -S size
tagfile find --mime=text/plain -show-all --sort=size
```

List all files, sorted by filetype (showing checksum, size and type):

``` console
tagfile list -HstS type
tagfile list --show-hash --show-size --show-type --sort=type
```

List all videos larger than 100MB, sorted by filesize from big to small
(showing type and filesize):

``` console
tagfile find --type video --size-gt 104857600 -stS size --reverse
tagfile find --type video --size-gt 104857600 --show-size --show-type --sort=size --reverse
```
''', 'destinations': ['README.md', 'docs/manual.md']},


# Command tagfile main header for README
    {'text': '''## Help and synopses for commands

<details><summary>tagfile</summary>
''', 'destinations': ['README.md']},

# Command tagfile main header for DOCS
    {'text': '''## Main command usage

Help and synopsis for main command that is printed when using:
`tagfile help`, `tagfile --help` or `tagfile -h`.
''', 'destinations': ['docs/commands.md']},

# Command tagfile main body
    {'text': '''``` console
Usage: tagfile [--config <filename>] [--db <name>] <command>
   or: tagfile [-h | --help] | [-V | --version]

Search, index and tag your files and find duplicates

Options:
--config=<filename>  use specified config file
--db=<name>          use database <name>, defined in config file
-h, --help           show this help information
-V, --version        show version and platform information

Commands:
  add        add a directory to media paths
  clones     show all indexed duplicate files
  find       find files according to certain criterias
  help       show help information
  info       show statistics for index and media paths
  list       show all indexed files
  updatedb   scan media paths and index newly added files
  version    show version and platform information

See 'tagfile help <command>' for more information on a
specific command, before using it.
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command add / subcommands header for README
    {'text': '''</details>

<details><summary>tagfile add</summary>
''', 'destinations': ['README.md']},

# Command add / subcommands header for DOCS
    {'text': '''## Command usage of subcommands

Help and synopses for subcommands that are printed when using `tagfile
help <command>`, `tagfile <command> --help` or `tagfile <command> -h`.

### add
''', 'destinations': ['docs/commands.md']},

# Command add
    {'text': '''``` console
usage: tagfile add [-q | --quiet] <media-path>
   or: tagfile add [-h | --help]

Add a directory to media paths

Options:
-h, --help   show this help information
-q, --quiet  print nothing except fatal errors
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command clones
    {'text': '''</details>

<details><summary>tagfile clones</summary>
''', 'destinations': ['README.md']},
    {'text': '''### clones
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile clones [-s | --show-size] [-t | --show-type] [-m | --show-mime]
   or: tagfile clones [-h | --help]

Show files with matching checksums. In this overview the column
with hashes is always printed. Add `-stm` flags to display more
columns.

By default, an extra line is printed after each list of clones,
showing the total number of duplicates. This can be hidden with
`--hide-sum`.

Options:
-h, --help       show this help information
-s, --show-size  display column with filesizes
-t, --show-type  display column with MIME type
-m, --show-mime  display column with MIME type/subtype
--hide-sum       do not print "X clones/duplicates" line
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command find
    {'text': '''</details>

<details><summary>tagfile find</summary>
''', 'destinations': ['README.md']},
    {'text': '''### find
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile find [--type=TYPE] [--mime=MIMETYPE] [--size-gt=BYTES]
                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]
                    [--name=NAME | --in-name=STRING] [-H | --show-hash]
                    [-s | --show-size] [-t | --show-type] [-m | --show-mime]
                    [-a | --show-all] [-S COL | --sort=COL] [--reverse]

   or: tagfile find [--type=TYPE] [--mime=MIMETYPE] [--size-gt=BYTES]
                    [--size-lt=BYTES] [--hash=HEX] [--in-path=STRING]
                    [--name=NAME | --in-name=STRING] [-0 | --print0]
                    [-S COL | --sort=COL] [--reverse]

   or: tagfile find [-h | --help]

Find files according to certain criterias

Options:
-h, --help          show this help information
--type=TYPE         match files on 1st part of MIME type
--mime=MIMETYPE     match files on full MIME type/subtype
--size-gt=BYTES     match files where size is greater than BYTES
--size-lt=BYTES     match files where size is lesser than BYTES
--hash=HEX          match files where checksum is (or starts with) HEX
--in-path=STRING    match absolute paths with a substring of STRING
--name=NAME         match filenames that are exactly NAME
--in-name=STRING    match filenames with a substring of STRING
-H, --show-hash     display column with checksum hash
-s, --show-size     display column with filesizes
-t, --show-type     display column with MIME type
-m, --show-mime     display column with MIME type/subtype
-a, --show-all      display hash, size, mime (same as -Hsm)
-S COL, --sort=COL  sort on: name, hash, size, type or mime
--reverse           reverse sort order
-0, --print0        end lines with null instead of newline
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command help
    {'text': '''</details>

<details><summary>tagfile help</summary>
''', 'destinations': ['README.md']},
    {'text': '''### help
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile help [<command>]

Show usage information (for subcommands)

Options:
-h, --help  show usage information for help command
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command info
    {'text': '''</details>

<details><summary>tagfile info</summary>
''', 'destinations': ['README.md']},
    {'text': '''### info
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile info [-C | --show-config]
   or: tagfile info [-h | --help]

Show media paths, user config and statistics for index.

Options:
-h, --help         show this help information
-C, --show-config  pretty print active config in python
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command list
    {'text': '''</details>

<details><summary>tagfile list</summary>
''', 'destinations': ['README.md']},
    {'text': '''### list
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile list [-H | --show-hash] [-s | --show-size] [-t | --show-type]
                    [-m | --show-mime] [-a | --show-all] [-S COL | --sort=COL]
                    [--reverse]

   or: tagfile list [-0 | --print0] [-S COL | --sort=COL] [--reverse]

   or: tagfile list [-h | --help]

Output a list of all indexed files.
By default, the list is sorted on file path.

Options:
-h, --help          show this help information
-H, --show-hash     display column with checksum hash
-s, --show-size     display column with filesizes
-t, --show-type     display column with MIME type
-m, --show-mime     display column with MIME type/subtype
-a, --show-all      display hash, size, mime (same as -Hsm)
-S COL, --sort=COL  sort on: name, hash, size, type or mime
--reverse           reverse sort order
-0, --print0        end lines with null instead of newline
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command updatedb
    {'text': '''</details>

<details><summary>tagfile updatedb</summary>
''', 'destinations': ['README.md']},
    {'text': '''### updatedb
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile updatedb [-v, --verbose] [-q, --quiet] [--prune] [--scan]
                        [-n ID, --path-id=ID]

   or: tagfile updatedb [-h | --help]

Scan media paths. Index added files and prune removed files.

Use the option `--prune` if you only want to remove entries
from the index if files are missing. Use the option `--scan`
to only scan for newly added files without pruning.

To prune and/or scan for a single media-path only, use
`--path-id=ID`. See tagfile info for an overview of paths/ID's.

Options:
-h, --help           show this help information
-v, --verbose        display a message for every action
-q, --quiet          display nothing except fatal errors
--prune              prune removed files only; don't scan
--scan               scan for new files only; don't prune
-n ID, --path-id=ID  prune/scan only files in path with this id

When no options are specified, updatedb will both scan and prune.
It will always prune deleted files before scanning for new files.
```
''', 'destinations': ['README.md', 'docs/commands.md']},

# Command version
    {'text': '''</details>

<details><summary>tagfile version</summary>
''', 'destinations': ['README.md']},
    {'text': '''### version
''', 'destinations': ['docs/commands.md']},
    {'text': '''``` console
usage: tagfile version [-h | --help]

Show version and platform information

Options:
-h, --help  show this help information
```
''', 'destinations': ['README.md', 'docs/commands.md']},
    {'text': '''</details>
''', 'destinations': ['README.md']},

# Installing
    {'text': '''## Installing tagfile

**All commands should be run as a regular user (not root).**

Tagfile is a command-line end-user application written in Python that is
dependant on packages from PyPI. You can install it using pip. But using
pipx (<https://pypa.github.io/pipx/>) is recommended because it avoids
dependency problems and/or clashes with python packages from your
system\'s package manager in the future.

Install latest **release** from PyPI:

``` console
pipx install tagfile
```

Install latest **development version** from git:

``` console
pipx install git+https://github.com/babab/tagfile@devel
```

To build and install **from source** you can use:

``` console
make install
```

To **upgrade** or **uninstall** tagfile in the future you can use:

``` console
pipx upgrade tagfile
pipx uninstall tagfile
```
''', 'destinations': ['README.md', 'docs/installing.md']},


# Manual part 2 - Relation explanation
    {'text': '''
## Relation between media-paths, databases and config files

By default, tagfile uses one config file and one database.

A config file:

-   Contains a single set of ignore rules for all databases.
-   Defines one or more databases. New databases must be defined in the
    config `[databases]` section with a `name = "location-path"`
    key-value pair.
-   Can be specified with the tagfile `--config=FILENAME` option

A database:

-   Can contain zero, one or multiple media-paths.
-   The most used commands/actions (add, find, list and updatedb) are
    performed in a database-wide scope.
-   The default database to use can be:

    > -   configured in the config file `default_database = "name"`
    >     setting.
    > -   specified with the tagfile `--config=FILENAME` option

A media-path is a parent directory that contains one or more files you
want to index. By scanning with `updatedb`, tagfile will walk
recursively through all subdirectories and add any file that does not
match the ignore rules from the config. Any files that are indexed but
removed in the filesystem itself afterwards, will be pruned from the
index on the next run of `updatedb`.
''', 'destinations': ['README.md', 'docs/manual.md']},


# Last section in README | On index page in docs
    {'text': '''## Status

**Until a stable version 1.0.0 is ready, the API, CLI and config
settings are subject to change from 0.x version to 0.x version, likely
without offering migrations.** Tagfile adheres to [Semantic
Versioning](https://semver.org).

-   Current stable release: **v0.1.0**
-   Current dev/git version: *v0.2.0a13*

Tagfile has been written in a short time and used by me sporadically for
8 years after that. All code was contained in a single file script in
`~/bin`, available from Github only.

Starting in March 2023 I\'ve decided to properly release it to PyPI and
flesh out the current project structure, command interface and database
handling before working on new features so it may live up to its name.
Since at this moment in time, you cannot tag your files yet :)

Prerequisites:

-   Python 3.8 or later

Dependencies (automatically installed with pipx / pip):

-   Peewee ORM (<https://peewee.readthedocs.org/en/latest/>)
-   pycommand (<https://babab.github.io/pycommand/>)
-   python-magic (<https://pypi.python.org/pypi/python-magic/>)
-   rich (<https://pypi.python.org/pypi/rich/>)
''', 'destinations': ['README.md', 'docs/index.md']},


# License section in README
    {'text': '''## Software license

Copyright (c) 2015-2023 Benjamin Althues \<benjamin at babab . nl\>

Tagfile is open source software, licensed under a BSD-3-Clause license.
See the [LICENSE](https://github.com/babab/tagfile/blob/devel/LICENSE)
file for the full license text.
''', 'destinations': ['README.md']},


# License section in docs
    {'text': '''Tagfile is open source software, licensed under a BSD-3-Clause license.

------------------------------------------------------------------------------

Copyright (c) 2015-2023 Benjamin Althues <benjamin@babab.nl>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from this
software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
''', 'destinations': ['docs/license.md']},


# CHANGELOG file / docs section
    {'text': '''# Change Log

Tagfile adheres to [Semantic Versioning](http://semver.org/).

## v0.2.0 - to be released (now in devel branch)

### Notes for "updating" from v0.1.0

Compared to version 0.1.0, the configfile and database fields are
changed completely. There are no migrations available for config or
data. They have to be re-created.

A new configfile `config.toml` with the default program settings will be
created next to the old `config.yaml` the first time tagfile runs. Edit
the new config manually.

The name of the (default) database has been changed from `index.db` to
`main.db`, but is configuable now. Re-populate the database by starting
from scratch.

### Added

-   Indexing of filesize and MIME-type for each file
-   Lots of search parameters and sorting options for *find* command
-   Support for specifying other config files
-   Support for multiple databases (defined in a single config)
-   Command *help* as alias/alternative for
    `tagfile <command> -h --help`
-   Command *version* as alias/alternative for `tagfile -V --version`
-   Command *list* for creating a list without searching
-   Validation of config file
-   More colored highlighting for output, spinner animations and
    improved progressbar using rich
-   Flexible settings for toggling colored output: auto, always and
    never
-   Unit and integration tests with coverage reporting
-   Support for configuring aliases for certain commands and options
    (like git [alias] in .gitconfig)
-   Support for running library module as a script with
    `python -m tagfile [opts] <command>`
-   Support for ENV variables: `TAGFILE_CONF_HOME` and
    `TAGFILE_DATA_HOME` using parent dirs of ENV vars
    `XDG_{DATA,CONFIG}_HOME` when defined or the expected defaults
    otherwise.
-   Option -q, \--quiet to commands add and updatedb
-   Option -v, \--verbose to command updatedb
-   Dependency `python-magic`
-   *Development:* task-runner config `Taskfile.dist.yml` for
    go-task/task as alternative for `Makefile`. Make remains the primary
    task-runner however and the Taskfile contents may lag behind.

### Changed

-   Commands *prune* and *scan* are removed and its features are
    included and expanded upon in a new *updatedb* command. By default,
    updatedb will prune first and scan afterwards. The old behaviour can
    be approximated through updatedb\'s option flags `--prune` and
    `--scan`.
-   Command *same* is replaced with *clones*
-   Command *stats* is replaced with *info*
-   User config file format from Yaml to TOML with a brand new settings
    mapping as well.
-   More sophisicated ignore rules: instead of only ignoring by partial
    match of path with a list, also ignore on complete and partial
    matches of filenames using separate lists.
-   Show first 7 chars instead of first 5 chars of checksum
-   Replaced dependency `ansicolors` with `rich`
-   Don\'t scan symlinks (by default, but configurable)
-   Logging level can be configured.

### Removed

-   Command *re-index*

### Bugs

-   Fixed race condition for temp. files when scanning

## v0.1.0 - 2023-03-23

-   Initial release
''', 'destinations': ['CHANGELOG.md', 'docs/changes.md']},

#     {'text': '''
# ''', 'destinations': ['README.md', 'docs/index.md']},
]


def main(eol='\n'):
    mapping = []
    files = []
    n_writes = {}

    def append_to_file(filename, string):
        with open(filename, 'a') as fh:
            if n_writes[filename] > 0:
                # add a newline before every section but not at top
                fh.write(eol)
            fh.write(string)
        n_writes[filename] += 1

    # collect snippets and files
    for snip in snippets:
        for dest in snip['destinations']:
            files.append(dest)
            mapping.append([dest, snip['text']])

    # remove all text in files first and add write counter for file
    uniqfiles = set(files)
    for fn in uniqfiles:
        with open(fn, 'w') as fh:
            fh.write('')
        n_writes[fn] = 0

    # append documentation
    for item in mapping:
        append_to_file(item[0], item[1])

    # output summary
    print('number of snippets defined: {}\n'.format(len(snippets)))
    padding = len(max(uniqfiles, key=len))
    for fn in sorted(uniqfiles):
        print('{0:{pad}s}  {1:2d} snippet{2}'.format(
            fn, n_writes[fn], 's' if n_writes[fn] > 1 else '', pad=padding
        ))


if __name__ == '__main__':
    try:
         main()
    except FileNotFoundError as e:
        print(e)
        print('error: make sure directories exist and are writable')
