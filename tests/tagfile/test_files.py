# file: tests/tagfile/test_files.py

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
from tagfile.common import ConfigError
import tagfile.files


def test_files_function_walkdir():
    '''Test walkdir with files that are created by Makefile/Taskfile'''
    _path = os.environ['TAGFILEDEV_MEDIA_PATH']
    paths = tagfile.files.walkdir(_path)
    assert paths == [
        '{}/video/sample-3.mp4'.format(_path),   # original
        '{}/video/sample-3b.mp4'.format(_path),  # copy
        '{}/video/sample3b.mp4'.format(_path),   # symlink to copy
        '{}/video/sample3.mp4'.format(_path),    # symlink to original
    ]


def test_files_function_hashfile_raises_error_on_unknown_algo():
    orig_val = tagfile.cfg['hashing']['algorithm']
    tagfile.cfg['hashing']['algorithm'] = 'not-a-valid-algo'
    _path = os.environ['TAGFILEDEV_MEDIA_PATH']
    paths = tagfile.files.walkdir(_path)
    sample_3_mp4 = paths[0]
    with pytest.raises(ConfigError):
        tagfile.files.hashfile(sample_3_mp4)
    tagfile.cfg['hashing']['algorithm'] = orig_val


def test_files_function_sizefmt():
    assert tagfile.files.sizefmt(0) == '    0B'
    assert tagfile.files.sizefmt(1) == '    1B'
    assert tagfile.files.sizefmt(34) == '   34B'
    assert tagfile.files.sizefmt(267) == '  267B'
    assert tagfile.files.sizefmt(1234) == '  1.2K'
    assert tagfile.files.sizefmt(12345) == ' 12.1K'
    assert tagfile.files.sizefmt(123456) == '120.6K'
    assert tagfile.files.sizefmt(1234567) == '  1.2M'
    assert tagfile.files.sizefmt(12345678) == ' 11.8M'
    assert tagfile.files.sizefmt(123456789) == '117.7M'
    assert tagfile.files.sizefmt(1234567890) == '  1.1G'
    assert tagfile.files.sizefmt(12345678901) == ' 11.5G'
    assert tagfile.files.sizefmt(123456789012) == '115.0G'
    assert tagfile.files.sizefmt(1234567890123) == '  1.1T'
    assert tagfile.files.sizefmt(12345678901234) == ' 11.2T'
    assert tagfile.files.sizefmt(123456789012345) == '112.3T'
    assert tagfile.files.sizefmt(1234567890123456) == '  1.1P'
    assert tagfile.files.sizefmt(12345678901234567) == ' 11.0P'
    assert tagfile.files.sizefmt(123456789012345678) == '109.7P'
    assert tagfile.files.sizefmt(1234567890123456789) == '  1.1E'
    assert tagfile.files.sizefmt(12345678901234567890) == ' 10.7E'
    assert tagfile.files.sizefmt(123456789012345678901) == '107.1E'
    assert tagfile.files.sizefmt(1234567890123456789012) == '  1.0Z'
    assert tagfile.files.sizefmt(12345678901234567890123) == ' 10.5Z'
    assert tagfile.files.sizefmt(123456789012345678901234) == '104.6Z'
    assert tagfile.files.sizefmt(1234567890123456789012345) == '  1.0Y'
    assert tagfile.files.sizefmt(12345678901234567890123456) == ' 10.2Y'
    assert tagfile.files.sizefmt(123456789012345678901234567) == '102.1Y'
    assert tagfile.files.sizefmt(1234567890123456789012345678) == '1021.2Y'
    assert tagfile.files.sizefmt(12345678901234567890123456789) == '10212.1Y'
    assert tagfile.files.sizefmt(123456789012345678901234567890) == '102121.1Y'
