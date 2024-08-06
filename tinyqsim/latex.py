"""
Prototype code for LaTeX display in notebooks.

These functions return an IPython Math object that can be displayed in
a Jupyter Notebook using the 'display' function. The display call is
not necessary in the last line of a notebook cell.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
from numpy import ndarray

from tinyqsim.quantum import components_dict

EPSILON = 1e-12
""" Threshold for ignoring small values """

DEFAULT_DECIMALS = 8
"""Default number of decimal places"""


def latex_array(array: ndarray, prefix: str = '', decimals: int = DEFAULT_DECIMALS) -> str:
    """Format 1D or 2D array as LaTeX string.
    :param array: 1D or 2D array
    :param prefix: prefix string
    :param decimals: number of decimal places
    :return: LaTeX representation of the array
    """
    if len(array.shape) == 1:
        array = [array]

    s = '\\\\'.join(['&'.join([repr(np.round(i, decimals=decimals))
                               for i in j]) for j in array])
    return f'{prefix}\\begin{{bmatrix}}{s} \\end{{bmatrix}}'


def latex_state(state: ndarray, prefix: str = '', decimals: int | None = None,
                include_zeros=False) -> str:
    """Format quantum state as LaTeX string.
    :param state: quantum state
    :param prefix: prefix string
    :param decimals: number of decimal places
    :param include_zeros: whether to include zero values
    :return: LaTeX representation of the state
    """
    if not decimals:
        decimals = DEFAULT_DECIMALS
    dic = components_dict(state)

    items = (rf'{np.round(v, decimals)}\,\ket{{{k}}}'
             for k, v in dic.items() if include_zeros or abs(v) > EPSILON)
    return prefix + ' + '.join(items)

    # return latex_state(state, prefix=prefix, decimals=decimals, include_zeros=include_zeros)
