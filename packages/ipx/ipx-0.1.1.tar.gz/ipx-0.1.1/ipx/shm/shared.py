# -*- coding: utf-8 -*-
#
#   SHM: Shared Memory
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import json
import mmap
from typing import Union

from .cache import CycledCache


class SharedMemoryCache:

    def __init__(self, size: int):
        super().__init__()
        shm = mmap.mmap(fileno=-1, length=size, flags=mmap.MAP_SHARED, prot=(mmap.PROT_READ | mmap.PROT_WRITE))
        self.__cache = CycledCache(buffer=shm, head_length=4)
        self.__shm = shm

    @property
    def shm(self) -> mmap.mmap:
        return self.__shm

    def close(self):
        self.__shm.close()

    def get(self) -> Union[str, dict, list, None]:
        data = self.__cache.get()
        if data is not None:
            data = data.decode('utf-8')
            return json.loads(data)

    def put(self, o: Union[str, dict, list]) -> bool:
        data = json.dumps(o)
        data = data.encode('utf-8')
        return self.__cache.put(data=data)
