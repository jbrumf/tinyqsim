""" Model for quantum circuit.

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
        self.items: list[(str, list[int], list[int], list)] = []  # (name, qubits, args)

    def add_gate(self, name: str, cqubits: list[int], tqubits: list[int], args=None):
        """ Add gate to circuit.
            :param name: Name of gate
            :param cqubits: Control qubits
            :param tqubits: Target qubits
            :param args: Arguments of gate
        """
        if args is None:
            args = []
        self.items.append((name, cqubits, tqubits, args))
