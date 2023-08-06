.. _api:dict:

Sparsifying Dictionaries and Sensing Matrices
===================================================


.. currentmodule:: cr.sparse.dict


Functions for constructing sparsying dictionaries and sensing matrices
--------------------------------------------------------------------------


.. autosummary::
  :toctree: _autosummary


    gaussian_mtx
    rademacher_mtx
    random_onb
    hadamard
    hadamard_basis
    dirac_hadamard_basis
    cosine_basis
    dirac_cosine_basis
    dirac_hadamard_cosine_basis
    fourier_basis
    random_orthonormal_rows



Dictionary properties
-------------------------


.. autosummary::
  :toctree: _autosummary

    gram
    frame
    coherence_with_index
    coherence
    frame_bounds
    upper_frame_bound
    lower_frame_bound
    babel



Dictionary comparison
----------------------------

These functions are useful for comparing dictionaries
during the dictionary learning process. 

.. autosummary::
  :toctree: _autosummary

    mutual_coherence_with_index
    mutual_coherence
    matching_atoms_ratio