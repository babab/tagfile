tagfile
==============================================================================

Search, index and tag your files and find duplicates.

Prerequisites:

- Python 3.7 or later

Dependencies (installed with pip):

- ansicolors (https://pypi.python.org/pypi/ansicolors/)
- Peewee ORM (https://peewee.readthedocs.org/en/latest/)
- pycommand (https://babab.github.io/pycommand/)
- PyYAML (http://pyyaml.org/)


**tagfile is in an early development stage and has not been released yet**


Quick Manual
------------

Open a terminal and cd to a directory to be scanned for files::

   $ cd ~/Music
   $ tagfile scan


Now, you can see stats, search for files by string and find duplicate
files using the following commands::

   $ tagfile stats
   $ tagfile find radiohead
   $ tagfile same


You can add directories without cd'ing to it first with the add command::

   $ tagfile add ~/Videos


Installing tagfile
------------------

Make sure that pip points to the python3 interpreter and run::

   $ sudo pip install -r requirements.txt
   $ sudo cp tagfile /usr/local/bin


Software license
----------------

Copyright (c) 2015-2023 Benjamin Althues <benjamin@babab.nl>

tagfile is open source software, licensed under a BSD-3-Clause license.
See the `LICENSE <LICENSE>`_ file for the full license text.
