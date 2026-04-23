"""Library of utility functions for the Jupyter Notebook examples.
  Some of these are developed in one notebook and then imported
  from this library for use in subsequent notebooks.
"""

from tinyqsim.qcircuit import QCircuit
from tinyqsim.utils import int_to_bits
import numpy as np
from numpy import pi

U_PI = '\u03C0'  # PI unicode


def qft(qc, n: int|None = None, start: int = 0):
    """ Quantum Fourier Transform (QFT).
    :param qc: QCircuit instance
    :param n: number of qubits
    :param start: start index
    """
    if not n:
        n = qc.n_qubits
    for i in range(n):
        j = i + start
        qc.h(j)
        for k in range(1, n - i):
            qc.cp(pi / 2 ** k, f'{U_PI}/{2 ** k}', j + k, j)
    for i in range(n // 2):  # Reverse order of qubits
        qc.swap(start + i, start + n - i - 1)


def iqft(qc, n: int|None = None, start: int = 0):
    """ Inverse Quantum Fourier Transform (IQFT).
    :param qc: QCircuit instance
    :param n: number of qubits
    :param start: start index
    """
    if not n:
        n = qc.n_qubits
    for i in range(n // 2 - 1, -1, -1):  # Reverse order of qubits
        qc.swap(start + i, start + n - i - 1)
    for i in range(n - 1, -1, -1):
        j = i + start
        for k in range(n - i - 1, 0, -1):
            qc.cp(-pi / 2 ** k, f'-{U_PI}/{2 ** k}', j + k, j)
        qc.h(j)


def create_qpe_circuit(unitary, nqc, nqt, eigenvec=1, pre_iqft=None):
    """Create Quantum Phase Estimation (QPE) circuit, excluding measurement.
    :param unitary: function returning the unitary matrix
    :param nqc: Number of control qubits
    :param nqt: Number of target qubits
    :param eigenvec: e.g. 3 for |0011> when nqt=4 (default=1)
    :param pre_iqft: Function called just before IQFT
    :return: QPE circuit with 'nqc' control qubits and 'nqt' target qubits."""

    # Registers
    regC = range(nqc)  # Control register
    regT = range(nqc, nqc + nqt)  # Target register

    # Qubit labels
    labels = [f'C{i}' for i in range(nqc)] + [f'T{i}' for i in range(nqt)]
    label_dict = dict(zip(range(nqc + nqt), labels))

    # Create the circuit
    qc = QCircuit(nqc + nqt)
    qc.qubit_labels(label_dict, numbers=False)

    # Initialialize registers
    x = int_to_bits(eigenvec, nqt)
    qc.x([regT[i] for i, s in enumerate(x) if s == 1])
    qc.h(regC)
    qc.barrier('1')

    # Apply unitary operators
    for i, j in enumerate(reversed(regC)):
        u = unitary(2 ** i)
        qc.cu(u, f'$U^{{{2 ** i}}}$', j, *regT)
    qc.barrier('2')

    # Call function to examine state just before the IQFT
    if pre_iqft is not None:
        pre_iqft(qc, nqc)

    # Inverse QFT
    iqft(qc, nqc)
    return qc


def continued_fraction(fraction):
    """Return continued fraction in list notation."""
    a, b = fraction.numerator, fraction.denominator
    print(f'Fraction = {a}/{b}')
    terms = []
    while b:
        q = a // b
        terms.append(q)
        a, b = b, a - b * q
    return terms


def convergents(cf):
    """Return generator for the convergents of a continued fraction.
    :param cf: continued fraction
    return: generator for the convergents of 'cf'.
    """
    p0, q0 = 1, 0
    p1, q1 = cf[0], 1
    yield (p1, q1)
    for a in cf[1:]:
        p2 = a * p1 + p0
        q2 = a * q1 + q0
        yield (p2, q2)
        p0, q0 = p1, q1
        p1, q1 = p2, q2


def print_probs(qc, qubits, min_prob: float = None, max_total: float = None):
    """Print state probabilities which are above threshold, in descending order.
    :param qc: quantum circuit
    :param qubits: list of qubits
    :param min_prob: minimum probability for item
    :param max_total: maximum total probability
    """
    probs = qc.probability_array(*qubits)
    y = np.argsort(probs)[::-1]  # Descending order
    total = 0
    for i in y:
        p = probs[i]
        total += p
        if min_prob and p < min_prob:
            break
        if max_total and total > max_total:
            break
        print(f'{i}: {probs[i]:.4f}')
    # print(f'total = {total:.4f}')