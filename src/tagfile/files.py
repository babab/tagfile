'''Filesystem functions'''

# file: src/tagfile/files.py

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

import hashlib
import os

import tagfile


def walkdir(filepath):
    paths = []
    for root, directories, files in os.walk(filepath):
        for filename in files:
            filepath = os.path.join(root, filename)
            paths.append(filepath)
    return paths


def hashfile(filepath):
    if tagfile.cfg['hash-algo'] == 'md5':
        h = hashlib.md5()
    elif tagfile.cfg['hash-algo'] == 'sha1':
        h = hashlib.sha1()
    else:
        raise tagfile.ConfigError('Invalid "hash-algo" in configuration')

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(tagfile.cfg['hash-buf-size'])
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def sizefmt(value, padding=6):
    nbytes = float(value)
    if nbytes < 1024:
        return '{0:>{pad}}'.format('{:.0f}B'.format(nbytes), pad=padding)
    for i, suffix in enumerate('KMGTPEZY'):
        factor = 1024 ** (i + 2)
        if nbytes < factor:
            break
    num = 1024 * nbytes / factor
    return '{0:>{pad}}'.format('{:.1f}{}'.format(num, suffix), pad=padding)
