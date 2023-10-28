# tagfile

<!-- vim-markdown-toc GFM -->

* [Introduction](#introduction)
* [Features](#features)
* [Quick Manual](#quick-manual)
    * [Adding paths, indexing files and housekeeping](#adding-paths-indexing-files-and-housekeeping)
    * [Finding duplicate files with clones command](#finding-duplicate-files-with-clones-command)
    * [Listing, searching and filtering files using the list and find commands](#listing-searching-and-filtering-files-using-the-list-and-find-commands)
* [Installing tagfile](#installing-tagfile)
* [Relation between media-paths, databases and config files](#relation-between-media-paths-databases-and-config-files)
* [Status](#status)
* [Software license](#software-license)

<!-- vim-markdown-toc -->

## Introduction

Search, index and tag your files and find duplicates.

The goal of tagfile is to manage and organize documents, downloads,
music, pictures and videos in a way that is not tied to any file browser
program, filesystem or operating system.

The metadata that tagfile creates and uses to keep track of these files
should be portable for use in multiple computer systems and be
independent from any persistent mount points, filepaths or filenames.

Tagfile is primarily a unixy command-line application with a focus on
simplicity, interactivity and scriptabilty through (shell) scripts. It
also is a package for Python (but the API is unstable at this point).

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

### Listing, searching and filtering files using the list and find commands

This is the most important part of tagfile and the reason why you might
want to use it. What follows are some usage examples with both short and
long optional arguments.

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
-   Current dev/git version: *v0.2.0a11*

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
