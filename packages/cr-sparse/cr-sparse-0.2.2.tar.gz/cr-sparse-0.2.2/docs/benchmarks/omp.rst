Orthogonal Matching Pursuit
=============================



.. rubric:: Speed benchmarks for JAX implementation

Each row of the following table describes:

* problem type and configuration (M x N is dictionary size, K is sparsity level)
* Average time taken in CPU/GPU configurations
* Speed improvement ratios

.. rubric:: System used

* All benchmarks have been generated on Google Colab
* CPU and GPU configurations Google Colab have been used

.. list-table::
    :header-rows: 1

    * - M
      - N
      - K 
      - CPU
      - CPU + JIT
      - CPU / CPU + JIT
      - GPU 
      - GPU + JIT
      - GPU / GPU + JIT
      - CPU + JIT / GPU + JIT
    * - 256
      - 1024
      - 16
      - 148 ms
      - 8.27 ms
      - 17.9x
      - 139 ms
      - 1.28 ms
      - 108x
      - 6.46x

.. rubric:: Observations

* JIT (Just In Time) compilation seems to give significant performance improvements 
  in both CPU and GPU architectures
* Current implementation seems to be slower on GPU vs CPU with JIT. 
* GPU speed gain over CPU (with JIT on) is relatively meager. 
  On TensorFlow, people regularly report 30x improvements between CPU to GPU 
  for neural networks implemented using Keras. 


.. rubric:: Possible deficiencies

* There is opportunity to improve parallelization in the OMP implementation.
* Cholesky update based implements depends heavily on solving triangular systems.
* GPUs may not be great at solving triangular systems. 


