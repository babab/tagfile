# file: tests/tagfile/test_core.py

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

import os

import pytest

import tagfile
import tagfile.common
import tagfile.core
import tagfile.files


# testing workings before init() step
##############################################################################

def test_core_tfman_paths_is_not_None():
    tfman = tagfile.core.tfman
    assert tfman.paths is not None


def test_core_tfman_error_when_not_initialized_loadKnownRepos():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.loadKnownRepos()


def test_core_tfman_error_when_not_initialized_addPath():
    _path = os.environ['TAGFILEDEV_MEDIA_PATH']
    paths = tagfile.files.walkdir(_path)
    sample_3_mp4 = paths[0]
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.addPath(sample_3_mp4)


def test_core_tfman_error_when_not_initialized_find():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.find('sampl')


def test_core_tfman_error_when_not_initialized_info():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.info()


def test_core_tfman_error_when_not_initialized_re_index():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.re_index()


def test_core_tfman_error_when_not_initialized_prune():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.prune()


def test_core_tfman_error_when_not_initialized_clones():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.clones()


def test_core_tfman_error_when_not_initialized_scan():
    with pytest.raises(tagfile.common.ProgrammingError):
        tagfile.core.tfman.scan()


# testing init() step
##############################################################################

def test_core_tfman_before_and_after_init():
    tfman = tagfile.core.tfman
    assert tfman._initialized is False
    tfman.init()
    assert tfman._initialized is True
