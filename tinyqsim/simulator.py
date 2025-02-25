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
        :param init: Initial state - 'zeros' or 'random'
        """
        self._nqubits = nqubits
        self._init = init
        self._state = None  # State tensor
        self._results = {}  # Measurement results
        self._gates = gates.GATES

        # Initialize state
        match init:
            case 'zeros':
                self._state = state_to_tensor(quantum.zeros_state(self._nqubits))
            case 'random':
                self._state = state_to_tensor(quantum.random_state(self._nqubits))
            case _:
                raise ValueError(f'Invalid init state: {init}')

    @property
    def state_vector(self) -> np.ndarray:
        """Return quantum state as a vector.
        :return: quantum state vector
        """
        return tensor_to_state(self._state)

    @state_vector.setter
    def state_vector(self, state: np.ndarray) -> None:
        """Setter for state vector.
        :param state: State vector
        """
        self._state = state_to_tensor(state)

    def results(self) -> dict[int, int]:
        """Return results of quantum measurements."""
        return self._results

    def apply(self, u: ndarray, qubits: list[int]) -> None:
        """ Apply a unitary matrix to specified qubits of state.
            :param u: unitary matrix
            :param qubits: qubits
        """
        tu = unitary_to_tensor(u)
        self._state = apply_tensor(self._state, tu, qubits)

    def measure(self, qubits: list[int]) -> ndarray:
        """ Measure specified qubits."
            :param qubits: qubits to be measured
            :return: measured values
        """
        m, self.state_vector = quantum.measure_qubits(self.state_vector, qubits)
        for i, q in enumerate(qubits):
            self._results[q] = m[i].item()
        return m

    def reset(self, qubit: int) -> None:
        """ Reset specified qubit."
            :param qubit: qubit to be reset
        """
        # Measure qubit and then apply X if it is |1>
        m, self.state_vector = quantum.measure_qubits(self.state_vector, [qubit])
        if m == 1:
            tu = unitary_to_tensor(self._gates['X'])
            self._state = apply_tensor(self._state, tu, [qubit])

    def execute(self, model: Model, init='zeros') -> None:
        """Initialize the state and execute the circuit.
        The init='none' option skips the initialization.
        :param model: Model to execute
        :param init: Initial state - 'zeros' | 'random' | 'none'
        """
        match init:
            case 'none':
                pass
            case 'zeros':
                self._state = state_to_tensor(quantum.zeros_state(self._nqubits))
            case 'random':
                self._state = state_to_tensor(quantum.random_state(self._nqubits))
            case _:
                raise ValueError(f'Invalid init state: {init}')

        self._results = {}

        for (name, qubits, params) in model.items:
            match name:
                case 'U':  # Custom unitary
                    u = params['unitary']
                    self.apply(u, qubits)

                case 'P' | 'CP' | 'CRX' | 'CRY' | 'CRZ' | 'RX' | 'RY' | 'RZ':  # Parameterized gate
                    u = self._gates[name](params['args'])
                    self.apply(u, qubits)

                case 'measure':  # Measurement
                    self.measure(qubits)

                case 'reset':  # Reset
                    self.reset(qubits[0])

                case 'barrier':  # Barrier
                    pass

                case _:  # Simple non-parameterized gate
                    self.apply(self._gates[name], qubits)
