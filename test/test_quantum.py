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


def test_permute_unitary():
    # Trivial case of 1 qubit
    x = permute_unitary(X, [0])
    assert_array_equal(x, X)

    # Swapping a 2-qubit gate
    x = permute_unitary(CX, [1, 0])
    assert_array_equal(x, CX_BIG)
    x = permute_unitary(CX, [0, 1])
    assert_array_equal(x, CX)

    # Permutation of all |0> state should have no effect
    all_zeros = kron_n(4, ID)
    x = permute_unitary(all_zeros, [2, 1, 3, 0])
    assert_array_equal(x, all_zeros)

    # More complex cases
    u = kron_all([X, CX, SWAP])
    x = permute_unitary(u, [4, 3, 2, 1, 0])
    assert_array_equal(x, kron_all([SWAP, CX_BIG, X]))

    u = kron_all([X, CX])
    exp = kron(ID, SWAP) @ kron(CX, X) @ kron(ID, SWAP)
    assert_array_equal(permute_unitary(u, [1, 0, 2]), exp)


def test_apply():
    u = kron(X, CX)
    state = random_state(5)
    u2 = kron((kron(ID, SWAP) @ kron(CX, X) @ kron(ID, SWAP)), kron_n(2, ID))
    assert_allclose(apply(state, u, [1, 0, 2]),
                    u2 @ state)


def test_swap_endian():
    x = swap_endian(CX)
    assert_array_equal(x, CX_BIG)

    s = kron_all([X, CX, SWAP])
    assert_array_equal(swap_endian(s), kron_all([SWAP, CX_BIG, X]))
    assert_array_equal(swap_endian(swap_endian(s)), s)


def test_to_tensor():
    assert_array_equal(state_to_tensor(np.array([1, 2])), [1, 2])
    assert_array_equal(state_to_tensor(np.array([1, 2, 3, 4, 5, 6, 7, 8])),
                       np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))


def test_from_tensor():
    assert_array_equal(tensor_to_state(np.array([1, 2])), [1, 2])
    assert_array_equal(tensor_to_state(np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])),
                       [1, 2, 3, 4, 5, 6, 7, 8])


def test_subscript():
    assert subscript([1]) == 'b'
    assert subscript([0, 3, 5]) == 'adf'


def test_sum_except_qubits():
    assert_array_equal(sum_except_qubits(np.array(range(8)), [0]), [6, 22])
    assert_array_equal(sum_except_qubits(np.array(range(8)), [1]), [10, 18])
    assert_array_equal(sum_except_qubits(np.array(range(8)), [2]), [12, 16])
    assert_array_equal(sum_except_qubits(np.array(range(8)), [1, 2]), [4, 6, 8, 10])
    assert_array_equal(sum_except_qubits(np.array(range(8)), [0, 2]), [2, 4, 10, 12])


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
