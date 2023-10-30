# tagfile

## Introduction

Search, index and tag your files and find duplicates.

The goal of tagfile is to manage and organize any sort of file
(documents, music, pictures and videos in particular) in a way that is
not tied to any file browser program, filesystem or operating system.
The metadata that tagfile creates and uses to keep track of these
files should be portable for use in multiple computer systems and be
independent from any persistent mount points, filepaths or filenames.

Tagfile is primarily a unixy command-line application with a focus on
simplicity, interactivity and scriptabilty through (shell) scripts. It
is shaping up to be an amalgamation of features from applications such
as locate, ls, find, file, cksum, sort and grep performed in constrained
scopes of specific sets of files that are defined and controlled by the
user in one or more sqlite databases.

It also is a package for Python (but the API is unstable at this point).

## Index

<!-- vim-markdown-toc GFM -->

* [Homes](#homes)
* [Features](#features)
* [Quick Manual](#quick-manual)
    * [Adding paths, indexing files and housekeeping](#adding-paths-indexing-files-and-housekeeping)
    * [Finding duplicate files with clones command](#finding-duplicate-files-with-clones-command)
    * [Usage examples: listing, searching and filtering files](#usage-examples-listing-searching-and-filtering-files)
    * [Help and synopses for commands](#help-and-synopses-for-commands)
* [Installing tagfile](#installing-tagfile)
* [Relation between media-paths, databases and config files](#relation-between-media-paths-databases-and-config-files)
* [Status](#status)
* [Software license](#software-license)

<!-- vim-markdown-toc -->

## Homes

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

## Quick Manual

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
tagfile find --type video --size-gt 104857600 --show-size --show-type \
   --sort=size --reverse
```

### Help and synopses for commands

<details><summary>tagfile</summary>

``` console
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

</details>

<details><summary>tagfile add</summary>

``` console
usage: tagfile add [-q | --quiet] <media-path>
   or: tagfile add [-h | --help]

Add a directory to media paths

Options:
-h, --help   show this help information
-q, --quiet  print nothing except fatal errors
```

</details>

<details><summary>tagfile clones</summary>

``` console
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

</details>

<details><summary>tagfile find</summary>

``` console
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

</details>

<details><summary>tagfile help</summary>

``` console
usage: tagfile help [<command>]

Show usage information (for subcommands)

Options:
-h, --help  show usage information for help command
```

</details>

<details><summary>tagfile info</summary>

``` console
usage: tagfile info [-C | --show-config]
   or: tagfile info [-h | --help]

Show media paths, user config and statistics for index.

Options:
-h, --help         show this help information
-C, --show-config  pretty print active config in python
```

</details>

<details><summary>tagfile list</summary>

``` console
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

</details>

<details><summary>tagfile updatedb</summary>

``` console
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

</details>

<details><summary>tagfile version</summary>

``` console
usage: tagfile version [-h | --help]

Show version and platform information

Options:
-h, --help  show this help information
```

</details>

## Installing tagfile

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

## Status

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

## Software license

Copyright (c) 2015-2023 Benjamin Althues \<benjamin at babab . nl\>

tagfile is open source software, licensed under a BSD-3-Clause license.
See the [LICENSE](https://github.com/babab/tagfile/blob/devel/LICENSE)
file for the full license text.
