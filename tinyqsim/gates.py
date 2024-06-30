"""
Quantum gates

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import sin, cos, sqrt

import numpy as np
from numpy import ndarray

# Useful constants
RT2 = sqrt(2)

# ---------- Basic gates as unitary matrices ----------

# Identity gate
ID = np.array([[1, 0],
               [0, 1]])

# Pauli X gate (aka NOT)
X = np.array([[0, 1],
              [1, 0]])

# Pauli Y gate
Y = np.array([[0, -1j],
              [1j, 0]])

# Pauli Z gate
Z = np.array([[1, 0],
              [0, -1]])

# Hadamard gate
H = np.array([[1, 1],
              [1, -1]]) / RT2

# S gate: S = sqrt(Z)
S = np.array([[1, 0],
              [0, 1j]])  # Phase: S=sqrt(Z)

# Sdg gate: S-dagger
Sdg = np.array([[1, 0],
                [0, -1j]])

# T gate: T = sqrt(S)
T = np.array([[1, 0],
              [0, (1 + 1j) / RT2]])

# Tdg gate: T-dagger
Tdg = np.array([[1, 0],
                [0, (1 - 1j) / RT2]])

# SX gate: sqrt(X)
SX = np.array([[1 + 1j, 1 - 1j],
               [1 - 1j, 1 + 1j]]) / 2  # aka SQRT-NOT

# ---------- Big-endian versions of multi-qubit gates ----------

# SWAP GATE
SWAP = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 1]])


def cu(u: ndarray, n_controls=1) -> ndarray:
    """Return controlled version of U (big endian).
       :param u: Unitary matrix of gate
       :param n_controls: Number of controls
       :return: The controlled-U gate
    """
    n_extra = (2 ** n_controls - 1) * len(u)
    a = np.array(u)
    for i in range(n_extra):
        a = np.insert(a, 0, 0, axis=0)
        a = np.insert(a, 0, 0, axis=1)
        a[0][0] = 1
    return a


# Controlled versions of gates
CH = cu(H)
CX = cu(X)
CY = cu(Y)
CZ = cu(Z)
CS = cu(S)
CT = cu(T)
CCX = cu(CX)
CSWAP = cu(SWAP)


# ---------- Parameterized gates ----------

def P(phi: float) -> ndarray:
    """Phase gate: Rotation by 'phi radians about Z axis.
       :param phi: Phase angle in radians
       :return: the phase gate
    """
    z = np.exp(1j * phi)
    return np.array([[1, 0], [0, z]])


def CP(phi: float) -> ndarray:
    """Controlled phase gate.
       :param phi: Phase angle in radians
       :return: the controlled-phase gate
    """
    return cu(P(phi))


def RX(theta: float) -> ndarray:
    """RX gate: Rotation by 'theta' radians about X axis.
       :param theta: angle in radians
       :return: the gate
    """
    c = cos(theta / 2)
    s = sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]])


def RY(theta: float) -> ndarray:
    """RY gate: Rotation by 'theta' radians about Y axis.
       :param theta: angle in radians
       :return: the gate
    """
    c = cos(theta / 2)
    s = sin(theta / 2)
    return np.array([[c, -s], [s, c]])


""" Dictionary to look-up gates by name."""
GATES = {
    'CCX': CCX,
    'CH': CH,
    'CP': CP,
    'CS': CS,
    'CSWAP': CSWAP,
    'CT': CT,
    'CX': CX,
    'CY': CY,
    'CZ': CZ,
    'H': H,
    'I': ID,
    'P': P,
    'RX': RX,
    'RY': RY,
    'S': S,
    'Sdg': Sdg,
    'SX': SX,
    'SWAP': SWAP,
    'T': T,
    'Tdg': Tdg,
    'X': X,
    'Y': Y,
    'Z': Z,
}
