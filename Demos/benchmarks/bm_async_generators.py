"""
Benchmark recursive async generators implemented in python
by traversing a binary tree.

Author: Kumar Aditya
"""

from __future__ import annotations

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



def run_benchmark(repeat=10, scale: cython.long = 1, timer=time.perf_counter):
    s: cython.long

    async_tree = tree(range(1000))

    timings = []
    for _ in range(repeat):
        t = timer()
        for s in range(scale):
            asyncio.run(bench_async_generators(async_tree))
        t = timer() - t
        timings.append(t)
    return timings
