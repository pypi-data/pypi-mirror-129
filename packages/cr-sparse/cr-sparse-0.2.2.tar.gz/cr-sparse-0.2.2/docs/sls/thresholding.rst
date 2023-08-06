.. _sls:thresholding:

Thresholding
==========================

.. contents::
    :depth: 2
    :local:


For a real or complex scalar :math:`x`, the **hard thresholding** operator can be defined as:

.. math::

    \mathbf{HT}_{\gamma}(x) = \begin{cases} 
     x & \text{for} & |x| \gt \gamma\\
     0 & \text{for} & |x| \le \gamma
    \end{cases}

For a multi-dimensional array, we apply the same operator on each entry in the array.

The **soft thresholding** operator for real and complex scalars can be defined as:

.. math::

    \mathbf{ST}_{\gamma}(x) = \begin{cases} 
     x\left ( 1 -  \frac{\gamma}{|x|} \right ) & \text{for} & |x| \gt \gamma\\
     0 & \text{for} & |x| \le \gamma
    \end{cases}

For real numbers, this reduces to:

.. math::

    \mathbf{ST}_{\gamma}(x) = \begin{cases} 
     x - \gamma & \text{for} & x \gt \gamma \\
     x + \gamma & \text{for} & x \lt -\gamma \\
     0 & \text{for} & |x| \le \gamma
    \end{cases}


:cite:`chen2014irregular` consider the general minimization problem:

.. math::

    \widehat{x} = \text{arg} \min_{x} \| b - A x \|_2^2 + \mathbf{R}(x)

where :math:`x` is a vector in the model space, :math:`b` is a vector in the data space,
:math:`A` is a linear operator from model space to data space, and
:math:`\mathbf{R}(x)` is the regularization term on the model vector.
They specifically consider the regularizations

.. math:: 

    \mathbf{R}(x) =  \tau \|x\|_p^p
    
for :math:`p`-norms where :math:`0 \leq p \leq 1`. 
This can be solved by the IST (Iterative Shrinkage and Thresholding)
algorithm where the thresholding operator depends on the selection of :math:`p`-norm and the
regularization parameter :math:`\tau`.
They describe the IST iterations in terms of a more general thresholding operator :math:`\mathbf{T}_{\gamma(\tau, p)}(x)`:

.. math::

    x_{n+1} = \mathbf{T}_{\gamma(\tau, p)}\left [x_n + A^H (b - A x_n) \right ]


They provide the definition of the thresholding operator for:

* :math:`p=0` **hard thresholding**
* :math:`p=1` **soft thresholding**
* :math:`p=1/2` **half thresholding**


.. rubric:: Hard thresholding

Whe :math:`p=0`, we have:

.. math::

    \mathbf{R}(x) = \| x \|_0

.. math::

    \gamma(\tau, 0) = \sqrt{2 \tau}

The hard thresholding operator reduces to:

.. math::

    \mathbf{T}_{\gamma(\tau, 0)}(x) = \begin{cases} 
     x & \text{for} & |x| \gt \gamma (\tau, 0)\\
     0 & \text{for} & |x| \le \gamma  (\tau, 0)
    \end{cases}

.. rubric:: Soft thresholding

Whe :math:`p=1`, we have:

.. math::

    \mathbf{R}(x) = \| x \|_1

.. math::

    \gamma(\tau, 1) = \tau

The soft thresholding operator reduces to:

.. math::

    \mathbf{T}_{\gamma(\tau, 1)}(x) = \begin{cases} 
     x\left ( 1 -  \frac{\gamma}{|x|} \right ) & \text{for} & |x| \gt \gamma (\tau, 1)\\
     0 & \text{for} & |x| \le \gamma (\tau, 1)
    \end{cases}


.. rubric:: Half thresholding

Whe :math:`p=\frac{1}{2}`, we have:

.. math::

    \mathbf{R}(x) = \| x \|_{\frac{1}{2}}^{\frac{1}{2}}

.. math::

    \gamma(\tau, \frac{1}{2}) = \frac{3}{2} \tau^{\frac{2}{3}}


The half thresholding operator is more complicated:


.. math::

    \mathbf{T}_{\gamma(\tau, 1)}(x) = \begin{cases} 
     \frac{2}{3} x\left ( 1 +  \cos \left ( \frac{2}{3} \pi - \frac{2}{3} \arccos \left ( \frac{\tau}{8} \left (\frac{|x|}{3} \right)^{\frac{3}{2}}
         \right )   \right )  \right ) 
     & \text{for} & |x| \gt \gamma (\tau, \frac{1}{2})\\
     0 & \text{for} & |x| \le \gamma (\tau, \frac{1}{2})
    \end{cases}
