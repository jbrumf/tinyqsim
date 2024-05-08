"""
Model for quantum circuit.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""


class Model:
    """ Model for quantum circuit. """

    def __init__(self, nqubits: int):
        """ Initialize circuit model.
            :param nqubits: Number of qubits.
        """
        self.nqubits = nqubits
        self.items: list[(str, list[int], list)] = []

    def add_gate(self, name: str, qubits: list[int], params=None):
        """ Add gate to circuit.
            :param name: Name of gate
            :param qubits: qubits to which gate is applied
            :param params:  parameters
        """
        if params is None:
            params = {}
        self.items.append((name, qubits, params))
