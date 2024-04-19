"""
Pytest unit tests for gate methods of qcircuit module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import pi

from numpy import allclose, kron
from numpy.testing import (assert_array_almost_equal)

from tinyqsim.gates import *
from tinyqsim.qcircuit import QCircuit

# Some useful constants
K0 = np.array([1, 0])  # Ket |0>
K1 = np.array([0, 1])  # Ket |1>

# Test state = P(pi/4) RX(pi/3) |0>
S1 = np.array([sqrt(3) / 2, (1 - 1j) / (2 * sqrt(2))])


def test_s1():
    """Test that tests state corresponds to expected rotations."""
    qc = QCircuit(1)
    qc.rx(pi / 3, 'pi/3', 0)
    qc.p(pi / 4, 'pi/4', 0)
    assert allclose(qc.state_vector, S1)


def test_cct_id():
    """Test identity gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.i(0)
    assert_array_almost_equal(qc.state_vector, S1)


def test_cct_x():
    """Test X gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.x(0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[1], S1[0]])


def test_cct_y():
    """Test Y gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.y(0)
    assert_array_almost_equal(qc.state_vector,
                              [-S1[1].conjugate(), S1[0] * 1j])


def test_cct_z():
    """Test Z gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.z(0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[0], -S1[1]])


def test_pauli_product():
    # Test that -iXYZ = I
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.z(0)
    qc.y(0)
    qc.x(0)
    assert_array_almost_equal(qc.state_vector * -1j, S1)


def test_cct_h():
    """Test Hadamard gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.h(0)
    assert_array_almost_equal(qc.state_vector,
                              1 / sqrt(2) * np.array([[1, 1], [1, -1]]) @ S1)


def tests_cct_s():
    """Test S gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.s(0)
    qc.s(0)
    qc.z(0)
    assert_array_almost_equal(qc.state_vector, S1)


def tests_cct_t():
    """Test T gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.t(0)
    qc.t(0)
    qc.s(0)
    qc.z(0)
    assert_array_almost_equal(qc.state_vector, S1)


def tests_cct_p():
    """Test P gate."""
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.p(0, '0', 0)

    qc = QCircuit(1)
    qc.state_vector = S1
    qc.p(pi / 2, 'pi/2', 0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[0], S1[1].conjugate()])
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.p(pi, 'pi', 0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[0], -S1[1]])

    qc = QCircuit(1)
    qc.state_vector = S1
    qc.p(pi / 2, 'pi/2', 0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[0], S1[1].conjugate()])
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.p(pi / 2, 'pi/2', 0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[0], S1[1].conjugate()])
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.p(pi / 4, 'pi/4', 0)
    assert_array_almost_equal(qc.state_vector, [S1[0], 0.5])


# TODO: Try some more intermediate angles
def test_rx():
    # Note: RX(pi) and X differ by a global phase of 'i'
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.rx(0, '0', 0)
    assert_array_almost_equal(qc.state_vector, S1)

    qc = QCircuit(1)
    qc.state_vector = S1
    qc.rx(pi, 'pi', 0)
    assert_array_almost_equal(qc.state_vector * 1j,
                              [S1[1], S1[0]])


# TODO: Try some more intermediate angles
def test_ry():
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.ry(0, '0', 0)
    assert_array_almost_equal(qc.state_vector, S1)

    qc = QCircuit(1)
    qc.state_vector = S1
    qc.ry(pi, 'pi', 0)
    assert_array_almost_equal(qc.state_vector * 1j,
                              [-S1[1].conjugate(), S1[0] * 1j])


def test_sx():
    qc = QCircuit(1)
    qc.state_vector = S1
    qc.sx(0)
    qc.sx(0)
    assert_array_almost_equal(qc.state_vector,
                              [S1[1], S1[0]])


def test_swap():
    qc = QCircuit(2)
    qc.state_vector = kron(S1, np.array([1, 0]))
    qc.swap(0, 1)
    assert_array_almost_equal(qc.state_vector,
                              kron(np.array([1, 0]), S1))


# Controlled gates

def test_ccx():
    pass


def test_cp():
    pass


def test_cs():
    pass


def test_cswap():
    pass


def test_ct():
    pass


def test_cx():
    pass


def test_cy():
    pass


def test_cz():
    pass


# Custom unitaries

def test_u():
    pass


# def test_cu():
#     assert is_unitary(cu(CX))
#
#     # Test CU on k*k matrix (not unitary for test)
#     def cu_aux(k):
#         k2 = k * k
#         u = np.arange(2, k2 + 2).reshape((k, k))
#         ref = np.array(u)
#         u1 = cu(u)
#         assert_array_equal(u, ref)  # Check 'u' unchanged
#         assert_array_equal(u1[0:k, 0:k], eye(k))
#         assert_array_equal(u1[k:k2, 0:k], zeros((k, k)))
#         assert_array_equal(u1[0:k, k:k2], zeros((k, k)))
#         assert_array_equal(u1[k:k2, k:k2], u)
#
#     # Test CU on several matrix sizes
#     cu_aux(2)
#     cu_aux(4)
#     cu_aux(8)


def test_cu():
    pass


def test_ccu():
    pass
