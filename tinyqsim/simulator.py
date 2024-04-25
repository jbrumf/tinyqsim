"""
Simulator for quantum circuit execution.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""
import numpy as np
from numpy import ndarray

from tinyqsim import quantum, gates
from tinyqsim.model import Model


class Simulator:
    """Simulator to evolve quantum state of system."""

    def __init__(self, nqubits: int, init='zeros'):
        """Initialize simulator.
        :param nqubits: Number of qubits
        :param init: Initial state: 'zeros' or 'random'
        """
        self._nqubits = nqubits
        self._init = init
        self._state = None
        self._gates = gates.GATES

        # Initialize state
        match init:
            case 'zeros':
                self._state = quantum.init_state(self._nqubits)
            case 'random':
                self._state = quantum.random_state(self._nqubits)
            case _:
                raise ValueError(f'Invalid init state: {init}')

    @property
    def state(self) -> np.ndarray:
        """Return quantum state.
        :return: quantum state
        """
        return self._state

    @state.setter
    def state(self, state: np.ndarray) -> None:
        """Setter for state vector.
        :param state: State vector
        """
        self._state = state

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

        self._state = quantum.map_qubits(u, self._nqubits, all_qubits) @ self._state

    def execute(self, model: Model) -> None:
        """Execute the circuit.
        :param model: Model to execute
        """
        if self._init == 'random':
            self._state = quantum.random_state(self._nqubits)
        else:
            self._state = quantum.init_state(self._nqubits)

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
                    m, self._state = quantum.measure_qubits(self._state, all_qubits)
                    print(f'm = {m}')

                case 'barrier':  # Barrier
                    pass

                case _:  # Simple non-parameterized gate
                    self.apply(self._gates[name], cqubits, tqubits)
