"""
Pytest unit tests for extras module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import sqrt, pi

import numpy as np
from numpy.testing import (assert_array_almost_equal)

from tinyqsim.bloch import (bloch_to_qubit, qubit_to_bloch)

DECIMAL = 15  # Require precision (decimal places)
ENABLE_STATS_TESTS = True  # Enable stochastic tests that may occasionally fail

# Useful constants
RT2 = sqrt(2)
RT2I = 1 / RT2

KET0 = np.array([1, 0])  # Ket: |0>
KET1 = np.array([0, 1])  # Ket: |1>
KETP = np.array([RT2I, RT2I])  # Ket: |+>
KETM = np.array([RT2I, -RT2I])  # Ket: |->
KETR = np.array([RT2I, 1j * RT2I])  # Ket: |R>
KETL = np.array([RT2I, -1j * RT2I])  # Ket: |L>


# Note: array_almost_equal() works on complex arrays.

def test_bloch_to_qubit():
    """ Test bloch_to_qubit."""
    assert_array_almost_equal(bloch_to_qubit(phi=0, theta=0),
                              KET0, decimal=DECIMAL)
    assert_array_almost_equal(bloch_to_qubit(phi=0, theta=pi),
                              KET1, decimal=DECIMAL)
    assert_array_almost_equal(bloch_to_qubit(phi=0, theta=pi / 2),
                              KETP, decimal=DECIMAL)
    assert_array_almost_equal(bloch_to_qubit(phi=pi, theta=pi / 2),
                              KETM, decimal=DECIMAL)
    assert_array_almost_equal(bloch_to_qubit(phi=pi / 2, theta=pi / 2),
                              KETR, decimal=DECIMAL)
    assert_array_almost_equal(bloch_to_qubit(phi=3 * pi / 2, theta=pi / 2),
                              KETL, decimal=DECIMAL)


def test_qubit_to_bloch():
    """ Test qubit_to_bloch."""
    assert_array_almost_equal(qubit_to_bloch(KET0),
                              (0, 0), decimal=DECIMAL)
    assert_array_almost_equal(qubit_to_bloch(KET1),
                              (0, pi), decimal=DECIMAL)
    assert_array_almost_equal(qubit_to_bloch(KETP),
                              (0, pi / 2), decimal=DECIMAL)
    assert_array_almost_equal(qubit_to_bloch(KETM),
                              (pi, pi / 2), decimal=DECIMAL)
    assert_array_almost_equal(qubit_to_bloch(KETR),
                              (pi / 2, pi / 2), decimal=DECIMAL)
    assert_array_almost_equal(qubit_to_bloch(KETL),
                              (3 * pi / 2, pi / 2), decimal=DECIMAL)
