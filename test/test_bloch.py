"""
Pytest unit tests for extras module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from cmath import exp as cexp
from math import sqrt, pi

import numpy as np
import numpy.random as random
from numpy.linalg import norm
from numpy.testing import (assert_array_almost_equal)
from pytest import approx

from tinyqsim.bloch import (bloch_to_qubit, qubit_to_bloch,
                            random_bloch, random_qubit)

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


def test_random_bloch():
    """ Test random_bloch, just for valid range."""
    nruns = 100
    low_phi = 1e10
    high_phi = -1e10
    low_theta = 1e10
    high_theta = -1e10
    for _ in range(nruns):
        phi, theta = random_bloch()
        low_phi = min(phi, low_phi)
        high_phi = max(phi, high_phi)
        low_theta = min(theta, low_theta)
        high_theta = max(theta, high_theta)
    assert 0 <= low_phi <= pi
    assert pi <= high_phi <= 2 * pi
    assert 0 <= low_theta <= pi / 2
    assert pi / 2 <= high_theta <= 2 * pi


def test_random_qubit():
    """ Test random_qubit for valid norm."""
    nruns = 100
    for _ in range(nruns):
        assert norm(random_qubit()) == approx(1.0, abs=1e-10)


def test_random_bloch_qubit_bloch():
    """Test random bloch -> qubit -> bloch."""
    nruns = 100
    for _ in range(nruns):
        psi = random_qubit()
        phi, theta = qubit_to_bloch(psi)
        psi = bloch_to_qubit(phi, theta)
        phase = random.random() * 2 * pi
        psi = psi * cexp(1j * phase)  # Introduce global phase
        phi1, theta1 = qubit_to_bloch(psi)
        assert_array_almost_equal(phi, phi1, decimal=13)
        assert_array_almost_equal(theta, theta1, decimal=13)
