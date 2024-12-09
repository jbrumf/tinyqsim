"""
Pytest unit tests for qcircuit module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import pi, sqrt

import numpy as np
import pytest
from numpy.linalg import norm
from numpy.testing import (assert_equal, assert_almost_equal,
                           assert_array_almost_equal)
from pytest import approx

from tinyqsim.qcircuit import QCircuit

RT2I = 1 / sqrt(2)
RT3I = 1 / sqrt(3)


def test_qcircuit():
    """ Test constructor."""
    qc1 = QCircuit(2)
    assert np.allclose(qc1.state_vector, np.array([1, 0, 0, 0]))


def test_state_vector():
    """ Test state_vector property."""
    nqubits = 2
    qc = QCircuit(nqubits)
    qc.state_vector = np.array([0, 1, 0, 0])
    assert np.allclose(qc.state_vector, np.array([0, 1, 0, 0]))


def test_random():
    s1 = QCircuit(2, init='random').state_vector
    s2 = QCircuit(2, init='random').state_vector

    assert not np.allclose(s1, s2)
    assert norm(s1) == approx(1)


def test_nqubits():
    qc = QCircuit(3)
    assert qc.n_qubits == 3


def test_basis_names():
    qc = QCircuit(3)
    bases = qc.basis_names()
    assert bases == ['000', '001', '010', '011', '100', '101', '110', '111']


def test_check_qubits():
    qc = QCircuit(3)
    qc._check_qubits([0])
    qc._check_qubits([0, 2, 1])
    with pytest.raises(ValueError):
        qc._check_qubits([3])
    with pytest.raises(ValueError):
        qc._check_qubits([-1])


def test_format_state():
    qc = QCircuit(3)
    qc.x(1)
    qc.h(2)
    c1 = qc.format_state(mode='table', decimals=5)
    exp = '|010⟩  0.70711\n|011⟩  0.70711'
    assert_equal(c1, exp)

    # Test 'include_zeros' option
    qc = QCircuit(2)
    qc.x(1)
    c2 = qc.format_state(mode='table', include_zeros=True)
    exp = '|00⟩  0\n|01⟩  1\n|10⟩  0\n|11⟩  0'
    assert_equal(c2, exp)


def test_counts():
    # Tested on eigenstates so that result is reproduceable
    qc = QCircuit(3)
    qc.x(1)
    c1 = qc.counts()
    assert_equal(c1, {'010': 1000})

    c2 = qc.counts(0, 1)
    assert_equal(c2, {'01': 1000})

    qc = QCircuit(2)
    qc.x(1)
    c3 = qc.counts(runs=100, include_zeros=True)
    assert_equal(c3, {'00': 0, '01': 100, '10': 0, '11': 0})


def test_format_probabilities():
    qc = QCircuit(2)
    qc.h(0)
    qc.p(pi / 4, 'phi', 0)
    qc.h(0)
    qc.cx(0, 1)
    s = qc.format_probabilities(0, 1, decimals=4)
    exp = '|00⟩  0.8536\n|11⟩  0.1464'
    assert_equal(s, exp)


def test_probability_dict():
    qc = QCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    p1 = qc.probability_dict(0, 1)
    assert p1 == pytest.approx({'00': 0.5, '01': 0, '10': 0, '11': 0.5})


def test_probability_array():
    qc = QCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    probs = qc.probability_array(0, 1)
    assert_almost_equal(probs, [0.5, 0, 0, 0.5])


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
