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

from test.config import ENABLE_STATS_TESTS
from tinyqsim.gates import ID, CX, X, H, SWAP
from tinyqsim.quantum import (n_qubits, basis_names, random_state, zeros_state,
                              random_unitary, unitary_to_tensor, tensor_to_state,
                              tensor_to_unitary, state_to_tensor, apply_tensor,
                              compose_tensor, state_dict, probabilities,
                              probability_dict)
from tinyqsim.utils import kron_n, normalize, is_unitary

CX_BIG = np.array([[1, 0, 0, 0],  # Big-endian CX gate
                   [0, 0, 0, 1],
                   [0, 0, 1, 0],
                   [0, 1, 0, 0]])


def create_state(nqubits: int) -> ndarray:
    return normalize(np.arange(2 ** nqubits))


def test_zeros_state():
    assert_array_equal(zeros_state(1), [1, 0])
    assert_array_equal(zeros_state(3), [1, 0, 0, 0, 0, 0, 0, 0])


def test_random_state_norm():
    """ Test random state has expected norm."""
    nruns = 10
    nqubits = 8
    for _ in range(nruns):
        psi = random_state(nqubits)  # / sqrt(2)
        assert (norm(psi) == approx(1.0, abs=1e-10))


@pytest.mark.skipif(not ENABLE_STATS_TESTS, reason='Skipping Statistical Test')
def test_random_state_stddev():
    """ Test random state has expected standard deviation."""
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


def test_random_unitary():
    u1 = random_unitary(1)
    assert u1.shape == (2, 2)
    assert is_unitary(u1)
    u2 = random_unitary(2)
    assert u2.shape == (4, 4)
    assert is_unitary(u2)
    u3 = random_unitary(3)
    assert u3.shape == (8, 8)
    assert is_unitary(u3)


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


def test_state_to_tensor():
    assert_array_equal(state_to_tensor(np.array([1, 2])), [1, 2])
    assert_array_equal(state_to_tensor(np.array([1, 2, 3, 4, 5, 6, 7, 8])),
                       np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))


def test_tensor_to_state():
    assert_array_equal(tensor_to_state(np.array([1, 2])), [1, 2])
    assert_array_equal(tensor_to_state(np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])),
                       [1, 2, 3, 4, 5, 6, 7, 8])


def test_unitary_to_tensor():
    t = unitary_to_tensor(CX)
    exp = np.array([[[[1, 0], [0, 0]],
                     [[0, 1], [0, 0]]],
                    [[[0, 0], [0, 1]],
                     [[0, 0], [1, 0]]]])
    assert_allclose(t, exp)


def test_tensor_to_unitary():
    t = np.array([[[[1, 0], [0, 0]],
                   [[0, 1], [0, 0]]],
                  [[[0, 0], [0, 1]],
                   [[0, 0], [1, 0]]]])
    m = tensor_to_unitary(t)
    assert_allclose(m, CX)


def test_apply_tensor():
    u = kron(X, CX)
    state = random_state(5)
    u2 = kron((kron(ID, SWAP) @ kron(CX, X) @ kron(ID, SWAP)), kron_n(2, ID))

    tu = unitary_to_tensor(u)
    tv = state_to_tensor(state)

    assert_allclose(tensor_to_state(apply_tensor(tv, tu, [1, 0, 2])),
                    u2 @ state)


def test_compose_tensor():
    nq = 2
    tu1 = unitary_to_tensor(np.eye(2 ** nq))
    th = unitary_to_tensor(H)
    tcx = unitary_to_tensor(CX)
    tu2 = compose_tensor(tu1, th, [0])
    tu3 = compose_tensor(tu2, tcx, [0, 1])
    m = tensor_to_unitary(tu3)
    exp = np.array([[1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, -1], [0, 1, -1, 0]])
    assert_allclose(m * sqrt(2), exp)


def test_state_dict():
    assert state_dict(np.array([1, 2, 3, 4])) == {'00': 1, '01': 2, '10': 3, '11': 4}


def test_probabilities():
    a = np.array([-2, 1j, 2, 3]) / sqrt(18)
    assert_allclose(probabilities(a, [0, 1]), [2 / 9, 5 / 90, 2 / 9, 1 / 2])
    assert_allclose(probabilities(a, [0]), [5 / 18, 13 / 18])
    assert_allclose(probabilities(a, [1]), [4 / 9, 5 / 9])


def test_probability_dict():
    a = np.array([-2, 1j, 2, 3]) / sqrt(18)
    dic = probability_dict(a)
    exp = {'00': 2 / 9, '01': 5 / 90, '10': 2 / 9, '11': 0.5}
    for k in (list(set(exp.keys()).union(dic.keys()))):
        assert_allclose(dic[k], exp[k])

# Note: Measurement tests are now in a separate module
