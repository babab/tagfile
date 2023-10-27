Change Log
==========

tagfile adheres to `Semantic Versioning <http://semver.org/>`_.


0.2.0 - to be released
----------------------

Notes for "updating" from v0.1.0
################################

Compared to version 0.1.0, the configfile and database fields are
changed completely. There are no migrations available for config or
data. They have to be re-created.

A new configfile ``config.toml`` with the default program settings will
be created next to the old ``config.yaml`` the first time tagfile runs.
Edit the new config manually.

The name of the (default) database has been changed from ``index.db``
to ``main.db``, but is configuable now. Re-populate the database by
starting from scratch.

Added
#####
- Indexing of filesize and MIME-type for each file
- Lots of search parameters and sorting options for *find* command
- Support for specifying other config files
- Support for multiple databases (defined in a single config)
- Command *help* as alias/alternative for ``tagfile <command> -h --help``
- Command *version* as alias/alternative for ``tagfile -V --version``
- Command *list* for creating a list without searching
- Validation of config file
- More colored highlighting for output, spinner animations and improved
  progressbar using rich
- Flexible settings for toggling colored output: auto, always and never
- Unit and integration tests with coverage reporting
- Support for running library module as a script with
  ``python -m tagfile [opts] <command>``
- Support for ENV variables: *TAGFILE_CONF_HOME* and *TAGFILE_DATA_HOME*
  using parent dirs of ENV vars XDG_{DATA,CONFIG}_HOME when defined or the
  expected defaults otherwise.
- Option -q, --quiet to commands add and updatedb
- Option -v, --verbose to command updatedb
- Dependency ``python-magic``
- *Development:* task-runner config ``Taskfile.dist.yml`` for
  go-task/task as alternative for ``Makefile``. Make remains the primary
  task-runner however and the Taskfile contents may lag behind.

Changed
#######

- Commands *prune* and *scan* are removed and its features are
  included and expanded upon in a new *updatedb* command. By default,
  updatedb will prune first and scan afterwards. The old behaviour can be
  approximated through updatedb's option flags ``--prune`` and ``--scan``.
- Command *same* is replaced with *clones*
- Command *stats* is replaced with *info*
- User config file format from Yaml to TOML with a brand new settings
  mapping as well.
- More sophisicated ignore rules: instead of only ignoring by partial
  match of path with a list, also ignore on complete and partial matches
  of filenames using separate lists.
- Show first 7 chars instead of first 5 chars of checksum
- Replaced dependency ``ansicolors`` with ``rich``
- Don't scan symlinks (by default, but configurable)
- Logging level can be configured.

Removed
#######

- Command *re-index*

Bugs
####

- Fixed race condition for temp. files when scanning


0.1.0 - 2023-03-23
------------------

- Initial release
