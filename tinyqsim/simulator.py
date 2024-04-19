"""
Simulator for quantum circuit execution.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from numpy import ndarray

from tinyqsim import quantum, gates
from tinyqsim.model import Model


class Simulator:
    """Simulator to evolve quantum state of system."""

    def __init__(self, nqubits: int, init='zeros'):
        self._nqubits = nqubits
        self._init = init
        self.state = None
        self._gates = gates.GATES

        # Initialize state
        match init:
            case 'zeros':
                self.state = quantum.init_state(self._nqubits)
            case 'random':
                self.state = quantum.random_state(self._nqubits)
            case _:
                raise ValueError(f'Invalid init state: {init}')

    def apply(self, u: ndarray, cqubits: list[int], tqubits: list[int]) -> None:
        """ Apply a unitary matrix to specified qubits of state.
            :param u: unitary matrix
            :param cqubits: list of control qubits
            :param tqubits: list of target qubits
        """
        all_qubits = cqubits + tqubits
        if min(all_qubits) < 0 or max(all_qubits) >= self._nqubits:
            raise ValueError(f'Qubit indices out of range: {all_qubits}')
        if 2 ** len(all_qubits) != len(u):
            raise ValueError(f'Wrong number of qubit indices, expected {quantum.n_qubits(u)}')

        self.state = quantum.map_qubits(u, self._nqubits, all_qubits) @ self.state

    def execute(self, model: Model) -> None:
        """Execute the circuit."""
        if self._init == 'random':
            self.state = quantum.random_state(self._nqubits)
        else:
            self.state = quantum.init_state(self._nqubits)

        for (name, cqubits, tqubits, args) in model.items:
            all_qubits = cqubits + tqubits
            match name:
                case 'U':  # Custom unitary
                    u = args[1]
                    self.apply(u, cqubits, tqubits)

                case 'P' | 'CP' | 'RX' | 'RY':  # Parameterized gate
                    u = self._gates[name](args[0])
                    self.apply(u, cqubits, tqubits)

                case 'measure':  # Measurement
                    m, self.state = quantum.measure_qubits(self.state, all_qubits)
                    print(f'm = {m}')

                case 'barrier':  # Barrier
                    pass

                case _:  # Simple non-parameterized gate
                    self.apply(self._gates[name], cqubits, tqubits)
