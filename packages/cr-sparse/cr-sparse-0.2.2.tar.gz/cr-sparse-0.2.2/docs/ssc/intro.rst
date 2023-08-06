Introduction to Sparse Subspace Clustering 
==============================================

Consider a dataset of :math:`S` points in the ambient data space
:math:`\mathbb{R}^M` which have been assembled in a matrix :math:`Y` of shape :math:`M \times S`.

In many applications, it often occurs that
if we *group* or *segment* the data set :math:`Y` into
multiple disjoint subsets (clusters): 
:math:`Y = Y_1 \cup \dots \cup Y_K`,
then each subset can be modeled sufficiently well by a low dimensional subspace
:math:`\mathbb{R}^D` where :math:`D \ll M`.
Some of the applications include:
motion segmentation :cite:`tomasi1991detection,tomasi1992shape, 
boult1991factorization,
poelman1997paraperspective,
gear1998multibody,
costeira1998multibody,
kanatani2001motion`, 
face clustering :cite:`basri2003lambertian, ho2003clustering, lee2005acquiring`
and handwritten digit recognition :cite:`zhang2012hybrid`.

*Subspace clustering* is a clustering framework which assumes
that the data-set can be segmented into clusters where points in
different clusters are drawn from different subspaces. Subspace clustering
algorithms are able to simultaneously segment the data into 
clusters corresponding to different subspaces as well as estimate
the subspaces from the data itself.
A comprehensive review of subspace clustering can be found in 
:cite:`vidal2010tutorial`.
Several state of the art algorithms are based on building
subspace preserving representations of individual data points
by treating the data set itself as a (self expressive) dictionary.
For creating subspace preserving representations, one resorts to
using sparse coding algorithms developed in sparse representations and 
compressive sensing literature. 

Two common algorithms are
*Sparse Subspace Clustering* using :math:`\ell_1` *regularization*
(SSC-:math:`\ell_1`):cite:`elhamifar2009sparse, elhamifar2013sparse` 
and *Sparse Subspace Clustering using Orthogonal
Matching Pursuit* (SSC-OMP) :cite:`dyer2013greedy, you2015sparse, you2016scalable`. 
While SSC-:math:`\ell_1` is guaranteed to give correct clustering under
broad conditions (arbitrary subspaces and corrupted data), it
requires solving a large scale convex optimization problem. On
the other hand, SSC-OMP 
is computationally efficient but its clustering accuracy is
poor (especially at low density of data points per subspace).

The dataset :math:`Y` is modeled as being sampled from a collection
or arrangement :math:`\mathcal{U}` of linear (or affine) subspaces
:math:`\mathcal{U}_k \subset \mathbb{R}^M` : 
:math:`\mathcal{U} = \{ \mathcal{U}_1  , \dots , \mathcal{U}_K \}`. 
The union of the subspaces
is denoted as
:math:`Z_{\mathcal{U}} = \mathcal{U}_1 \cup \dots \cup \mathcal{U}_K`.

Let the data set be :math:`\{ y_j  \in \mathbb{R}^M \}_{j=1}^S`
drawn from the union of subspaces under consideration.
:math:`S` is the total number of data points being analyzed
simultaneously.
We put the data points together in a *data matrix* as

.. math::

    Y  \triangleq \begin{bmatrix}
    y_1 & \dots & y_S
    \end{bmatrix}.

Let the vectors be drawn from a set of :math:`K` (linear or affine) subspaces, 
The subspaces are indexed by a variable :math:`k` with :math:`1 \leq k \leq K`.
The :math:`k`-th subspace is denoted by :math:`\mathcal{U}_k`. 
Let the (linear or affine) dimension
of :math:`k`-th subspace be :math:`\dim(\mathcal{U}_k) = D_k` with :math:`D_k \leq D \ll M`.

The vectors in :math:`Y` can be grouped (or segmented or clustered) 
as submatrices 
:math:`Y_1, Y_2, \dots, Y_K` such 
that all vectors in :math:`Y_k` are drawn from the subspace :math:`\mathcal{U}_k`. 
Thus, we can write

.. math::

    Y^* = Y \Gamma = \begin{bmatrix} y_1 & \dots & y_S \end{bmatrix} 
    \Gamma
    = \begin{bmatrix} Y_1 & \dots & Y_K \end{bmatrix} 

where :math:`\Gamma` is an :math:`S \times S` unknown permutation
matrix placing each vector to the right subspace. 

Let there be :math:`S_k` vectors in :math:`Y_k` with
:math:`S = S_1 + \dots + S_K`. 
Let :math:`Q_k` be an orthonormal basis for subspace :math:`\mathcal{U}_k`. Then,
the subspaces can be described as 

.. math::

    \mathcal{U}_k = \{ y \in \mathbb{R}^M : y = \mu_k + Q_k \alpha \}, \quad 1 \leq k \leq K 

For linear subspaces, :math:`\mu_k = 0`.

A dataset where each point can be expressed as a linear combination
of other points in the dataset is said to satisfy 
*self-expressiveness property*. The self-expressive 
representation of a point :math:`y_s` in :math:`Y` is given by 

.. math::

    y_s = Y c_s, \; c_{ss} = 0, \text{ or } Y = Y C, \quad \text{diag}(C) = 0

where :math:`C = \begin{bmatrix}c_1, \dots, c_S \end{bmatrix} \in \mathbb{R}^{S \times S}` 
is the matrix of representation coefficients. 

Let :math:`y_s` belong to :math:`k`-th subspace :math:`\mathcal{U}_k`. 
Let :math:`Y^{-s}` denote the dataset :math:`Y` excluding the point :math:`y_s` 
and  :math:`Y_k^{-s}` denote the
set of points in :math:`Y_k` excluding :math:`y_s`. If :math:`Y_k^{-s}` spans the subspace
:math:`\mathcal{U}_k`, then a representation of :math:`y_s` can be constructed entirely
from the points in :math:`Y_k^{-s}`. A representation is called 
*subspace preserving* if it consists of points within the same subspace.

If :math:`c_i` is a subspace preserving representation of :math:`y_i` and :math:`y_j`
belongs to a different subspace, then :math:`c_{ij} = 0`. Thus, if :math:`C` consists
entirely of subspace preserving representations, then :math:`C_{ij} = 0` whenever
:math:`y_i` and :math:`y_j` belong to different subspaces. 
In other words, if :math:`Y_{-k}` denotes the set of points from 
all subspaces excluding the subspace :math:`Y_k` corresponding
to the point :math:`y_i`, then points in :math:`Y_{-k}` do not
participate in the representation :math:`c_i`.

In the ``cr.sparse.cluster.ssc`` package, we provide a version of
OMP which can be used to construct the sparse self expressive representations 
:math:`C` of :math:`Y`. Once the representation has been constructed, we compute an
affinity matrix :math:`W = |C| + |C^T|`. 

We then apply spectral clustering on :math:`W` to complete SSC-OMP. 
For this, we have written a JAX version of spectral clustering
in ``cr.sparse.cluster.spectral`` package. In particular, it
uses our own Lanczos Bidiagonalization with Partial Orthogonalization (LANBPRO)
algorithm to compute the :math:`K` largest singular values of the
normalized affinity matrix
in as few iterations as possible. The intermediate variables 
:math:`C`, :math:`W` are maintained in the experimental sparse matrices
stored in BCOO format.
The LANBPRO algorithm also works on sparse matrices directly. 
Thus, even though :math:`C` is of size :math:`S \times S`, it can be stored 
efficiently in :math:`O(DS)` storage. This enables us to process 
hundreds of thousands of points efficiently. 
