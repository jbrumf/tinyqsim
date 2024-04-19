"""
Pytest unit tests for quantum module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import sqrt

import numpy as np
import pytest
from numpy import kron, ndarray
from numpy.linalg import norm
from numpy.testing import assert_array_equal, assert_allclose
from pytest import approx

from tinyqsim.gates import ID, CX, X, SWAP
from tinyqsim.quantum import (init_state, n_qubits, permute_qubits, swap_endian, map_qubits,
                              random_state)
from tinyqsim.utils import kron_all, kron_n, normalize

ENABLE_STATS_TESTS = True  # Enable stochastic tests that may occasionally fail

CX_BIG = np.array([[1, 0, 0, 0],  # Big-endian CX gate
                   [0, 0, 0, 1],
                   [0, 0, 1, 0],
                   [0, 1, 0, 0]])


def create_state(nqubits: int) -> ndarray:
    return normalize(np.arange(2 ** nqubits))


def test_init_qubits():
    assert_array_equal(init_state(1), [1, 0])
    assert_array_equal(init_state(3), [1, 0, 0, 0, 0, 0, 0, 0])


def test_n_qubits():
    # Test with vector
    assert_array_equal(n_qubits(np.array([])), 0)
    v3 = np.array([1, 0, 0, 0, 0, 0, 0, 0])
    assert_array_equal(n_qubits(v3), 3)
    assert_array_equal(n_qubits(np.array([1, 0])), 1)

    # Test with matrix
    assert_array_equal(n_qubits(ID), 1)
    assert_array_equal(n_qubits(kron(ID, ID)), 2)


def test_qubit_permutation():
    # Trivial case of 1 qubit
    x = permute_qubits(X, [0])
    assert_array_equal(x, X)

    # Swapping a 2-qubit gate
    x = permute_qubits(CX, [1, 0])
    assert_array_equal(x, CX_BIG)
    x = permute_qubits(CX, [0, 1])
    assert_array_equal(x, CX)

    # Permutation of all |0> state should have no effect
    all_zeros = kron_n(4, ID)
    x = permute_qubits(all_zeros, [2, 1, 3, 0])
    assert_array_equal(x, all_zeros)

    # More complex cases
    u = kron_all([X, CX, SWAP])
    x = permute_qubits(u, [4, 3, 2, 1, 0])
    assert_array_equal(x, kron_all([SWAP, CX_BIG, X]))

    u = kron_all([X, CX])
    exp = kron(ID, SWAP) @ kron(CX, X) @ kron(ID, SWAP)
    assert_array_equal(permute_qubits(u, [1, 0, 2]), exp)


def test_map_qubits():
    u = kron_all([X, CX])
    state = create_state(5)
    exp = kron((kron(ID, SWAP) @ kron(CX, X) @ kron(ID, SWAP)), kron_n(2, ID))
    nqubits = n_qubits(state)
    u2 = map_qubits(u, nqubits, [1, 0, 2])
    assert_allclose(u2, exp)


def test_swap_endian():
    x = swap_endian(CX)
    assert_array_equal(x, CX_BIG)

    s = kron_all([X, CX, SWAP])
    assert_array_equal(swap_endian(s), kron_all([SWAP, CX_BIG, X]))
    assert_array_equal(swap_endian(swap_endian(s)), s)


@pytest.mark.skipif(not ENABLE_STATS_TESTS, reason='Skipping Statistical Test')
def test_random_state():
    """ Test random state has expected norm and standard deviation."""
    nruns = 10
    nqubits = 8
    zmax = 0.15  # Test threshold
    n = 2 ** nqubits
    sigma = 1 / sqrt(2 * n)  # Expected standard deviation
    for _ in range(nruns):
        psi = random_state(nqubits)  # / sqrt(2)
        # Check norm of state is approximately 1
        assert (norm(psi) == approx(1.0, abs=1e-10))
        # Check standard deviation is approximately as expected
        zr = np.std(psi.real) / sigma
        zi = np.std(psi.imag) / sigma
        assert abs(1 - zr) < zmax
        assert abs(1 - zi) < zmax

# Note: Measurement tests are now in a separate module
