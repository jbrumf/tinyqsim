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

from tinyqsim.utils import (is_unitary, is_normalized, normalize)

RANGLE = '\u27E9'  # Unicode right bracket for ket


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
    # Create matrix of independent Gaussian random complex variables
    m = random_state(nq * 2).reshape(2 ** nq, 2 ** nq)
    # Orthonormalize using QR factorization
    q, r = np.linalg.qr(m)
    assert is_unitary(q)
    return q


def n_qubits(a: ndarray) -> int:
    """Return the number of qubits of a state or unitary matrix.
       :param a: state or unitary matrix
       :return: number of qubits
    """
    n = len(a)
    return 0 if n == 0 else int.bit_length(n - 1)


def basis_names(nqubits: int, kets: bool = False) -> list[str]:
    """Return list of integers < 2**nqubits as binary strings.
        :param nqubits: number of qubits
        :param kets: forma names as ket symbols
        :return: list of integers as binary strings
    """

    def wrap(s):
        return '|' + s + RANGLE if kets else s

    return [wrap(bin(i)[2:].zfill(nqubits)) for i in range(2 ** nqubits)]


def state_to_tensor(a: ndarray) -> ndarray:
    """Convert state vector to tensor representation.
        :param a: state vector
        :return: tensor representation of state
    """
    nqubits = n_qubits(a)
    return a.reshape([2] * nqubits)


def tensor_to_state(t: ndarray) -> ndarray:
    """Convert tensor representation of state into a state vector.
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


def tensor_to_unitary(t: ndarray) -> ndarray:
    """Convert tensor representation of square matrix (e.g. unitary) to a matrix.
    :param t: tensor representation of matrix
    :return: unitary matrix
    """
    k = 2 ** (len(t.shape) // 2)
    return t.reshape([k, k])


def swap_vector_endianness(v: ndarray) -> ndarray:
    """Swap endianness of state vector.
       :param v: state vector
       :return state vector with reversed endianness
    """
    return tensor_to_state(np.transpose(state_to_tensor(v)))


def swap_unitary_endianness(u: ndarray) -> ndarray:
    """Swap endianness of a square matrix.
       :param u: matrix
       :return: matrix with reversed endianness
    """
    nq = int.bit_length(len(u) - 1)
    tm = unitary_to_tensor(u)

    rng = np.flip(np.arange(nq))
    indices = np.concatenate((rng, rng + nq))
    t = np.einsum(tm, indices)

    return tensor_to_unitary(t)  # Tensor to unitary


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
    b = [i + nq for i in range(len(qubits))]
    fn = dict(zip(qubits, b))
    c = [fn[i] if i in qubits else i for i in a]

    return np.einsum(ts, a, tu, b + qubits, c, optimize=True)


def compose_tensor(tu: ndarray, tg: ndarray, qubits: list[int]) -> ndarray:
    """ Compose gate operator 'tg', applied to specified qubits, with unitary 'tu'.
        The gate operator and unitary are in the form of tensors.
       :param tu: unitary tensor
       :param tg: gate tensor
       :param qubits: list of qubits to wich gate is applied
       :return: resulting unitary tensor
    """
    nq = int.bit_length(tu.size - 1) // 2

    # Tensor subscripts as lists of integers
    inputs = list(range(nq))  # Input indices of 'tu'
    outputs = [i + nq for i in inputs]  # Output indices of 'tu'

    a = inputs + outputs  # tu indices
    b = [q + nq for q in qubits] + [q + 2 * nq for q in qubits]  # tg indices
    c = inputs + [i + nq if i - nq in qubits else i for i in outputs]  # new tu indices

    return np.einsum(tu, a, tg, b, c, optimize=True)


def state_dict(state: ndarray) -> dict:
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
    nq = n_qubits(state)
    if not qubits:
        qubits = range(nq)
    assert 0 <= min(qubits) <= max(qubits) < nq, 'qubit out of range'
    probs = probabilities(state, qubits).tolist()
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
    measured = int(np.random.choice([0, 1], None, p=probs))

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
