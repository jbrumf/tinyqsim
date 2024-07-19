"""
Prototype code for LaTeX display in notebooks.

These functions return an IPython Math object that can be displayed in
a Jupyter Notebook using the 'display' function. The display call is
not necessary in the last line of a notebook cell.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
from IPython.display import Math
from numpy import ndarray

from tinyqsim.quantum import components_dict

EPSILON = 1e-12
""" Threshold for ignoring small values """

DEFAULT_DECIMALS = 8
"""Default number of decimal places"""


def latex_array(array: ndarray, decimals: int = DEFAULT_DECIMALS) -> Math:
    """Format 1D or 2D array in LaTeX for display in notebook.
    :param array: 1D or 2D array
    :param decimals: number of decimal places
    :return: IPython Math object representing array
    """
    if len(array.shape) == 1:
        array = [array]

    s = '\\\\'.join(['&'.join([repr(np.round(i, decimals=decimals))
                               for i in j]) for j in array])
    ltx = f'\\begin{{bmatrix}}{s} \\end{{bmatrix}}'
    return Math(ltx)


def latex_dict(dic: dict, prefix: str = '', decimals: int = DEFAULT_DECIMALS,
               include_zeros=False) -> Math:
    """Format state dictionary in LaTeX for display in notebook.
    :param dic: state dictionary
    :param prefix: prefix string
    :param decimals: number of decimal places
    :param include_zeros: whether to include zero values
    :return: IPython Math object representing state dictionary
    """
    items = (rf'{np.round(v, decimals)}\,\ket{{{k}}}'
             for k, v in dic.items() if include_zeros or abs(v) > EPSILON)
    ltx = prefix + ' + '.join(items)
    return Math(ltx)


# This should not go here because it creates a cyclic dependency
def latex_state(state: ndarray, prefix: str = '', decimals: int | None = None,
                include_zeros=False) -> Math:
    """Format quantum state in LaTeX for display in notebook.
    :param state: quantum state
    :param prefix: prefix string
    :param decimals: number of decimal places
    :param include_zeros: whether to include zero values
    :return: IPython Math object representing quantum state
    """
    if not decimals:
        decimals = DEFAULT_DECIMALS
    dic = components_dict(state)
    return latex_dict(dic, prefix=prefix, decimals=decimals, include_zeros=include_zeros)
