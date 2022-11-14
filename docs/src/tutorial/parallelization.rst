.. _parallel-tutorial:

=======================
Writing parallel code with Cython
=======================

One method of speeding up your code that Cython supports is parallelization:
here you write code that can be run on multiple cores of your CPU simultaneously.
For code that lends itself to parallelization this can produce quite
dramatic speed-ups, equal to the number of cores your CPU has (for example
a 4× speed-up on a 4-core CPU).

This tutorial assumes that you are already familiar with Cython's 
:ref:`"typed memoryviews"<memoryviews>` (since code using memoryviews is often
the sort of code that's easy to parallelize with Cython), and also that you're
somewhat familiar with the pitfalls of writing parallel code in general
(it aims to be a Cython tutorial rather than a complete introduction
to parallel programming).

Before starting, a few notes:

- Not all code can be parallelized - for some code the algorithm simply
  relies on code being executed in order and you should not attempt to
  parallelize this code. A cumulative sum is a good example.
  
- Not all code is worth parallelizing. There's a reasonable amount of
  overhead in starting a parallel section and so you need to make sure
  that you're operating on enough data to make this overhead worthwhile.
  Additionally, make sure that you are doing actual work on the data!
  Multiple threads simply reading the same data tends not to parallelize
  too well. If in doubt, time it.

- Cython requires the contents of parallel blocks to be ``nogil``. If
  your algorithm requires access to Python objects then it may not be
  suitable for parallelization.
  
- Cython's inbuilt parallelization uses the OpenMP constructs
  ``omp parallel for`` and ``omp parallel``. These are ideal
  for parallelizing relatively small, self-contained blocks of code
  (especially loops). However, If you want to use other models of 
  parallelization such as spawning and waiting for tasks, or 
  off-loading some "side work" to a continuously running secondary 
  thread, then you might be better using other methods (such as 
  Python's ``threading`` module).
  
- Actually implementing your parallel Cython code should probably be 
  one of the last steps in your optimization. You should start with
  some working serial code first. However, it's probably worth thinking
  about early since it may affect your choice of algorithm.

This tutorial does not aim to explore all the options available to
customize parallelization. See 
  
The first th
