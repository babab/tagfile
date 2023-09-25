# Copyright (c) 2015-2023 Benjamin Althues <benjamin@babab.nl>
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
VERSION   = 0.2.0a9
SCRIPT    = ./src/${NAME}/commands/main_cmd.py
CODE_DIRS = src tests
BIN_NAME  = ${NAME}
BADGESDIR = docs/badges

# absolute path to system python (version)
SYSPYTHON = /usr/bin/python3

# directory name, will be created next to Makefile
VENVDIR   = .virtualenv

### Settings for testing, using ENV vars #####################################
# Without these envvars, pytest will try to use your real data/config
# and fail. The directories (including the cache dir) will be
# automatically created by tagfile.
export TAGFILE_CONFIG_HOME = ${PWD}/cache/config_home
export TAGFILE_DATA_HOME = ${PWD}/cache/data_home
export TAGFILEDEV_MEDIA_PATH = ${PWD}/cache/media

### Variables - changing these is not advised ################################
sys_pip   = ${SYSPYTHON} -m pip
venv_pip  = ${VENVDIR}/bin/python -m pip
dist_whl  = dist/${NAME}-${VERSION}-py3-none-any.whl


# Include any local configuration overrides
sinclude config.mk

help:
	@echo 'This makefile is meant to aid in development flow as well as'
	@echo 'document it. Regular users should follow the instructions on'
	@printf 'installing %s in the README.\n' "${NAME}"
	@echo
	@echo 'To work on this project while keeping package dependencies isolated'
	@echo 'from system packages, you can either use:'
	@echo
	@echo "- 'make pipx-develop' to have command(s) directly available in PATH"
	@echo "- 'make develop' to keep the command(s) out your PATH (by default,"
	@echo '  but available after sourcing bin/activate).'
	@echo
	@echo 'The test target will install a link to the project code so that'
	@echo 'the source and tests can be inspected for code coverage.'
	@echo
	@echo 'The test-pkg target will always build and install using the'
	@echo 'wheel dist, even when this project is already installed with an'
	@echo '--editable flag. This is to minimize any issues that may arise'
	@echo 'in the packaging process by including it in testing. This target'
	@echo 'does not check for coverage.'
	@echo
	@echo 'HELP'
	@echo ' help         - show this help information'
	@echo ' release      - show manual release steps'
	@echo
	@printf 'BUILD AND TEST TARGETS (using venv at %s)\n' "${VENVDIR}"
	@echo ' test         - make develop and run tests through Coverage.py'
	@echo " develop      - install into venv with 'pip install --editable .'"
	@echo ' install      - do a venv-install and link exe in .local/bin'
	@echo ' exe          - build a single executable file with pyinstaller'
	@echo ' test-pkg     - install pkg and run checks/tests without coverage'
	@echo ' badges       - make test and create svg badges using shields.io'
	@echo
	@printf 'PIPX TARGETS (using ~/.local/pipx/venvs/%s)\n' "${NAME}"
	@echo ' pipx-install - flit build and install with pipx install'
	@echo " pipx-devel   - install with 'pipx install --editable .'"
	@printf ' pipx-remove  - same as pipx uninstall %s\n' "${NAME}"
	@echo
	@echo 'MISC TARGETS that are used as precursors in the targets above'
	@echo ' build | dist - flit build'
	@echo ' clean        - remove venv, build and dist directories'
	@echo ' get-pipx     - install pipx into user site-packages if not in PATH'
	@echo ' venv         - only make virtualenv and install build deps'
	@echo ' venv-install - install into venv with all dependencies/extras'

release:
	@echo 'MANUAL RELEASE STEPS'
	@echo ' - Create / edit ~/.pypirc'
	@echo
	@echo ' $$ make clean'
	@echo ' $$ flit publish --repository testpypi'
	@echo
	@echo ' - check sdist and project page on test.pypi.org'
	@echo ' - if not already done, bump version in package/module and Makefile.'
	@echo ' - edit changelog,'
	@echo ' - make final signed commit for release.'
	@echo
	@echo ' $$ flit publish'
	@echo ' $$ git tag -S vX.X.X'
	@echo ' $$ git push --tags'
	@echo
	@echo ' - set __version__ to X.X.Xa0'


### targets using venv #######################################################

build: dist

venv: ${VENVDIR}

${VENVDIR}:
	@printf '\n--- SETTING UP VIRTUAL ENVIRONMENT AND FLIT ---\n'
	@printf 'Using python version: '
	@${SYSPYTHON} --version
	${SYSPYTHON} -m venv ${VENVDIR}
	${venv_pip} install -U pip
	${venv_pip} install flit
	@printf '\n--- INSTALL ALL DEPENDENCIES BUT NOT %s ITSELF ---\n' "${NAME}"
	${VENVDIR}/bin/flit install --only-deps

exe: clean ${VENVDIR}
	@printf '\n--- FREEZE AND COMPILE WITH PYINSTALLER ---\n'
	${VENVDIR}/bin/pyinstaller -F -n ${NAME} --clean ${SCRIPT}

dist: ${VENVDIR}
	@printf '\n--- BUILD WITH FLIT ---\n'
	${VENVDIR}/bin/flit build

install: venv-install
	@printf '\n--- CREATING SYMBOLIC LINK IN PATH ---\n'
	ln -svf "$${PWD}/${VENVDIR}/bin/${BIN_NAME}" "$${HOME}/.local/bin/${BIN_NAME}"

venv-install: ${VENVDIR}
	@printf '\n--- INSTALL ALL DEPENDENCIES AND %s ITSELF ---\n' "${NAME}"
	${VENVDIR}/bin/flit install

develop: ${VENVDIR}
	@printf '\n--- INSTALL IN VENV WITH EDITABLE SOURCE ---\n'
	${venv_pip} install --editable .
	@printf '\n--- CREATING SYMBOLIC LINK IN PATH ---\n'
	ln -svf "$${PWD}/${VENVDIR}/bin/${BIN_NAME}" "$${HOME}/.local/bin/${BIN_NAME}"

test-data: #custom
	@printf '\n--- CREATING DIRECTORY FOR HOLDING MEDIA FILES FOR TESTING ---\n'
	mkdir -vp "$${TAGFILEDEV_MEDIA_PATH}/video"
	@printf '\n--- Downloading MEDIA FILES FOR TESTING ---\n'
	wget -P "$${TAGFILEDEV_MEDIA_PATH}/video" "https://getsamplefiles.com/download/mp4/sample-3.mp4"
	cp -v "$${TAGFILEDEV_MEDIA_PATH}/video/sample-3.mp4" "$${TAGFILEDEV_MEDIA_PATH}/video/sample-3b.mp4"

test: ${VENVDIR} develop clean-config-data #custom
	@printf '\n--- CREATING DIRECTORY FOR REPORTS ---\n'
	mkdir -vp reports/htmlcov
	@printf '\n--- CHECKING IF TESTDATA IS ALREADY AVAILABLE ---\n' #custom
	test -d "$${TAGFILEDEV_MEDIA_PATH}" || make test-data #custom
	@printf '\n--- CHECK CODE STYLE AND CYCLOMATIC COMPLEXITY ---\n'
	${VENVDIR}/bin/flake8 -v --max-complexity=20 ${CODE_DIRS}
	@printf '\n--- RUN PYTEST THROUGH COVERAGE ---\n'
	${VENVDIR}/bin/coverage run -m pytest
	@printf '\n--- COVERAGE REPORT ---\n'
	${VENVDIR}/bin/coverage report
	${VENVDIR}/bin/coverage xml -o reports/coverage.xml
	${VENVDIR}/bin/coverage html -d reports/htmlcov

test-pkg: ${VENVDIR} venv-install clean-config-data #custom
	@printf '\n--- CHECK CODE STYLE AND CYCLOMATIC COMPLEXITY ---\n'
	${VENVDIR}/bin/flake8 -v --max-complexity=20 ${CODE_DIRS}
	@printf '\n--- RUN PYTEST ---\n'
	${VENVDIR}/bin/pytest  # uses config section in pyproject.toml

badges: test
	@printf '\n--- CREATING DIRECTORY FOR BADGES ---\n'
	mkdir -vp ${BADGESDIR}
	@printf '\n--- CREATING BADGES ---\n'
	${VENVDIR}/bin/genbadge tests -i reports/junit.xml -o ${BADGESDIR}/tests.svg
	${VENVDIR}/bin/genbadge coverage -i reports/coverage.xml -o ${BADGESDIR}/coverage.svg

clean-config-data: #custom
	@printf '\n--- CLEANING UP TESTING CONFIG/DATA HOMES ---\n'
	test -n "$${TAGFILE_CONFIG_HOME}" && rm -vrf "$${TAGFILE_CONFIG_HOME}"
	test -n "$${TAGFILE_DATA_HOME}" && rm -vrf "$${TAGFILE_DATA_HOME}"

clean:
	@printf '\n--- CLEANING UP FILES AND VIRTUAL ENV ---\n'
	rm -rf build dist reports ${VENVDIR}
	rm -f ${NAME}.spec
	find -type d -name __pycache__ -print0 | xargs -0 rm -rf
	@printf '\nWarning: The cache/media dir must be manually removed if needed!\n' #custom


### pipx targets / user packages #############################################

pipx-install: get-pipx pipx-remove dist
	@printf '\n--- INSTALL IN A PIPX ENVIRONMENT ---\n'
	pipx install "${dist_whl}"

pipx-devel: get-pipx pipx-remove
	@printf '\n--- INSTALL IN A PIPX ENVIRONMENT WITH EDITABLE SOURCE ---\n'
	pipx install --editable .

pipx-remove:
	@printf '\n--- UNINSTALL FROM PIPX IF FOUND, ELSE CONTINUE ---\n'
	-pipx uninstall "${NAME}"
get-pipx:
	@printf '\n--- FIND PIPX OR ELSE INSTALL PIPX IN USER ENVIRONMENT ---\n'
	command -v pipx >/dev/null || ${sys_pip} install --user pipx

# These are to help debug this Makefile:
pipuserlist = "$$(${sys_pip} list --user --format=freeze)"
X-WARNING-purge-all-user-packages-from-pip:
	${sys_pip} uninstall -y "${pipuserlist}"
