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
import tagfile.core


# testing workings before init() step
##############################################################################

def test_core_Files_staticmethod_walkdir():
    _path = os.environ['TAGFILEDEV_MEDIA_PATH']
    paths = tagfile.core.Files.walkdir(_path)
    assert paths == [
        '{}/video/sample-3.mp4'.format(_path),
        '{}/video/sample-3b.mp4'.format(_path),
    ]


def test_core_Files_hashfile_raises_error_on_unknown_algo():
    tagfile.config['hash-algo'] = 'not-a-valid-algo'
    _path = os.environ['TAGFILEDEV_MEDIA_PATH']
    paths = tagfile.core.Files.walkdir(_path)
    sample_3_mp4 = paths[0]
    with pytest.raises(tagfile.ConfigError):
        tagfile.core.Files.hashfile(sample_3_mp4)


def test_core_Files_staticmethod_sizefmt():
    lib = tagfile.core.Files
    assert lib.sizefmt(0) == '    0B'
    assert lib.sizefmt(1) == '    1B'
    assert lib.sizefmt(34) == '   34B'
    assert lib.sizefmt(267) == '  267B'
    assert lib.sizefmt(1234) == '  1.2K'
    assert lib.sizefmt(12345) == ' 12.1K'
    assert lib.sizefmt(123456) == '120.6K'
    assert lib.sizefmt(1234567) == '  1.2M'
    assert lib.sizefmt(12345678) == ' 11.8M'
    assert lib.sizefmt(123456789) == '117.7M'
    assert lib.sizefmt(1234567890) == '  1.1G'
    assert lib.sizefmt(12345678901) == ' 11.5G'
    assert lib.sizefmt(123456789012) == '115.0G'
    assert lib.sizefmt(1234567890123) == '  1.1T'
    assert lib.sizefmt(12345678901234) == ' 11.2T'
    assert lib.sizefmt(123456789012345) == '112.3T'
    assert lib.sizefmt(1234567890123456) == '  1.1P'
    assert lib.sizefmt(12345678901234567) == ' 11.0P'
    assert lib.sizefmt(123456789012345678) == '109.7P'
    assert lib.sizefmt(1234567890123456789) == '  1.1E'
    assert lib.sizefmt(12345678901234567890) == ' 10.7E'
    assert lib.sizefmt(123456789012345678901) == '107.1E'
    assert lib.sizefmt(1234567890123456789012) == '  1.0Z'
    assert lib.sizefmt(12345678901234567890123) == ' 10.5Z'
    assert lib.sizefmt(123456789012345678901234) == '104.6Z'
    assert lib.sizefmt(1234567890123456789012345) == '  1.0Y'
    assert lib.sizefmt(12345678901234567890123456) == ' 10.2Y'
    assert lib.sizefmt(123456789012345678901234567) == '102.1Y'
    assert lib.sizefmt(1234567890123456789012345678) == '1021.2Y'
    assert lib.sizefmt(12345678901234567890123456789) == '10212.1Y'
    assert lib.sizefmt(123456789012345678901234567890) == '102121.1Y'


def test_core_tfman_paths_is_not_None():
    tfman = tagfile.core.tfman
    assert tfman.paths is not None


def test_core_tfman_error_when_not_initialized_loadKnownRepos():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.loadKnownRepos()


def test_core_tfman_error_when_not_initialized_addPath():
    _path = os.environ['TAGFILEDEV_MEDIA_PATH']
    paths = tagfile.core.Files.walkdir(_path)
    sample_3_mp4 = paths[0]
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.addPath(sample_3_mp4)


def test_core_tfman_error_when_not_initialized_find():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.find('sampl')


def test_core_tfman_error_when_not_initialized_info():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.info()


def test_core_tfman_error_when_not_initialized_re_index():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.re_index()


def test_core_tfman_error_when_not_initialized_prune():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.prune()


def test_core_tfman_error_when_not_initialized_clones():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.clones()


def test_core_tfman_error_when_not_initialized_scan():
    with pytest.raises(tagfile.ProgrammingError):
        tagfile.core.tfman.scan()


# testing init() step
##############################################################################

def test_core_tfman_before_and_after_init():
    tfman = tagfile.core.tfman
    assert tfman._initialized is False
    tfman.init()
    assert tfman._initialized is True
