"""
Pytest unit tests for gates module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import pi

from numpy import kron, eye, zeros
from numpy.testing import (assert_array_equal,
                           assert_array_almost_equal)

from tinyqsim.gates import *
from tinyqsim.utils import is_unitary


# Note:
#   Controlled versions of gates are not tested explicitly as the underlying
#   gates are tested and the generic control mechanism is tested by 'test_cu'.

def test_id():
    assert is_unitary(ID)
    assert_array_equal(ID @ ID, ID)


def test_x():
    assert is_unitary(X)
    assert_array_equal(X @ X, ID)


def test_y():
    assert is_unitary(Y)
    assert_array_equal(Y @ Y, ID)


def test_z():
    assert is_unitary(Z)
    assert_array_equal(Z @ Z, ID)


def test_xyz():
    assert_array_equal(X @ Y, Z * 1j)
    assert_array_equal(Y @ Z, X * 1j)
    assert_array_equal(Z @ X, Y * 1j)


def test_h():
    assert is_unitary(H)
    assert_array_almost_equal(H @ H, ID)


def test_s():
    assert is_unitary(S)
    assert_array_almost_equal(S @ S, Z)


def test_sdg():
    assert is_unitary(Sdg)
    assert_array_almost_equal(S @ Sdg, ID)


def test_t():
    assert is_unitary(T)
    assert_array_almost_equal(T @ T, S)


def test_tdg():
    assert is_unitary(Sdg)
    assert_array_almost_equal(T @ Tdg, ID)


def test_p():
    assert is_unitary(P(pi / 3))
    assert_array_almost_equal(P(0), ID)
    assert_array_almost_equal(P(pi), Z)
    assert_array_almost_equal(P(pi / 2), S)
    assert_array_almost_equal(P(pi / 4), T)


def test_rx():
    # Note: RX(pi) and X differ by a global phase of 'i'
    assert is_unitary(RX(pi / 3))
    assert_array_almost_equal(RX(0), ID)
    assert_array_almost_equal(RX(2 * pi), -ID)
    assert_array_almost_equal(RX(pi) * RX(pi), -X)
    assert_array_almost_equal(RX(pi), -1j * X)
    a = RX(pi / 3)
    assert_array_almost_equal(a @ a @ a, -1j * X)


def test_ry():
    # Note: RY(pi) and Y differ by a global phase of 'i'
    assert is_unitary(RY(pi / 3))
    assert_array_almost_equal(RY(0), ID)
    assert_array_almost_equal(RY(pi), -1j * Y)


def test_rz():
    # Note: RZ(pi) and Z differ by a global phase of 'i'
    assert is_unitary(RZ(pi / 3))
    assert_array_almost_equal(RZ(0), ID)
    assert_array_almost_equal(RZ(pi), -1j * Z)


def test_sx():
    assert is_unitary(SX)
    assert_array_almost_equal(SX @ SX, X)


def test_equivalences():
    """ Test for expected equivalences allowing for global phase."""
    assert np.allclose(1j * RX(pi), X)
    assert np.allclose(1j * RY(pi), Y)


def test_swap():
    assert is_unitary(SWAP)
    assert_array_equal(SWAP @ SWAP, kron(ID, ID))


def test_cu():
    assert is_unitary(cu(CX))

    # Test CU on k*k matrix (not unitary for test)
    def cu_aux(k):
        k2 = k * k
        u = np.arange(2, k2 + 2).reshape((k, k))
        ref = np.array(u)
        u1 = cu(u)
        assert_array_equal(u, ref)  # Check 'u' unchanged
        assert_array_equal(u1[0:k, 0:k], eye(k))
        assert_array_equal(u1[k:k2, 0:k], zeros((k, k)))
        assert_array_equal(u1[0:k, k:k2], zeros((k, k)))
        assert_array_equal(u1[k:k2, k:k2], u)

    # Test CU on several matrix sizes
    cu_aux(2)
    cu_aux(4)
    cu_aux(8)
