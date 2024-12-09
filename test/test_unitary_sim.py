"""
Pytest unit tests for unitary_sim module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""
from math import pi

from numpy.ma.testutils import assert_allclose

from tinyqsim.qcircuit import QCircuit
from utils import is_unitary

PI = '\u03C0'  # PI unicode


# QFT as a test circuit
def qft(qc, n: int, start: int = 0):
    """ N-qubit QFT starting at qubit index 'start'."""
    for i in range(n):
        j = i + start
        qc.h(j)
        for k in range(1, n - i):
            qc.cp(pi / 2 ** k, f'{PI}/{2 ** k}', j, j + k)
    for i in range(n // 2):  # Reverse order of qubits
        qc.swap(start + i, start + n - i - 1)


# Quantum circuit for the test
def circuit(qc, nq):
    qc.h(0)
    qc.cx(0, 1)
    qc.p(pi / 7, 'pi/7', 0)  # Non-Hermitian
    qft(qc, nq)


def test_to_unitary():
    nqubits = 5

    # Derive unitary matrix from circuit 'simple'
    qc = QCircuit(nqubits)
    circuit(qc, nqubits)
    u = qc.to_unitary()
    assert is_unitary(u)

    # Run the circuit normally with a random initial state
    qc1 = QCircuit(nqubits, init='random')
    sv_rand = qc1.state_vector.copy()
    circuit(qc1, nqubits)
    sv1 = qc1.state_vector

    # Run the unitary as a custom gate on the same random input
    qc2 = QCircuit(nqubits)
    qc2.state_vector = sv_rand
    qc2.u(u, 'U', *range(nqubits))
    sv2 = qc2.state_vector

    # Compare the 2 results
    assert_allclose(sv2, sv1)
