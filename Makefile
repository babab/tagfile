# Copyright (c) 2023 Benjamin Althues <benjamin@babab.nl>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# SPDX-License-Identifier: BSD-3-Clause

NAME    = tagfile
VERSION = 0.2.0a0
PYTHON  = python3
PIP     = ${PYTHON} -m pip
WHEEL   = dist/${NAME}-${VERSION}-py3-none-any.whl

help:
	# This makefile is meant to aid in development flow as
	# well as document it. Regular users should follow the
	# instructions on installing this program in the README.
	#
	# HELP
	#  help         - show this help information
	#  release	- show manual release steps
	#
	# DEVELOPMENT TARGETS
	#  build        - flit build
	#  install      - flit build and install with pipx install
	#  install-dev  - install with pipx install --editable .
	#  uninstall    - same as pipx uninstall NAME
	#  clean        - remove build and dist folders
	#
	# BUILD DEPENDENCIES that are precursors to the targets above
	#  get-flit - install flit if it isn't in PATH
	#  get-pipx - install pipx if it isn't in PATH

release:
	# MANUAL RELEASE STEPS
	#  - Create / edit ~/.pypirc
	#
	#  $ make clean
	#  $ flit publish --repository testpypi
	#
	#  - check sdist and project page on test.pypi.org
	#  - if not already done, bump version in package/module and Makefile.
	#  - edit changelog,
	#  - make final signed commit for release.
	#
	#  $ flit publish
	#  $ git tag -S vX.X.X
	#  $ git push --tags
	#
	#  - set __version__ to X.X.Xa0


dist: get-flit
	@echo
	### BUILD ###
	flit build

build: dist

install: get-pipx uninstall dist
	@echo
	### INSTALL ###
	pipx install "${WHEEL}"

install-dev: get-pipx uninstall dist
	@echo
	### INSTALL ###
	pipx install --editable .

uninstall:
	@echo
	### UNINSTALL ###
	-pipx uninstall "${NAME}"
clean:
	rm -rf dist

get-flit:
	@echo
	### GET-FLIT ###
	command -v flit >/dev/null || ${PIP} install --user flit
get-pipx:
	@echo
	### GET-PIPX ###
	command -v pipx >/dev/null || ${PIP} install --user pipx

# These are to help debug this Makefile:
pipuserlist = "$$(${PIP} list --user --format=freeze)"
X-WARNING-purge-all-user-packages-from-pip:
	${PIP} uninstall -y "${pipuserlist}"
