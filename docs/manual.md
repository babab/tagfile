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
you've added and may take some time, especially the first time.

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
