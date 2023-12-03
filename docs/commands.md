## Main command usage

Help and synopsis for main command that is printed when using:
`tagfile help`, `tagfile --help` or `tagfile -h`.

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

## Command usage of subcommands

Help and synopses for subcommands that are printed when using `tagfile
help <command>`, `tagfile <command> --help` or `tagfile <command> -h`.

### add

``` console
usage: tagfile add [-q | --quiet] <media-path>
   or: tagfile add [-h | --help]

Add a directory to media paths

Options:
-h, --help   show this help information
-q, --quiet  print nothing except fatal errors
```

### clones

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

### find

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

### help

``` console
usage: tagfile help [<command>]

Show usage information (for subcommands)

Options:
-h, --help  show usage information for help command
```

### info

``` console
usage: tagfile info [-C | --show-config]
   or: tagfile info [-h | --help]

Show media paths, user config and statistics for index.

Options:
-h, --help         show this help information
-C, --show-config  pretty print active config in python
```

### list

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

### updatedb

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

### version

``` console
usage: tagfile version [-h | --help]

Show version and platform information

Options:
-h, --help  show this help information
```
