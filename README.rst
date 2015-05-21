tagfile
==============================================================================

Search, index and tag your files and find duplicates.

Prerequisites:

- Python 3.2 or later (no Python 2 support, but it may very well work)

Dependencies (installed with pip):

- Peewee ORM (https://peewee.readthedocs.org/en/latest/)
- PyYAML (http://pyyaml.org/)
- ansicolors (https://pypi.python.org/pypi/ansicolors/1.0.2)
- pycommand (http://pythonhosted.org/pycommand/)


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

Copyright (c) 2015  Benjamin Althues <benjamin@babab.nl>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
