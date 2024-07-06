"""
Functions for working with qubits and quantum states.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from typing import Iterable

import numpy as np
import numpy.random as random
from numpy import ndarray
from numpy.linalg import norm

from tinyqsim.utils import (is_normalized, normalize)


def zeros_state(nqubits: int) -> ndarray:
    """Return a quantum state initialized to |000...0>.
       :param nqubits: number of qubits
       :return: the initialized state vector
    """
    assert nqubits > 0
    state = np.zeros(2 ** nqubits, dtype='int')
    state[0] = 1
    return state


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
        if n > 1e-9:  # Try again if norm is zero
            break
    return z / n


def random_unitary(nq: int):
    """Return a random unitary matrix.
    :param nq: number of qubits
    """
    while True:
        # Create matrix of independent Gaussian random complex variables
        m = random_state(nq * 2).reshape(2 ** nq, 2 ** nq)
        if abs(np.linalg.det(m)) > 1E-6:  # Check non-singular
            break
    # Orthonormalize using QR factorization
    q, r = np.linalg.qr(m)
    return q


def n_qubits(a: ndarray) -> int:
    """Return the number of qubits of a state or unitary matrix.
       :param a: state or unitary matrix
       :return: number of qubits
    """
    n = len(a)
    return 0 if n == 0 else int.bit_length(n - 1)


def basis_names(nqubits: int) -> list[str]:
    """Return list of integers < 2**nqubits as binary strings.
        :param nqubits: number of qubits
        :return: list of integers as binary strings
    """
    return [bin(i)[2:].zfill(nqubits) for i in range(2 ** nqubits)]


def state_to_tensor(a: ndarray) -> ndarray:
    """Convert state vector to tensor representation.
        :param a: state vector
        :return: tensor representation of state
    """
    nqubits = n_qubits(a)
    return a.reshape([2] * nqubits)


def tensor_to_state(t: ndarray) -> ndarray:
    """Convert tensor into a state vector.
        :param t: tensor representation of state
        :return: state vector
    """
    k = len(t.shape)
    return t.reshape(2 ** k)


def unitary_to_tensor(u: ndarray):
    """Convert unitary matrix to tensor representation.
        :param u: unitary matrix
        :return: tensor representation of unitary
    """
    nqu = int.bit_length(len(u) - 1)
    return u.reshape([2] * nqu * 2)


def apply_tensor(ts: ndarray, tu: ndarray, qubits: list[int]) -> ndarray:
    """ Apply tensor of unitary to specified qubits of state tensor.
        :param ts: state tensor
        :param tu: tensor of unitary
        :param qubits: list of qubits
        :return: updated state tensor
    """
    nq = int.bit_length(ts.size - 1)

    # Tensor subscripts as lists of integers
    a = range(nq)
    b = [q + nq for q in qubits] + qubits
    c = [i + nq if i in qubits else i for i in a]

    return np.einsum(ts, a, tu, b, c, optimize=True)


def components_dict(state: ndarray) -> dict:
    """Return components of the state vector as a dictionary.
       :param state: State vector
       :return: Dictionary of state components
    """
    keys = basis_names(n_qubits(state))
    return dict(zip(keys, state))


def probabilities(state: ndarray, qubits: Iterable[int]) -> ndarray:
    """ Return the probability of each measurement outcome.
        :param state: State vector
        :param qubits: List of qubit indices
        :return: list of probabilities
    """
    nq = n_qubits(state)
    assert 0 <= min(qubits) <= max(qubits) < nq, 'qubit out of range'

    probs = np.absolute(state) ** 2
    return tensor_to_state(np.einsum(state_to_tensor(probs),
                                     range(nq), list(qubits)))


def probability_dict(state: ndarray, qubits: Iterable[int] | None = 0) \
        -> dict[str, float]:
    """ Return dictionary of the probabilities of measurement outcomes.
        :param state: State vector
        :param qubits: List of qubits
        :return: dictionary of outcome->probability
    """
    if not qubits:
        qubits = range(n_qubits(state))
    probs = probabilities(state, qubits)
    return dict(zip(basis_names(len(qubits)), probs))


def counts_dict(state: ndarray, qubits: list[int], runs: int = 1000) -> dict[str, int]:
    """ Return measurement counts for repeated experiment.
        The state is not changed (collapsed).
        :param state: State vector
        :param qubits: List of qubits
        :param runs: Number of test runs (default=1000)
        :return: Dictionary of counts for each state
    """
    dic = probability_dict(state, qubits)
    probs = list(dic.values())
    n = len(probs)
    freqs = [0] * n
    for i in range(runs):
        k = np.random.choice(n, None, p=probs)
        freqs[k] += 1
    return dict(zip(dic.keys(), freqs))


# ------------------- Measurement of qubits states ------------------

def measure_qubit(state: ndarray, qubit: int) -> tuple[int, ndarray]:
    """Measure a single qubit of a state vector with collapse.
    :param state: State vector
    :param qubit: Qubit to be measured
    :return: (measured, new_state) where 'measured' is the measured value
    """
    # Choose a state according to probabilities
    assert is_normalized(state), f'norm={norm(state)}'
    probs = probabilities(state, [qubit])
    measured = np.random.choice([0, 1], None, p=probs)

    # Create the new state
    n = len(state)
    index = n_qubits(state) - qubit - 1  # Convert qubit index to little-endian
    mask = np.arange(n) & (1 << index) == (measured << index)
    return measured, normalize(np.where(mask, state, np.zeros(n)))


def measure_qubits(state: ndarray, qubits: [int]) -> tuple[ndarray, ndarray]:
    """Measure a list of qubits with collapse.
    :param state: State vector
    :param qubits: Qubits to be measured
    :return: (bits, new_state) where bits is list of measured values
    """
    bits = np.zeros(len(qubits), dtype=int)
    for i in range(len(qubits)):
        bits[i], state = measure_qubit(state, qubits[i])
    return bits, state
