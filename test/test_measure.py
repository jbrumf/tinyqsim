"""
Pytest unit tests for quantum module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
import pytest
import scipy
from numpy.testing import assert_array_equal

from test.config import ENABLE_STATS_TESTS
from tinyqsim.quantum import (n_qubits, measure_qubits, measure_qubit)

DEBUG = False  # Enable printing of debug information
NRUNS = 1000  # Number of runs for stats
P_TEST = 0.02  # P-value for testing null hypothesis


# ----- Helper functions for tests -----

def make_measurement(probs: list[float]) -> list[int]:
    """ Create a state and measure the qubits.
        :param probs: Probability for each state
        :return: Measured state (0 or 1) for each qubit
    """
    # Create a state with the given probabilities
    probs = np.array(probs)
    state = np.sqrt(probs / sum(probs))

    # Measure each qubit in turn without collapse
    nqubits = n_qubits(state)
    ones = [0] * nqubits
    for index in range(nqubits):
        meas, state1 = measure_qubit(state, index)
        if meas == 1:
            ones[index] += 1
    return ones


def do_measurement_test(state_probs: list[float], expected: list[float]) -> None:
    """ Perform a test using state vector with the given probabilities.
        :param state_probs: State probabilities
        :param expected: Expected qubit probabilities
    """
    counts = [make_measurement(state_probs) for _ in range(NRUNS)]
    freqs = np.array(counts).T

    for qubit, p_exp in enumerate(expected):
        k = sum(freqs[qubit])
        result = scipy.stats.binomtest(k, NRUNS, p_exp, alternative='two-sided')
        if DEBUG:
            print(f'k={k}, p-value={result.pvalue:.4f}')

        if result.pvalue < P_TEST:
            raise ValueError(f'p-value {result.pvalue:.4f} < {P_TEST}')


def test_measure_eigen1():
    """ Test measure_qubit with simple eigenstate."""

    # Prepare a 3-qubit state vector
    state = np.zeros(8)
    state[4] = 1

    m0, v0 = measure_qubit(state, 0)
    assert m0 == 1
    assert_array_equal(v0, state)

    m0, v0 = measure_qubit(state, 1)
    assert m0 == 0
    assert_array_equal(v0, state)

    m1, v1 = measure_qubit(state, 2)
    assert m1 == 0
    assert_array_equal(v1, state)

    m4, v4 = measure_qubits(state, [0, 1, 2])
    assert_array_equal(m4, [1, 0, 0])


def test_measure_eigen2():
    """ Test measure_qubit with simple eigenstate."""

    # Prepare a 3-qubit state vector
    state = np.zeros(8)
    state[3] = 1

    m0, v0 = measure_qubit(state, 0)
    assert m0 == 0
    assert_array_equal(v0, state)

    m0, v0 = measure_qubit(state, 1)
    assert m0 == 1
    assert_array_equal(v0, state)

    m1, v1 = measure_qubit(state, 2)
    assert m1 == 1
    assert_array_equal(v1, state)

    m4, v4 = measure_qubits(state, [0, 1, 2])
    assert_array_equal(m4, [0, 1, 1])


@pytest.mark.skipif(not ENABLE_STATS_TESTS, reason='Skipping Statistical Test')
def test_measure_qubit_stats_1():
    """ Stochastic test of measurement outcomes for 1 qubit."""
    p = [0.3, 0.7]
    do_measurement_test(p, [p[1]])


@pytest.mark.skipif(not ENABLE_STATS_TESTS, reason='Skipping Statistical Test')
def test_measure_qubit_stats_2():
    """ Stochastic test of measurement outcomes for 2 qubits."""
    p = [0.2, 0.1, 0.4, 0.3]
    do_measurement_test(p, [p[2] + p[3], p[1] + p[3]])


@pytest.mark.skipif(not ENABLE_STATS_TESTS, reason='Skipping Statistical Test')
def test_measure_qubit_stats_3():
    """ Check that test detects a probability error of 0.1."""
    p = [0.2, 0.1, 0.4, 0.3]
    with pytest.raises(ValueError):
        do_measurement_test(p, [p[2] + p[3], p[1] + p[3] + 0.1])


@pytest.mark.skipif(not ENABLE_STATS_TESTS, reason='Skipping Statistical Test')
def test_measure_qubit_stats_4():
    """ Check that test detects a probability error of -0.1."""
    p = [0.2, 0.1, 0.4, 0.3]
    with pytest.raises(ValueError):
        do_measurement_test(p, [p[2] + p[3], p[1] + p[3] - 0.1])
