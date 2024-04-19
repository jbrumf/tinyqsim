"""
Functions for qubits and quantum states.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
import numpy.random as random
from numpy import ndarray, kron, eye, einsum
from numpy.linalg import norm

from tinyqsim.utils import (is_normalized, normalize, complete, round_complex)

ATOL = 1E-14  # Tolerance for normalization


def init_state(n: int) -> ndarray:
    """Initialize an N-qubit state to all |0>.
       :param n: number of qubits
       :return: the initialized state vector
    """
    assert n > 0
    state = np.zeros(2 ** n, dtype='int')
    state[0] = 1
    return state


def n_qubits(a: ndarray) -> int:
    """Return the number of qubits of a state or unitary matrix.
       The argument should be a power of two.
       :param a: state or unitary matrix
       :return: number of qubits
    """
    n = len(a)
    return 0 if n == 0 else int.bit_length(n - 1)


def map_qubits(u: ndarray, nqubits, indices: list[int]) -> ndarray:
    """Return unitary matrix expanded to nqubits with mapped indices.
       :param u: unitary matrix
       :param nqubits: number of qubits in expanded matrix
       :param indices: qubit indices to be mapped onto in state
       :return: unitary matrix expanded to nqubits
    """
    assert n_qubits(u) == len(indices)
    perm = complete(indices, nqubits)
    nextra = nqubits - n_qubits(u)
    if nextra > 0:
        u = kron(u, eye(2 ** nextra))
    return permute_qubits(u, perm)


def permute_qubits(u: ndarray, perm: list[int]) -> ndarray:
    """Permute the unitary 'u' into qubit order 'perm'.
       Qubit indices [0,1,2,...] are mapped onto the indices in 'perm'.
       :param u: Unitary matrix of the gate
       :param perm: qubit indices that [0,1,2,...] map to
       :return: permuted matrix
    """
    nqubits = n_qubits(u)
    assert len(perm) == nqubits
    nq2 = 2 ** nqubits
    u = u.reshape([2] * (2 * nqubits))
    indices = perm + [i + nqubits for i in perm]
    return einsum(u, indices).reshape([nq2, nq2])


def swap_endian(u: ndarray) -> np.ndarray:
    """Swap the qubit-endianness of unitary matrix 'u'.
       :param: u: The unitary matrix to swap
       :return: Swapped unitary matrix
    """
    nqubits = n_qubits(u)
    lower = list(reversed(range(nqubits)))
    return permute_qubits(u, lower)


def qft(state: ndarray, inverse=False) -> ndarray:
    """Quantum FourierTransform (QFT).
       :param state: state vector
       :param inverse: inverse of QFT
       :return: the QFT of the state
    """
    if inverse:
        return np.fft.ifft(state, norm='ortho')
    else:
        return np.fft.fft(state, norm='ortho')


def random_state(nqubits: int) -> np.ndarray:
    """Return a random pure state vector.
       :param nqubits: number of qubits
       :return: random quantum state vector
    """
    n = 2 ** nqubits
    gen = random.default_rng()

    while True:
        v = gen.normal(size=(2, n))
        z = v[0] + 1j * v[1]  # Random complex
        n = norm(z)
        if n > 1e-9:  # Repeat if norm is zero
            break
    return z / n


# ------------------- Measurement of qubits states ------------------

def measure_qubit(state: ndarray, index: int = 0, endian: str = 'big') -> tuple[int, ndarray]:
    """Measure a single qubit of a state vector with collapse.
        :param state: State vector
        :param index: Index of qubit
        :param endian: Endianness ('big' or 'little')
        :return: (measured, new_state) where 'measured' is the measured value
    """
    assert is_normalized(state, ATOL)
    n = len(state)
    nqubits = int.bit_length(n - 1)
    if endian == 'big':
        index = nqubits - index - 1

    # Sum the probabilities of all states that have the required index bit
    prob = 0
    for i in range(n):
        if (i >> index) & 1 == 1:  # State contributes to probability
            a = norm(state[i])
            prob += a * a  # Probability using Born rule
    measured = np.random.choice([0, 1], None, p=[1 - prob, prob])

    # Create the new state
    new_state = np.zeros(n, dtype=np.cdouble)
    for i in range(n):
        if measured == (i >> index) & 1:  # bit=1 if state contributes
            new_state[i] = state[i]
    return measured, normalize(new_state)


def measure_qubits(state: ndarray, indices: [int], endian: str = 'big') \
        -> tuple[ndarray, ndarray]:
    """Measure a list of qubits with collapse.
    :param state: Initial state vector
    :param indices: List of qubit indices
    :param endian: Endianness ('big' or 'little')
    :return: (bits, new_state) where bits is list of measured values
    """
    bits = np.zeros(len(indices), dtype=int)
    for i in range(len(indices)):
        bits[i], state = measure_qubit(state, indices[i], endian)
    return bits, state


# ------------------- Inspection of quantum state --------------------

def counts(state: ndarray, nruns: int = 100, include_zeros: bool = False) \
        -> dict[str, int]:
    """ Return measurement counts for repeated experiment.
        The state is not changed (collapsed).
        :param state: State vector
        :param nruns: Number of test runs (default=1000)
        :param include_zeros: True to include zero values (default=False)
        :return: Dictionary of counts for each state
    """
    nstates = len(state)
    probs = state.real ** 2 + state.imag ** 2
    freqs = [0] * nstates
    for i in range(nruns):
        n = np.random.choice(nstates, None, p=probs)
        freqs[n] += 1

    dic = {}
    for i, a in enumerate(state):
        nqubits = n_qubits(state)
        bits = bin(i)[2:]
        key = '0' * (nqubits - len(bits)) + bits
        value = freqs[i]
        if include_zeros or value > 0:
            dic[key] = value
    return dic


def components(state: ndarray, decimals: int = 5, include_zeros: bool = False) \
        -> dict:
    """Return complex components of the state vector.
       :param state: State vector
       :param decimals: Number of decimal places
       :param include_zeros: True to include zero values (default=False)
       :return: Dictionary of state components
    """
    dic = {}
    for i, a in enumerate(state):
        nqubits = n_qubits(state)
        bits = bin(i)[2:]
        key = '0' * (nqubits - len(bits)) + bits
        value = round_complex(state[i], decimals)
        if include_zeros or not value == 0:
            dic[key] = value
    return dic


def probabilities(state: ndarray, decimals: int = 5, include_zeros: bool = False) \
        -> dict[str, float]:
    """ Return map of the probabilities of each outcome.
        :param state: State vector
        :param decimals: number of decimal places (default=5)
        :param include_zeros: True to include zero values (default=False)
        :return: dictionary of outcome->probability
    """
    nqubits = n_qubits(state)
    dic = {}
    for i, a in enumerate(state):
        key = bin(i)[2:].zfill(nqubits)
        value = round(norm(a) ** 2, decimals)
        if include_zeros or value > 0:
            dic[key] = value
    return dic
