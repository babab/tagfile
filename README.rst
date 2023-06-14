tagfile
==============================================================================

Search, index and tag your files and find duplicates.

The goal of tagfile is to manage and organize documents, downloads,
music, pictures and videos in a way that is not tied to any file browser
program, filesystem or operating system.

The metadata that tagfile creates and uses to keep track of these
files should be portable for use in multiple computer systems and be
independent from any persistent mount points, filepaths or filenames.


--------
Features
--------

- index files with their checksums
- find duplicate files/checksums
- scan all files in a directory recursively
- ignore files according to rules in user config
- prune index from files that got moved or deleted

Features to be implemented in later versions:

- remove duplicate files in the same directory
- remove duplicate files interactively across directories
- add user defined tags to files (using checksums, independent from filenames)

Ideas that may or may not be implemented in later versions:

- ability to filter files using tags to create listings to use with
  other programs
- ability to use tags to create directory structures of symlinked content


------------
Quick Manual
------------

Open a terminal and cd to a directory to be scanned for files:

.. code:: console

   $ cd ~/Music
   $ tagfile scan


Now, you can see stats, search for files by string and find duplicate
files using the following commands:

.. code:: console

   $ tagfile stats
   $ tagfile find radiohead
   $ tagfile same


You can add directories without cd'ing to it first with the add command:

.. code:: console

   $ tagfile add ~/Videos


------------------
Installing tagfile
------------------

Tagfile is a command-line end-user application written in Python that
is dependant on packages from PyPI. You can install it using pip. But
using pipx (https://pypa.github.io/pipx/) is recommended because it
avoids dependency problems and/or clashes with python packages from your
system's package manager in the future.

Install latest release from PyPI:

.. code:: console

   $ pipx install tagfile

Install latest development version from git:

.. code:: console

   $ pipx install git+https://github.com/babab/tagfile@devel

To build and install from source you can use:

.. code:: console

   $ make install

This will auto-install flit (build tool) and pipx if not found.

To upgrade or uninstall tagfile in the future you can use:

.. code:: console

   $ pipx upgrade tagfile
   $ pipx uninstall tagfile


------
Status
------

Current version: **v0.1.0**

Tagfile has been written in a short time and used by me sporadically for
8 years after that. All code was contained in a single file script in
``~/bin``, available from Github only.

Starting in March 2023 I've decided to properly release it to PyPI and
flesh out the current project structure, command interface and database
handling before working on new features so it may live up to its name.
Since at this moment in time, you cannot tag your files yet :)

Tagfile adheres to `Semantic Versioning <https://semver.org>`_. Until
a stable version 1.0.0 is ready, the API, CLI and config settings are
subject to change from 0.x version to 0.x version, likely without
offering migrations.

Prerequisites:

- Python 3.7 or later

Dependencies (automatically installed with pipx / pip):

- Peewee ORM (https://peewee.readthedocs.org/en/latest/)
- PyYAML (https://pyyaml.org/)
- ansicolors (https://pypi.python.org/pypi/ansicolors/)
- pycommand (https://babab.github.io/pycommand/)


----------------
Software license
----------------

Copyright (c) 2015-2023 Benjamin Althues <benjamin at babab . nl>

tagfile is open source software, licensed under a BSD-3-Clause license.
See the `LICENSE <https://github.com/babab/tagfile/blob/devel/LICENSE>`_
file for the full license text.
