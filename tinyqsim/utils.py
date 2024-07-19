"""
Miscellaneous utility functions.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
from numpy import kron, ndarray
from numpy.linalg import norm


# --------------- General utility functions ---------------

def int_to_bits(n: int, nbits=0) -> list[int]:
    """Return integer 'n' as list of bits left-padded with zeros to width 'nbits'.
       'nbits' has no effect if it is smaller than the minimum required."""
    return [int(i) for i in bin(n)[2:].zfill(nbits)]


def bits_to_int(bitlist: list[int]) -> int:
    """Convert list of bits (0 or 1) to an integer."""
    value = 0
    for bit in bitlist:
        value = (value << 1) | (bit & 1)
    return value


def round_complex(z, decimals: int = 3) -> complex:
    """Round a complex number.
       :param z: The complex number
       :param decimals: Number or decimal places
       :return: The rounded result
    """
    return complex(round(z.real, decimals), round(z.imag, decimals))


def complete(perm: list[int], n: int) -> list[int]:
    """Complete a permutation, by appending missing integers in range(n)."""
    n1 = max(n, max(perm))
    pad = [item for item in range(n1) if item not in perm]
    return perm + pad


# --------------- Utilities for vectors and matrices ---------------

def normalize(psi: ndarray) -> ndarray:
    """Normalize a complex vector"""
    return psi / norm(psi)


def is_normalized(psi, tol: float = 1E-14) -> bool:
    """Test whether a vector is normalized to given tolerance."""
    n = norm(psi)
    return abs(n - 1) <= tol


def is_unitary(m: ndarray) -> bool:
    """Test whether a matrix is unitary"""
    return np.allclose(np.eye(m.shape[0]), m.conj().T @ m)


def is_hermitian(m: ndarray) -> bool:
    """Test whether a matrix is Hermitian"""
    return np.allclose(m.conj().T, m)


def kron_n(n: int, u: ndarray) -> ndarray:
    """Return tensor product of 'n' instances of 'u' """
    assert n > 0, 'kron-n requires n>0'
    product = u
    for i in range(1, n):
        product = kron(u, product)
    return product


def kron_all(xs: list[ndarray]) -> ndarray:
    """Return tensor product of a list of vectors or matrices.
       e.g. kron_all([H,H,H])"""
    assert len(xs) > 0, 'kron-all requires at least one item'
    p = xs[0]
    for i in range(1, len(xs)):
        p = kron(p, xs[i])
    return p
