## Installing tagfile

**All commands should be run as a regular user (not root).**

Tagfile is a command-line end-user application written in Python that is
dependant on packages from PyPI. You can install it using pip. But using
pipx (<https://pypa.github.io/pipx/>) is recommended because it avoids
dependency problems and/or clashes with python packages from your
system's package manager in the future.

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
