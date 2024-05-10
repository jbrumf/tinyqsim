"""
Simulator for quantum circuit execution.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""
import numpy as np
from numpy import ndarray

from tinyqsim import quantum, gates
from tinyqsim.model import Model
from tinyqsim.quantum import (state_to_tensor, tensor_to_state,
                              unitary_to_tensor, apply_tensor)


class Simulator:
    """Simulator to evolve quantum state of system."""

    def __init__(self, nqubits: int, init='zeros'):
        """Initialize simulator.
        :param nqubits: Number of qubits
        :param init: Initial state: 'zeros' or 'random'
        """
        self._nqubits = nqubits
        self._init = init
        self._state = None  # State tensor
        self._gates = gates.GATES

        # Initialize state
        match init:
            case 'zeros':
                self._state = state_to_tensor(quantum.init_state(self._nqubits))
            case 'random':
                self._state = state_to_tensor(quantum.random_state(self._nqubits))
            case _:
                raise ValueError(f'Invalid init state: {init}')

    @property
    def state(self) -> np.ndarray:
        """Return quantum state as a vector.
        :return: quantum state vector
        """
        return tensor_to_state(self._state)

    @state.setter
    def state(self, state: np.ndarray) -> None:
        """Setter for state vector.
        :param state: State vector
        """
        self._state = state_to_tensor(state)

    def apply(self, u: ndarray, qubits: list[int]) -> None:
        """ Apply a unitary matrix to specified qubits of state.
            :param u: unitary matrix
            :param qubits: qubits
        """
        tu = unitary_to_tensor(u)
        self._state = apply_tensor(self._state, tu, qubits)

    def measure(self, qubits: list[int]):
        """ Measure specified qubits."""
        m, self.state = quantum.measure_qubits(self.state, qubits)
        print(f'Measured qubits{qubits} -> {m}')

    def execute(self, model: Model) -> None:
        """Execute the circuit.
        :param model: Model to execute
        """
        if self._init == 'random':
            self._state = state_to_tensor(quantum.random_state(self._nqubits))
        else:
            self._state = state_to_tensor(quantum.init_state(self._nqubits))

        for (name, qubits, params) in model.items:
            match name:
                case 'U':  # Custom unitary
                    u = params['unitary']
                    self.apply(u, qubits)

                case 'P' | 'CP' | 'RX' | 'RY':  # Parameterized gate
                    u = self._gates[name](params['args'])
                    self.apply(u, qubits)

                case 'measure':  # Measurement
                    self.measure(qubits)

                case 'barrier':  # Barrier
                    pass

                case _:  # Simple non-parameterized gate
                    self.apply(self._gates[name], qubits)
