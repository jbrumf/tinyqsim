"""
Formatting of results for printing or display.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
from numpy import ndarray

from tinyqsim import quantum

DEFAULT_DECIMALS = 4
"""Default number of decimal places"""

RANGLE = '\u27E9'  # Unicode right bracket for ket


# --------- Low-level formatting of numbers ----------

def format_float(x, decimals: int, trim: bool) -> str:
    """Format a float value.
    :param x: float value
    :param decimals: number of decimal places
    :param trim: trim trailing fractional zeros
    :return: formatted string
    """
    s = f'{x:.{decimals}f}'
    if trim and len(s) > 1:
        s = s.rstrip('0').rstrip('.')
    return s


def format_complex(z, decimals: int = 5, trim: bool = False) -> tuple[str, bool]:
    """Format a complex number.\n
    This is specifically intended for use in ket strings.
    Values with both real and imag parts that don't round to zero are enclosed
    parentheses. The sign is returned separately and not included in the value string unless it is in parentheses.

    :param z: complex number
    :param decimals: number of decimal digits
    :param trim: trim trailing fractional zeros
    :return: formatted string
    """
    re = z.real
    im = z.imag
    tol = 10 ** (-decimals) / 2
    zr = bool(abs(re) >= tol)  # True if real part non-negligible
    zi = bool(abs(im) >= tol)  # True if imag part non-negligible

    neg = False
    match (zr, zi):
        case (True, True):
            sign = '-' if im < 0 else '+'
            s = '(' + format_float(re, decimals, trim) + sign + format_float(abs(im), decimals, trim) + 'j)'

        case (False, True):
            s = format_float(abs(im), decimals, trim) + 'j'
            neg = bool(im < 0)

        case (True, False):
            s = format_float(abs(re), decimals, trim)
            neg = bool(re < 0)

        case (False, False):
            s = format_float(0, decimals, trim)

        case _:
            raise ValueError(f'Unknown case {(zr, zi)}')

    return s, neg  # Formatted string and sign (True=negative)


def ket(index: int, nqubits=0, kets=True):
    """Format a state-vector index as a ket string.
    :param index: state vector index
    :param nqubits: number of qubits
    :param kets: whether to format as kets (default)
    :return: formatted string
    """

    def wrap(s):
        return '|' + s + RANGLE if kets else s

    return wrap(bin(index)[2:].zfill(nqubits))


def format_table(values, decimals=5, include_zeros=False, trim=True, edge=5):
    """Format a table of kets and the corresponding values.
    :param values: array of values (e.g. state vector)
    :param decimals: number of decimal places
    :param include_zeros: whether to include zeros
    :param trim: trim trailing fractional zeros
    :param edge: Number of items before and after ellipsis
    :return: table as formatted string
    """

    n = len(values)
    if edge == 0:
        edge = n

    sig = 10 ** (-decimals) / 2
    nqubits = int.bit_length(n - 1)

    def format_row(ii, vv):
        if include_zeros or abs(vv) >= sig:
            ss, neg = format_complex(vv, decimals=decimals, trim=trim)
            return f'{ket(ii, nqubits, True)} {' -'[neg]}{ss}'
        else:
            return None

    def scan(rng):
        # Return list of formatted items satisfying option
        items = []
        count = 0
        last_index = 0
        for i in rng:
            last_index = i
            s = format_row(i, values[i])
            if s:
                items.append(s)
                count += 1
                if count >= edge:
                    break
        return last_index, items

    # Process up to 'edge' items from start and end of list
    ipre, pre = scan(range(n))
    ipost, post = scan(range(n - 1, ipre, -1))

    # Combine the lists, with an ellipsis if needed
    sep = ['...'] if ipost > ipre + 1 else []
    return '\n'.join(pre + sep + list(reversed(post)))


# ---------- Formatting quantum states ----------

def _ket(label: str, latex: bool):
    """Format ket as ASCII or LaTeX string.
    :param label: int
    :param latex: str
    :return: formatted string
    """
    if latex:
        return '\\ \\ket{' + label + '}'
    else:
        return '|' + label + RANGLE


def state_kets(state: ndarray, prefix: str = '', decimals: int = DEFAULT_DECIMALS,
               include_zeros=False, trim=True, latex=False) -> str:
    """Format state as ket string in ASCII or LaTeX.
    :param state: state vector
    :param prefix: prefix string or latex string
    :param decimals: number of decimal places
    :param include_zeros: include values that round to zero
    :param trim: trim trailing fractional zeros
    :param latex: return as latex source string
    :return: formatted string
    """
    # The LaTeX mode works for up to about 10 qubits, but it is
    # really only useful for a small number of qubits (say up to 4).

    dic = quantum.state_dict(state)
    ltx = prefix
    first = True
    for k, v in dic.items():
        zs, neg = format_complex(v, decimals=decimals, trim=trim)
        zero = zs == '0' or zs.rstrip('0').strip('.') == '0'
        if not include_zeros and zero:
            continue
        op = '' if first and not neg else '+-'[neg] + ' '
        if not first:
            ltx += ' '  # No space before first item
        ltx += op + zs + _ket(k, latex)
        first = False
    return ltx


# This is just a wrapper to call state_kets with mode='latex'
def latex_state(state: ndarray, prefix: str = '', decimals: int = DEFAULT_DECIMALS,
                include_zeros: bool = False, trim: bool = True) -> str:
    """Format quantum state as LaTeX string.
    :param state: quantum state
    :param prefix: prefix string
    :param decimals: number of decimal places
    :param include_zeros: whether to include zero values
    :param trim: trim trailing fractional zeros
    :return: LaTeX representation of the state
    """
    return state_kets(state, prefix=prefix, decimals=decimals, include_zeros=include_zeros,
                      trim=trim, latex=True)


# ---------- Formatting arrays in LaTeX ----------

def latex_array(array: ndarray, prefix: str = '', decimals: int = DEFAULT_DECIMALS) -> str:
    """Format 1D or 2D array as LaTeX string.
    :param array: 1D or 2D array
    :param prefix: prefix string
    :param decimals: number of decimal places
    :return: LaTeX representation of the array
    """
    # FIXME: Legaacy mode for Numpy 2 compatibility
    with np.printoptions(legacy="1.25"):  # type: ignore
        if len(array.shape) == 1:
            array = [array]

        s = '\\\\'.join(['&'.join([repr(np.round(i, decimals=decimals))
                                   for i in j]) for j in array])
        return f'{prefix}\\begin{{bmatrix}}{s} \\end{{bmatrix}}'
