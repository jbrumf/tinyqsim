"""
Pytest unit tests for qutils module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
import pytest
from numpy import kron
from numpy.testing import (assert_equal, assert_array_equal, assert_almost_equal)

from tinyqsim.gates import ID, X, Y, Z, S, T
from tinyqsim.utils import (int_to_bits, bits_to_int, kron_n, kron_all, normalize,
                            is_normalized, is_hermitian, is_unitary, complete,
                            round_complex, is_square_matrix)


def test_int_to_bits():
    assert_array_equal(int_to_bits(0), [0])
    assert_array_equal(int_to_bits(1), [1])
    assert_array_equal(int_to_bits(0, 3), [0, 0, 0])
    assert_array_equal(int_to_bits(6), [1, 1, 0])
    assert_array_equal(int_to_bits(6, 5), [0, 0, 1, 1, 0])
    assert_array_equal(int_to_bits(6, 0), [1, 1, 0])


def test_bits_to_int():
    assert_equal(bits_to_int([]), 0)
    assert_equal(bits_to_int([0]), 0)
    assert_equal(bits_to_int([1]), 1)
    assert_equal(bits_to_int([1, 0, 1, 1, 0, 1]), 45)
    assert_equal(bits_to_int([0, 0, 0, 1, 0, 1]), 5)


def test_round_complex():
    z = 12.3456789 + 0.3141592654j
    assert round_complex(z, 3) == pytest.approx(12.346 + 0.314j, rel=1e-10)
    z = 12.3456789 - 0.3141592654j
    assert round_complex(z, 3) == pytest.approx(12.346 - 0.314j, rel=1e-10)


def test_complete():
    assert_array_equal(complete([0], 0), [0])
    assert_array_equal(complete([0], 1), [0])
    assert_array_equal(complete([0], 3), [0, 1, 2])
    assert_array_equal(complete([2], 0), [2, 0, 1])
    assert_array_equal(complete([2], 5), [2, 0, 1, 3, 4])
    assert_array_equal(complete([4, 2], 0), [4, 2, 0, 1, 3])
    assert_array_equal(complete([4, 2], 6), [4, 2, 0, 1, 3, 5])


def test_normalize():
    v = np.array([3 + 4j, 5 + 6j])
    assert_almost_equal(np.linalg.norm(normalize(v)), 1)


def test_is_normalized():
    assert is_normalized([0, 1])
    assert not is_normalized([0, 0.99])
    assert not is_normalized([0, 1.01])
    assert not is_normalized([0, 1.01], tol=0.009)
    assert is_normalized([0, 1.01], tol=0.011)


def test_is_unitary():
    assert is_unitary(X)
    assert is_unitary(T)
    assert not is_unitary(T * 1.001)


def test_is_hermitian():
    assert is_hermitian(X)
    assert not is_hermitian(T)
    assert not is_hermitian(S)
    assert not is_hermitian(T)


def test_is_square_matrix():
    assert is_square_matrix(np.array([[1, 2], [3, 4]]))
    assert is_square_matrix(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]))
    assert not is_square_matrix(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]))
    assert not is_square_matrix(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]))


def test_kron_n():
    assert_equal(kron_n(1, X), X)
    assert_equal(kron_n(2, X), kron(X, X))
    assert_equal(kron_n(3, ID), kron(ID, kron(ID, ID)))


def test_kron_all():
    assert_equal(kron_all([X]), X)
    assert_equal(kron_all([X, Y, Z]), kron(X, kron(Y, Z)))
