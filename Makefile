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

### Settings #################################################################
NAME      = tagfile
VERSION   = 0.2.0a0
SCRIPT    = ./src/${NAME}/commands/${NAME}.py
CODE_DIRS = src tests

# absolute path to system python (version)
SYSPYTHON = /usr/bin/python3

# directory name, will be created next to Makefile
VENVDIR   = .virtualenv


### Variables - changing these is not advised ################################
sys_pip   = ${SYSPYTHON} -m pip
venv_pip  = ${VENVDIR}/bin/python -m pip
dist_whl  = dist/${NAME}-${VERSION}-py3-none-any.whl

# Include any local configuration overrides
sinclude config.mk

help:
	# This makefile is meant to aid in development flow as well as
	# document it. Regular users should follow the instructions on
	@printf '# installing %s in the README.\n' "${NAME}"
	#
	# To work on this project while keeping package dependencies isolated
	# from system packages, you can either use:
	#
	# - 'make pipx-develop' to have command(s) directly available in PATH
	# - 'make develop' to keep the command(s) out your PATH (by default,
	#   but available after sourcing bin/activate).
	#
	# The test target will always build and install using the wheel dist,
	# even when this project is already installed with an --editable flag.
	# This is to minimize any issues that may arrise in the packaging
	# process by including it in testing.
	#
	# HELP
	#  help         - show this help information
	#  release	- show manual release steps
	#
	@printf '# BUILD AND TEST TARGETS (using venv at %s)\n' "${VENVDIR}"
	#  test         - build and install; check style and run unit tests
	#  develop      - install into venv with 'pip install --editable .'
	#  exe          - build a single executable file with pyinstaller'
	#
	@printf '# PIPX TARGETS (using ~/.local/pipx/venvs/%s)\n' "${NAME}"
	#  pipx-install - flit build and install with pipx install
	#  pipx-devel   - install with 'pipx install --editable .'
	@printf '#  pipx-remove  - same as pipx uninstall %s\n' "${NAME}"
	#
	# MISC TARGETS that are primarily precursors to the targets above
	#  build | dist - flit build
	#  clean        - remove venv, build and dist directories
	#  get-pipx     - install pipx into user site-packages if not in PATH
	#  venv         - only make virtualenv and install build deps
	#  venv-install - install into venv with all dependencies/extras

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


### targets using venv #######################################################

build: dist

venv: ${VENVDIR}

${VENVDIR}:
	@printf "\n--- SETTING UP VIRTUAL ENVIRONMENT AND FLIT ---\n"
	@printf "Using python version: "
	@${SYSPYTHON} --version
	${SYSPYTHON} -m venv ${VENVDIR}
	${venv_pip} install -U pip
	${venv_pip} install flit

exe: clean ${VENVDIR}
	@printf "\n--- INSTALL ALL DEPENDENCIES BUT NOT %s ITSELF ---\n" "${NAME}"
	${VENVDIR}/bin/flit install --only-deps
	@printf "\n--- FREEZE AND COMPILE WITH PYINSTALLER ---\n"
	${VENVDIR}/bin/pyinstaller --onefile --clean ${SCRIPT}

dist: ${VENVDIR}
	@printf "\n--- BUILD WITH FLIT ---\n"
	${VENVDIR}/bin/flit build

venv-install: ${VENVDIR}
	@printf "\n--- INSTALL ALL DEPENDENCIES AND %s ITSELF ---\n" "${NAME}"
	${VENVDIR}/bin/flit install

develop: ${VENVDIR}
	@printf "\n--- INSTALL IN VENV WITH EDITABLE SOURCE ---\n"
	${venv_pip} install --editable .

test: ${VENVDIR} venv-install
	@printf "\n--- CHECK CODE STYLE AND CYCLOMATIC COMPLEXITY ---\n"
	${VENVDIR}/bin/flake8 -v --max-complexity=20 ${CODE_DIRS}
	@printf "\n--- TEST CODE ---\n"
	${VENVDIR}/bin/pytest  # uses config section in pyproject.toml

clean:
	@printf "\n--- CLEANING UP FILES AND VIRTUAL ENV ---\n"
	rm -rf build dist ${VENVDIR}
	rm -f ${NAME}.spec
	find -type d -name __pycache__ -print0 | xargs -0 rm -rf


### pipx targets / user packages #############################################

pipx-install: get-pipx pipx-remove dist
	@printf "\n--- INSTALL IN A PIPX ENVIRONMENT ---\n"
	pipx install "${dist_whl}"

pipx-devel: get-pipx pipx-remove dist
	@printf "\n--- INSTALL IN A PIPX ENVIRONMENT WITH EDITABLE SOURCE ---\n"
	pipx install --editable .

pipx-remove:
	@printf "\n--- UNINSTALL FROM PIPX IF FOUND, ELSE CONTINUE ---\n"
	-pipx uninstall "${NAME}"
get-pipx:
	@printf "\n--- FIND PIPX OR ELSE INSTALL PIPX IN USER ENVIRONMENT ---\n"
	command -v pipx >/dev/null || ${sys_pip} install --user pipx

# These are to help debug this Makefile:
pipuserlist = "$$(${sys_pip} list --user --format=freeze)"
X-WARNING-purge-all-user-packages-from-pip:
	${sys_pip} uninstall -y "${pipuserlist}"
