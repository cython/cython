# mode: run
# tag: no_cache_builtins

# memoryview was broken with cache_builtins=False (the exception throwing code needed the GIL)
# this just repeats the tests with it off

include "memoryview.pyx"
