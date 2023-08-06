Computation Time Comparison of Sparse Recovery Methods
===============================================================

Performance on CPU
-------------------------------------------------

.. rubric:: System configuration

* MacBook Pro 2019 Model
* Processor: 1.4 GHz Quad Core Intel Core i5
* Memory: 8 GB 2133 MHz LPDDR3

.. rubric:: Problem Specification

* Gaussian sensing matrices (normalized to unit norm columns)
* Sparse vectors with non-zero entries drawn from Gaussian distributions
* M, N, K have been chosen so that all algorithms under comparison are known to converge to successful 
  recovery.

.. rubric:: Remarks

* All algorithms have been benchmarked for both 32-bit and 64-bit floating point calculations. Benchmarks are separately presented for them.
* It was separately verified that sparse recovery results were identical for both with or without JIT acceleration.
* Python ``%timeit`` magic was used for benchmarking. 
* Every algorithm has been run several times on the given problem and the average time has been computed.
* Average times have been reported in jit_off and jit_on columns with milliseconds units.

.. rubric:: Algorithm structures

The table below highlights the differences
in the structure of different algorithms under consideration. These differencess are key reason for the computational
complexity.

.. list-table:: Comparison of algorithm structures
    :header-rows: 1

    * - method
      - Correlation with residual
      - Least squares
      - Hard thresholding
      - Step size
    * - OMP
      - Yes
      - Cholesky update
      - 1 atom
      - No
    * - SP
      - Yes
      - 2 (2K atoms and K atoms)
      - K atoms and K atoms
      - No
    * - CoSaMP
      - Yes
      - 1 (3K atoms)
      - 2K atoms and K atoms
      - No
    * - IHT
      - Yes
      - 0
      - K atoms
      - Fixed
    * - NIHT
      - Yes
      - 0
      - K atoms
      - Dynamic
    * - HTP
      - Yes
      - 1 (K atoms)
      - K atoms
      - Fixed
    * - NHTP
      - Yes
      - 1 (K atoms)
      - K atoms
      - Dynamic




.. rubric:: Benchmarks for 32-bit

.. list-table:: Average time (msec) and speedups due to JIT acceleration
    :header-rows: 1

    * - method
      - M
      - N
      - K
      - iterations
      - jit_off
      - jit_on
      - speedup
    * - OMP
      - 200
      - 1000
      - 20
      - 20
      - 105.78
      - 2.14
      - 49.48
    * - SP
      - 200
      - 1000
      - 20
      - 3
      - 1645.32
      - 2.73
      - 602.34
    * - CoSaMP
      - 200
      - 1000
      - 20
      - 4
      - 309.01
      - 6.20
      - 49.84
    * - IHT
      - 200
      - 1000
      - 20
      - 65
      - 232.99
      - 36.27
      - 6.42
    * - NIHT
      - 200
      - 1000
      - 20
      - 16
      - 240.96
      - 5.64
      - 42.72
    * - HTP
      - 200
      - 1000
      - 20
      - 5
      - 1491.00
      - 13.71
      - 108.76
    * - NHTP
      - 200
      - 1000
      - 20
      - 4
      - 1467.35
      - 1.98
      - 741.88


.. rubric:: Benchmarks for 64-bit

.. list-table:: Average time (msec) and speedups due to JIT acceleration
    :header-rows: 1

    * - method
      - M
      - N
      - K
      - iterations
      - jit_off
      - jit_on
      - speedup
    * - OMP
      - 200
      - 1000
      - 20
      - 20
      - 112.69
      - 2.43
      - 46.42
    * - SP
      - 200
      - 1000
      - 20
      - 4
      - 1324.79
      - 4.49
      - 295.02
    * - CoSaMP
      - 200
      - 1000
      - 20
      - 5
      - 293.50
      - 9.82
      - 29.90
    * - IHT
      - 200
      - 1000
      - 20
      - 77
      - 209.22
      - 48.81
      - 4.29
    * - NIHT
      - 200
      - 1000
      - 20
      - 19
      - 196.66
      - 7.23
      - 27.21
    * - HTP
      - 200
      - 1000
      - 20
      - 6
      - 1218.62
      - 18.96
      - 64.28
    * - NHTP
      - 200
      - 1000
      - 20
      - 5
      - 1238.37
      - 2.79
      - 443.68
      
​

Subjective Analysis 
----------------------------

.. rubric:: 64-bit vs 32-bit

* There are differences in number of iterations for convergence
* Every algorithm except OMP takes more iterations to converge with 64-bit compared to 32-bit floating point computations.
* In case of OMP, number of iterations is decided by sparsity. Hence, it is same for both 32-bit and 64-bit.
* It was separately established that success rates of these algorithms suffers somewhat for 32-bit floating point calculations.
* In other words, 32-bit computations are more aggressive and may be inaccurate.
* On CPUs, the floating point units are 64-bit. Hence, using 32-bit floating point computations doesn't give us much speedup. 
  32-bit computation would be more relevant for GPUs.
* The general trend of computation times (with JIT on) for both 32-bit and 64-bit are similar. i.e. algorithms which are
  slower for 32-bit are slower for 64-bit too.

Rest of the discussion is focused on the results for 64-bit sparse recovery. 
.. rubric:: All algorithms without JIT vs with JIT

* It is clear that all algorithms exhibit significant speedups with the introduction of 
  JIT acceleration.
* The speedup is as low as 4x for IHT and as high as 443x in NHTP.
* Before JIT, OMP is the fastest algorithm and SP is the slowest. 
* After JIT acceleration, OMP is the fastest algorithm while IHT is the slowest. NHTP comes as a close second. 
  Incidentally, NHTP is faster than OMP for 32-bit.
* NHTP and SP show significant speedups with JIT. HTP, OMP, CoSaMP and NIHT show modest gains. IHT doesn't seem to provide much 
  optimization opportunities.
* It appears that steps like dynamic step size computation (in NIHT, NHTP) and 
  least squares (in SP, CoSaMP, HTP, NHTP)
  tend to get aggressively optimized and lead to massive speed gains.

.. rubric:: OMP

* With JIT on, OMP is actually one of the fastest algorithms in the mix (for both 32-bit and 64-bit).
* In the current implementations, OMP is the only one in which the least squares step has
  been optimized using Cholesky updates. 
* This is possible as OMP structure allows for adding atoms one at a time to the mix.
* Other algorithms change several atoms [add / remove] in each iteration. Hence, such
  optimizations are not possible.
* The least squares steps in other algorithms can be accelerated using small number of conjugate gradients
  iterations. However, this hasn't been implemented yet.


.. rubric:: SP vs CoSaMP

* CoSaMP has one least squares step (on 3K indices) in each iteration.
* SP (Subspace Pursuit) has two least squares steps in each iteration.
* Without JIT, CoSaMP is 4x faster.
* With JIT, SP becomes 2x faster than CoSaMP.
* Thus, SP seems to provide more aggressive optimization opportunities.

.. rubric:: IHT vs NIHT

* IHT and NIHT are both simple algorithms. They don't involve a least squares step in their iterations.
* The main difference is that the step-size fixed for IHT and it is computed on every iteration in NIHT.
* The dynamic step size leads to reduction in the number of iterations for NIHT. From 77 to 19, 4x reduction.
* Without JIT, there is no significant difference between IHT and NIHT.
  Thus, step-size computation seems to contribute a lot to computation time without acceleration.
* With JIT, step-size computation seems to be aggressively optimized.
  NIHT after JIT is 6x faster than IHT even though the number of iterations reduces by only 4 times
  and there is extra overhead of computing the step size. This appears to be counter-intuitive.

.. rubric:: IHT vs HTP

* The major difference in the two algorithms is that HTP performs a least squares estimate
  on the current guess of signal support
* The number of iterations reduces 13 times due to the least squares step but it has its own extra overhead.
* Without JIT, HTP becomes much slower than IHT (6x slower). Thus, overhead of a least squares step is quite high.
* HTP is about 3x faster than IHT with JIT. This makes sense. The number of iterations reduced by 13
  times and the overhead of least squares was added.

.. rubric:: HTP vs NHTP

* Just like NIHT, NHTP also introduces computing the step size dynamically in every iteration.
* It helps in reducing the number of iterations from 6 to 5.
* In this case, the benefit of dynamic step size is not visible much in terms of iterations.
* Without JIT, NHTP is somewhat slower than HTP.
* However, with JIT, NHTP is 6x faster than HTP. This speedup is unusual as there is just
  20% reduction in number of iterations and there is the overhead of step size computation.

 

