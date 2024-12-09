"""
Pytest unit tests for format module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
from numpy.testing import (assert_equal)

from tinyqsim.format import format_float, format_complex, state_kets, latex_array

RANGLE = '\u27E9'  # Unicode right angle-bracket


def ket(s):
    return '|' + s + RANGLE


def test_format_float_positive():
    """Test formatting positive float value."""

    x = 1.23456
    # Test that decimal point is trimmed
    s = format_float(x, 0, False)
    assert_equal(s, '1')

    # Test with a single decimal place
    s = format_float(x, 1, False)
    assert_equal(s, '1.2')

    # Test with a 3 decimal places
    s = format_float(x, 3, False)
    assert_equal(s, '1.235')

    # Tes with more decimal places than precision of value
    s = format_float(x, 10, False)
    assert_equal(s, '1.2345600000')

    # Test trimming of trailing fractional zeros
    s = format_float(x, 10, True)
    assert_equal(s, '1.23456')


def test_format_float():
    """Test formatting zero float value."""

    s = format_float(0, 2, True)
    assert_equal(s, '0')

    s = format_float(0, 2, False)
    assert_equal(s, '0.00')

    s = format_float(0, 0, True)
    assert_equal(s, '0')

    s = format_float(0, 0, False)
    assert_equal(s, '0')


def test_format_complex1():
    # Test with real and imaginary both positive.
    z = 1.2 + 3.4j
    s, neg = format_complex(z, 5)
    assert s == '(1.20000+3.40000j)'
    assert not neg

    # T est with negative real, positive imaginary.
    z = -1.2 + 3.4j
    s, neg = format_complex(z, 5)
    assert s == '(-1.20000+3.40000j)'
    assert not neg

    # Test with positive real, negative imaginary.
    z = (1.2 - 3.4j)
    s, neg = format_complex(z, 5)
    assert s == '(1.20000-3.40000j)'
    assert not neg

    # Test with real and imaginary both negative.
    z = -1.2 - 3.4j
    s, neg = format_complex(z, 5)
    assert s == '(-1.20000-3.40000j)'
    assert not neg

    # Test with positive real, zero imaginary.
    z = 1.2
    s, neg = format_complex(z, 5)
    assert s == '1.20000'
    assert not neg

    # Test with negative real, zero imaginary.
    z = -1.2
    s, neg = format_complex(z, 5)
    assert s == '1.20000'
    assert neg

    # Test with zero real, positive imaginary.
    z = 3.4j
    s, neg = format_complex(z, 5)
    assert s == '3.40000j'
    assert not neg

    # Test with negative real, positive imaginary.
    z = -3.4j
    s, neg = format_complex(z, 5)
    assert s == '3.40000j'
    assert neg

    # Test with real and imaginary both zero.
    z = 0 + 0j
    s, neg = format_complex(z, 5)
    assert s == '0.00000'
    assert not neg

    s, neg = format_complex(z, 0)
    assert s == '0'
    assert not neg


def test_format_complex_nodecimals():
    # Test with zero decimal places.                               """
    z = 1.2 + 3.4j
    s, neg = format_complex(z, 0)
    assert s == '(1+3j)'
    assert not neg

    # Test with 3 decimal places trim=False
    z = 1. + 3.j
    s, neg = format_complex(z, 3, trim=False)
    assert s == '(1.000+3.000j)'
    assert not neg

    # Test with 3 decimal places trim=True
    z = 1. + 3.j
    s, neg = format_complex(z, 3, trim=True)
    assert s == '(1+3j)'
    assert not neg


def test_state_kets_simple():
    # Note: Unicode RANGLE of ket is replaced by '>' for easier string comparison.
    # Note: 'state_kets' does not require the state to be normalized.

    psi = np.array([1.2, 3.4j])
    s = state_kets(psi, latex=False)
    s = s.replace(RANGLE, '>')
    assert s == '1.2|0> + 3.4j|1>'

    psi = np.array([1.2, 3.4j])
    s = state_kets(psi, latex=True)
    s = s.replace(RANGLE, '>')
    assert s == '1.2\\ \\ket{0} + 3.4j\\ \\ket{1}'

    psi = np.array([1.2, 3.4j])
    s = state_kets(psi, latex=False, decimals=3, trim=True)
    s = s.replace(RANGLE, '>')
    assert s == '1.2|0> + 3.4j|1>'

    psi = np.array([1.2, 3.4j])
    s = state_kets(psi, latex=False, decimals=3, trim=False)
    s = s.replace(RANGLE, '>')
    assert s == '1.200|0> + 3.400j|1>'

    psi = np.array([1.0, 3.0j])
    s = state_kets(psi, latex=False, decimals=3, trim=True)
    s = s.replace(RANGLE, '>')
    assert s == '1|0> + 3j|1>'

    psi = np.array([1.0, 3.0j])
    s = state_kets(psi, latex=False, decimals=3, trim=False)
    s = s.replace(RANGLE, '>')
    assert s == '1.000|0> + 3.000j|1>'


def test_state_kets_nolatex():
    """Test state_kets with latex=False and no prefix"""

    # Note: Unicode RANGLE of ket is replaced by '>' f sor easier string comparison.
    # This example exercises all the sign variants.
    psi = np.array([1.1, 2.2j, 3.3 + 4.4j, -5.5, -6.6j, -(7.7 + 8.8j), 0, -0])

    # latex=False, decimals=3, include_zeros=False, trim=False, prefix='psi = '
    s = state_kets(psi, latex=False, decimals=3, include_zeros=False, trim=False, prefix='psi = ')
    s = s.replace(RANGLE, '>')
    assert s == ('psi = 1.100|000> + 2.200j|001> + (3.300+4.400j)|010> - 5.500|011>'
                 ' - 6.600j|100> + (-7.700-8.800j)|101>')

    # latex=False, decimals=3, include_zeros=True, trim=False, prefix='psi = '
    s = state_kets(psi, latex=False, decimals=3, include_zeros=True, trim=False, prefix='psi = ')
    s = s.replace(RANGLE, '>')
    assert s == ('psi = 1.100|000> + 2.200j|001> + (3.300+4.400j)|010> - 5.500|011>'
                 ' - 6.600j|100> + (-7.700-8.800j)|101> + 0.000|110> + 0.000|111>')

    # latex=False, decimals=3, include_zeros=True, trim=True, prefix='psi = '
    s = state_kets(psi, latex=False, decimals=3, include_zeros=True, trim=True, prefix='psi = ')
    s = s.replace(RANGLE, '>')
    assert s == ('psi = 1.1|000> + 2.2j|001> + (3.3+4.4j)|010> - 5.5|011>'
                 ' - 6.6j|100> + (-7.7-8.8j)|101> + 0|110> + 0|111>')

    # latex=False, decimals=3, include_zeros=False, trim=True, prefix='psi = '
    s = state_kets(psi, latex=False, decimals=3, include_zeros=False, trim=True, prefix='psi = ')
    s = s.replace(RANGLE, '>')
    assert s == ('psi = 1.1|000> + 2.2j|001> + (3.3+4.4j)|010> - 5.5|011>'
                 ' - 6.6j|100> + (-7.7-8.8j)|101>')


def test_state_kets_nodecimals():
    """Test state_kets with decimals=False."""
    psi = np.array([1.1, 2.2j, 3.3 + 4.4j, -5.5, -6.6j, -(7.7 + 8.8j), 0, -0])

    # latex=False, decimals=0, include_zeros=True, trim=True, prefix='psi = '
    s = state_kets(psi, latex=False, decimals=0, include_zeros=True, trim=True, prefix='psi = ')
    s = s.replace(RANGLE, '>')
    assert s == ('psi = 1|000> + 2j|001> + (3+4j)|010> - 6|011>'
                 ' - 7j|100> + (-8-9j)|101> + 0|110> + 0|111>')


def test_state_kets_prefix():
    """ Test state_kets with prefix."""

    psi = np.array([1.2, 3.4j])

    # Test prefix on ket string.
    s = state_kets(psi, latex=False, prefix='psi = ')
    s = s.replace(RANGLE, '>')
    assert s == 'psi = 1.2|0> + 3.4j|1>'

    # Test LaTeX prefix on LaTeX ket string.
    s = state_kets(psi, latex=True, prefix=r'\ket{\psi}=\ ')
    s = s.replace(RANGLE, '>')
    assert s == r'\ket{\psi}=\ 1.2\ \ket{0} + 3.4j\ \ket{1}'


def test_latex_array():
    """Test 1D latex_array."""
    a = np.array([1.2, 3.4])
    ltx = latex_array(a)
    assert ltx == '\\begin{bmatrix}1.2&3.4 \\end{bmatrix}'

    """Test 2D latex_array."""
    a = np.array([[1.2, 3.4], [5.6, 7.8]])
    ltx = latex_array(a)
    assert ltx == '\\begin{bmatrix}1.2&3.4\\\\5.6&7.8 \\end{bmatrix}'
