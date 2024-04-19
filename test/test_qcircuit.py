"""
Pytest unit tests for qcircuit module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import pi, sqrt

from numpy.testing import (assert_equal, assert_almost_equal,
                           assert_array_almost_equal)

from tinyqsim.qcircuit import QCircuit

RT2I = 1 / sqrt(2)
RT3I = 1 / sqrt(3)


# FIXME: Test cases to be added:
#  def test_apply(self):
#  def test_measure(self):
#  def test_probabilities(self):

# ----- Test gates -----

# The gates are tested in the test_gates module.
# This is just to check the wrappers in QCircuit.

def test__gate():
    qc = QCircuit(1)
    qc.i(0)
    assert_equal(qc.state_vector, [1, 0])

    qc = QCircuit(1)
    qc.x(0)
    qc.i(0)
    assert_equal(qc.state_vector, [0, 1])


def test_x_gate():
    qc = QCircuit(2)
    assert_equal(qc.state_vector, [1, 0, 0, 0])
    qc.x(1)
    assert_equal(qc.state_vector, [0, 1, 0, 0])
    qc.x(0)
    assert_equal(qc.state_vector, [0, 0, 0, 1])
    qc.x(1)
    assert_equal(qc.state_vector, [0, 0, 1, 0])


def test_y_gate():
    qc = QCircuit(2)
    qc.x(1)
    qc.y(1)
    assert_almost_equal(qc.state_vector, [-1j, 0, 0, 0])


def test_z_gate():
    qc = QCircuit(2)
    qc.x(1)
    qc.z(1)
    assert_equal(qc.state_vector, [0, -1, 0, 0])


def test_h_gate():
    qc = QCircuit(1)
    qc.h(0)
    assert_almost_equal(qc.state_vector, [RT2I, RT2I])

    qc = QCircuit(1)
    qc.x(0)
    qc.h(0)
    assert_almost_equal(qc.state_vector, [RT2I, -RT2I])


def test_s_gate():
    qc = QCircuit(1)
    qc.s(0)
    assert_equal(qc.state_vector, [1, 0])

    qc = QCircuit(1)
    qc.x(0)
    qc.s(0)
    assert_equal(qc.state_vector, [0, 1j])


def test_t_gate():  # pi/8
    qc = QCircuit(1)
    qc.t(0)
    assert_equal(qc.state_vector, [1, 0])

    qc = QCircuit(1)
    qc.x(0)
    qc.t(0)
    assert_equal(qc.state_vector, [0, (1 + 1j) * RT2I])


def test_p_gate():
    qc = QCircuit(1)
    qc.p(pi / 4, 'pi/4', 0)
    assert_equal(qc.state_vector, [1, 0])

    qc = QCircuit(1)
    qc.x(0)
    qc.p(pi / 4, 'pi/4', 0)
    assert_array_almost_equal(qc.state_vector, [0, (1 + 1j) * RT2I])


def test_sqrtx_gate():
    qc = QCircuit(1)
    qc.sx(0)
    qc.sx(0)
    assert_equal(qc.state_vector, [0, 1])


def test_cx_gate():
    qc = QCircuit(2)
    qc.cx(0, 1)
    assert_equal(qc.state_vector, [1, 0, 0, 0])  # |00>->|00>


def test_cp_gate():
    qc = QCircuit(2)
    qc.x(1)
    qc.p(pi / 4, 'pi/4', 0)
    assert_array_almost_equal(qc.state_vector, [0, 1, 0, 0])

    qc = QCircuit(2)
    qc.x(0)
    qc.x(1)
    qc.p(pi / 4, 'pi/4', 0)
    assert_array_almost_equal(qc.state_vector, [0, 0, 0, (1 + 1j) * RT2I])


def test_swap_gate():
    qc = QCircuit(2)
    qc.x(0)
    qc.swap(0, 1)
    assert_equal(qc.state_vector, [0, 1, 0, 0])
    qc.swap(0, 1)
    assert_equal(qc.state_vector, [0, 0, 1, 0])
