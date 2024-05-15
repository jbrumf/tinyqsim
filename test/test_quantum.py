"""
Pytest unit tests for quantum module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import sqrt

import pytest
from numpy import kron
from numpy.testing import assert_array_equal, assert_allclose
from pytest import approx

from tinyqsim.gates import ID, CX, X, SWAP
from tinyqsim.quantum import *
from tinyqsim.utils import kron_n, normalize

ENABLE_STATS_TESTS = True  # Enable stochastic tests that may occasionally fail

CX_BIG = np.array([[1, 0, 0, 0],  # Big-endian CX gate
                   [0, 0, 0, 1],
                   [0, 0, 1, 0],
                   [0, 1, 0, 0]])


def create_state(nqubits: int) -> ndarray:
    return normalize(np.arange(2 ** nqubits))


def test_zeros_state():
    assert_array_equal(zeros_state(1), [1, 0])
    assert_array_equal(zeros_state(3), [1, 0, 0, 0, 0, 0, 0, 0])


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


def test_n_qubits():
    # Test with vector
    assert_array_equal(n_qubits(np.array([])), 0)
    v3 = np.array([1, 0, 0, 0, 0, 0, 0, 0])
    assert_array_equal(n_qubits(v3), 3)
    assert_array_equal(n_qubits(np.array([1, 0])), 1)

    # Test with matrix
    assert_array_equal(n_qubits(ID), 1)
    assert_array_equal(n_qubits(kron(ID, ID)), 2)


def test_basis_names():
    assert_array_equal(basis_names(1), ['0', '1'])
    assert_array_equal(basis_names(3), ['000', '001', '010', '011', '100', '101', '110', '111'])


def test_apply_tensor():
    u = kron(X, CX)
    state = random_state(5)
    u2 = kron((kron(ID, SWAP) @ kron(CX, X) @ kron(ID, SWAP)), kron_n(2, ID))

    tu = unitary_to_tensor(u)
    tv = state_to_tensor(state)

    assert_allclose(tensor_to_state(apply_tensor(tv, tu, [1, 0, 2])),
                    u2 @ state)


def test_to_tensor():
    assert_array_equal(state_to_tensor(np.array([1, 2])), [1, 2])
    assert_array_equal(state_to_tensor(np.array([1, 2, 3, 4, 5, 6, 7, 8])),
                       np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))


def test_from_tensor():
    assert_array_equal(tensor_to_state(np.array([1, 2])), [1, 2])
    assert_array_equal(tensor_to_state(np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])),
                       [1, 2, 3, 4, 5, 6, 7, 8])


def test_components_dict():
    assert components_dict(np.array([1, 2, 3, 4])) == {'00': 1, '01': 2, '10': 3, '11': 4}


def test_probabilities():
    a = np.array([-2, 1j, 2, 3]) / sqrt(18)
    assert_allclose(probabilities(a, [0, 1]), [2 / 9, 5 / 90, 2 / 9, 1 / 2])
    assert_allclose(probabilities(a, [0]), [5 / 18, 13 / 18])
    assert_allclose(probabilities(a, [1]), [4 / 9, 5 / 9])

# def test_probability_dict():
# def test_counts_dict

# Note: Measurement tests are now in a separate module
