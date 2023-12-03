# Tagfile

## Introduction

Search, index and tag your files and find duplicates.

The goal of tagfile is to manage and organize any sort of file
(documents, music, pictures and videos in particular) in a way that is
not tied to any file browser program, filesystem or operating system.
The metadata that tagfile creates and uses to keep track of these
files should be portable for use in multiple computer systems and be
independent from any persistent mount points, filepaths or filenames.


![logo](https://babab.codeberg.page/tagfile/assets/logo128.png){ align=right }
Tagfile is primarily a unixy command-line application with a focus on
simplicity, interactivity and scriptabilty through (shell) scripts. It
is shaping up to be an amalgamation of features from applications such
as locate, ls, find, file, cksum, sort and grep performed in constrained
scopes of specific sets of files that are defined and controlled by the
user in one or more sqlite databases.

It also is a package for Python (but the API is unstable at this point).

## Homes

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

Starting in March 2023 I've decided to properly release it to PyPI and
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
