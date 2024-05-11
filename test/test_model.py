"""
Pytest unit tests for model module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from tinyqsim.model import Model


def test_apply_tensor():
    m = Model(3)
    m.add_gate('X', [0, 1, 2], {'label': 'abc'})
    m.add_gate('Y', [2], {'label': 'def'})
    assert m.items[1] == ('Y', [2], {'label': 'def'})
    assert len(m.items) == 2
