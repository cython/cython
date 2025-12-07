"""
Benchmark recursive async generators implemented in python
by traversing a binary tree.

Author: Kumar Aditya
"""

from __future__ import annotations

import cython
import asyncio
import time
from collections.abc import AsyncIterator


class Tree:
    def __init__(self, left: Tree | None, value: int, right: Tree | None) -> None:
        self.left = left
        self.value = value
        self.right = right

    async def __aiter__(self) -> AsyncIterator[int]:
        if self.left:
            async for i in self.left:
                yield i
        yield self.value
        if self.right:
            async for i in self.right:
                yield i


def tree(input: range) -> Tree | None:
    n = len(input)
    if n == 0:
        return None
    i = n // 2
    return Tree(tree(input[:i]), input[i], tree(input[i + 1:]))


async def bench_async_generators(async_tree) -> None:
    async for _ in async_tree:
        pass


def run_benchmark(repeat=True, scale: cython.long = 1):
    from util import repeat_to_accuracy
    async_tree = tree(range(1000))

    def single_run(scale, timer):
        s: cython.long
        t = timer()
        for s in range(scale):
            asyncio.run(bench_async_generators(async_tree))
        t = timer() - t
        return t

    return repeat_to_accuracy(single_run, scale=scale, repeat=repeat)[0]
