"""
System tests for tinyqsim.

These tests use the Quantum Fourier Transform and Quantum Phase
Estimation. These exercise much of the functionality of TinyQsim.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import pi

import numpy as np
from numpy.testing import assert_allclose
from pytest import approx

from tinyqsim.qcircuit import QCircuit

PI = '\u03C0'  # PI unicode


def qft(qc, n: int, start: int = 0):
    """ N-qubit QFT starting at qubit index 'start'."""
    for i in range(n):
        j = i + start
        qc.h(j)
        for k in range(1, n - i):
            qc.cp(pi / 2 ** k, f'{PI}/{2 ** k}', j, j + k)
    for i in range(n // 2):  # Reverse order of qubits
        qc.swap(start + i, start + n - i - 1)


def iqft(qc, n: int, start: int = 0):
    """ N-qubit inverse QFT starting at qubit index 'start'."""
    for i in range(n // 2 - 1, -1, -1):  # Reverse order of qubits
        qc.swap(start + i, start + n - i - 1)
    for i in range(n - 1, -1, -1):
        j = i + start
        for k in range(n - i - 1, 0, -1):
            qc.cp(-pi / 2 ** k, f'-{PI}/{2 ** k}', j, j + k)
        qc.h(j)


def qpe(qc, k, phi):
    """ QPE for 1-qubit unitary using k-qubit phase register."""
    radians = 2 * pi * phi
    qc.barrier()
    for q in range(k):
        qc.h(k - q - 1)

    for q in range(k):
        i = k - q - 1
        for j in range(2 ** q):
            qc.cp(radians, 'phi', i, k)
    qc.barrier()
    iqft(qc, k, start=0)


def test_qft():
    """ Test QFT by comparison with numpy inverse FFT."""

    n = 8  # Size of QFT
    qc = QCircuit(n, init='random')
    state = np.array(qc.state_vector)  # Copy of state

    qft(qc, n)
    dft_result = qc.state_vector
    qft_result = np.fft.ifft(state, norm='ortho')
    assert_allclose(qft_result, dft_result)


def test_qft_iqft():
    """Test QFT followed by IQFT gives identity."""
    n = 4  # Size of QFT
    start = 2  # Index of first QFT qubit
    qc = QCircuit(8, init='random')
    initial_state = qc.state_vector
    qft(qc, n, start)
    qc.barrier()
    iqft(qc, n, start)
    # Check that the result is the same as the initial state
    print('Result:', np.allclose(qc.state_vector, initial_state))
    assert_allclose(qc.state_vector, initial_state)


def test_qpe11():
    """ Test using Quantum Phase Estimation."""
    k = 4
    phi = 11 / 2 ** k
    qc = QCircuit(k + 1)
    qc.x(k)
    qpe(qc, k, phi)
    probs = qc.probabilities(range(k))
    assert probs['1011'] == approx(1.0)


def test_qpe_mid():
    """ Test using QPE between resolution steps."""
    k = 4
    phi = 3.5 / 2 ** k
    qc = QCircuit(k + 1)
    qc.x(k)
    qpe(qc, k, phi)
    probs = qc.probabilities(range(k))
    assert probs['0011'] == approx(0.4, abs=0.01)
    assert probs['0100'] == approx(0.4, abs=0.01)
