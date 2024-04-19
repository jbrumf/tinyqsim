"""
Extras for Bloch sphere, random qubits, etc.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import atan2, sin, cos, pi, asin

import numpy as np
import numpy.random as random


def bloch_to_qubit(phi: float, theta: float) -> np.ndarray:
    """Convert Bloch sphere angles to a qubit.
        :param phi: Bloch sphere 'phi' angle in radians
        :param theta: Bloch sphere 'theta' angle in radians
        :return: A qubit
    """
    assert 0 <= phi < 2 * pi
    assert 0 <= theta <= pi
    return np.array([cos(theta / 2),
                     sin(theta / 2) * (cos(phi) + sin(phi) * 1j)])


def qubit_to_bloch(psi: np.ndarray) -> tuple[float, float]:
    """Convert qubit to Bloch sphere angles (phi, theta).
        :param psi: qubit state
        :return: Bloch sphere angles (phi, theta) in radians
    """
    alpha, beta = psi

    theta = 2 * atan2(abs(beta), abs(alpha))
    ab = alpha.conjugate() * beta  # Adjust for global phase
    phi = atan2(ab.imag, ab.real)
    if phi < 0:
        phi += 2 * pi
    return phi, theta


def random_bloch() -> tuple[float, float]:
    """ Return random point on Bloch sphere.
        0 <= theta <= pi,  0 <= phi < 2*pi
        :return: phi, theta (radians)
    """
    phi = random.random() * 2 * pi
    theta = asin(random.random() * 2 - 1) + pi / 2
    return phi, theta


def random_qubit() -> np.ndarray:
    """ Return random qubit (uniformly distributed on Bloch sphere.
        0 <= theta <= pi,  0 <= phi < 2*pi
        :return: A qubit (uniformly distributed on Bloch sphere.)
    """
    return bloch_to_qubit(*random_bloch())
