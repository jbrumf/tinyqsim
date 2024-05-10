"""
Quantum Circuit.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import isclose
from typing import Iterable

import numpy as np
from numpy import ndarray
from numpy.linalg import norm

import tinyqsim
from tinyqsim import gates, quantum, utils, plotting
from tinyqsim.model import Model
from tinyqsim.schematic import Schematic
from tinyqsim.simulator import Simulator
from tinyqsim.utils import round_complex

EPS = 1e-12  # Threshold for ignoring small valUes


class QCircuit(object):
    """ Class representing a quantum circuit.

        QCircuit ties together all the components of a quantum simulation
        and presents them as a quantum circuit with methods to add gates
        and perform measurements.
    """
    version = tinyqsim.__version__

    def __init__(self, nqubits: int, init='zeros', auto_exec=True) -> None:
        """Initialize QCircuit.
           :param: nqubits: number of qubits
           :param: init: initialization 'zeros' or 'random'
           :param: auto_exec: Enable on-the-fly execution
        """
        self._nqubits = nqubits
        self._init = init
        self._auto_exec = auto_exec
        self._model = Model(nqubits)
        self._schematic = Schematic(nqubits)
        self._simulator = Simulator(nqubits, init)
        self._gates = gates.GATES

    # -------------------------- Properties --------------------------

    @property
    def state_vector(self) -> np.ndarray:
        """Return copy of the quantum state vector.
           :return: copy of quantum state vector
        """
        return self._simulator.state

    @state_vector.setter
    def state_vector(self, state: ndarray) -> None:
        """Setter for state_vector.
            :param state: state vector
        """
        if not isclose(norm(state), 1.0):
            raise ValueError(f'State vector must be normalised: {norm(state)}')
        if not len(state) == 2 ** self._nqubits:
            raise ValueError(f'State vector should have length {2 ** self._nqubits}')

        self._simulator.state = state

    @property
    def n_qubits(self) -> int:
        """Return the number of qubits.
           :return: number of qbits
        """
        return self.n_qubits

    # ----------------- Add components to the model -----------------

    def check_qubits(self, qubits):
        """ Validate qubit indices.
            :param qubits: list of qubits
        """
        if min(qubits) < 0 or max(qubits) >= self._nqubits:
            raise ValueError(f'Qubit indices out of range: {qubits}')

    def _add_gate(self, name: str, qubits: list[int], params: dict = None) -> None:
        """ Add a gate to the model.
            :param name: name of the gate
            :param qubits: qubits
            :param params: parameter dictionary
        """
        self.check_qubits(qubits)
        self._model.add_gate(name, qubits, params)
        if self._auto_exec:
            self._simulator.apply(self._gates[name], qubits)

    def _add_param_gate(self, name: str, qubits: list[int], params: dict) -> None:
        """ Add a parameterized gate to the model.
            :param name: name of the gate
            :param qubits: Qubits
            :param params: Parameter dictionary
        """
        self.check_qubits(qubits)
        self._model.add_gate(name, qubits, params)
        if self._auto_exec:
            u = self._gates[name](params['args'])
            self._simulator.apply(u, qubits)

    def _add_measure(self, qubits: list[int]) -> None:
        """ Add a measurement to the model.
            :param qubits: list of qubits
        """
        self._model.add_gate('measure', qubits)
        if self._auto_exec:
            self._simulator.measure(qubits)

    def _add_unitary(self, name: str, u: ndarray, qubits: list[int], params: dict) -> None:
        """ Add a unitary matrix to the model.
            :param name: name of the gate
            :param u: unitary matrix
            :param qubits: qubits
            :param params: Parameter dictionary
        """
        self.check_qubits(qubits)
        if 2 ** len(qubits) != len(u):
            raise ValueError(f'Wrong number of qubit indices, expected {quantum.n_qubits(u)}')

        params['label'] = name
        params['unitary'] = u
        self._model.add_gate('U', qubits, params)
        if self._auto_exec:
            if not utils.is_unitary(u):
                raise ValueError('Matrix must be unitary')
            self._simulator.apply(u, qubits)

    # ----------------- Execution of quantum circuit ----------------

    def _execute(self) -> None:
        """Execute the circuit."""
        self._simulator.execute(self._model)

    # -------------- Obtain information about the state -------------

    def components(self, decimals: int = 5, include_zeros: bool = False) -> dict:
        """Return complex components of state vector as a dictionary.
           :param decimals: number of decimal places (default=5)
           :param include_zeros: True to include zero values (default=False)
           :return: Dictionary of state components
        """
        comp = quantum.components_dict(self._simulator.state)
        return {k: round_complex(v, decimals) for k, v in comp.items() if include_zeros or v > EPS}

    def counts(self, qubits: list[int] = None, runs: int = 1000, include_zeros: bool = False) -> dict[str, int]:
        """ Return measurement counts for repeated experiment.
            The state is not changed (collapsed).
                        :param qubits: list of qubits
            :param runs: Number of test runs (default=1000)
            :param include_zeros: True to include zero values (default=False)
            :return: frequencies of outcomes as a dictionary
        """
        counts = quantum.counts_dict(self._simulator.state, qubits, runs)
        return {k: v for k, v in counts.items() if include_zeros or v > EPS}

    def probabilities(self, qubits: Iterable[int] = None, decimals: int = 5,
                      include_zeros: bool = False) -> dict[str, float]:
        """ Return dictionary of the probabilities of each outcome.
            :param qubits: list of qubits
            :param decimals: number of decimal places (default=5)
            :param include_zeros: True to include zero values (default=False)
            :return: dictionary of outcome->probability
        """
        if not qubits:
            qubits = range(self._nqubits)
        probs = quantum.probability_dict(self._simulator.state, qubits)
        return {k: round(v, decimals) for k, v in probs.items() if include_zeros or v > EPS}

    # ------------------ Measurement ------------------

    def measure(self, qubits: Iterable[int] = None) -> None:
        """Add a measurement gate to one or more qubits.
            :param qubits: list of qubits
        """
        if not qubits:
            qubits = range(self._nqubits)
        self._add_measure(list(qubits))

    # -------------------------- Graphics ---------------------------

    def draw(self, scale: float = 1, show: bool = True, save: str | None = None) -> None:
        """Draw the quantum circuit.
            :param: scale: scale factor (default=1)
            :param: show: show the quantum circuit
            :param: save: file to save image if required
        """
        self._schematic.draw(self._model, scale=scale, show=show, save=save)

    def plot_probabilities(self, qubits: Iterable[int] = None, save: str | None = False) -> None:
        """Plot histogram of probabilities for list of qubits.
            :param qubits: list of qubits (None => all)
            :param save: file to save image if required
        """
        if not qubits:
            qubits = range(self._nqubits)
        probs = quantum.probability_dict(self._simulator.state, qubits)
        plotting.plot_histogram(probs, save=save, ylabel='Probability')

    def plot_counts(self, qubits: list[int] = None, runs: int = 1000, save: str | None = False) -> None:
        """Plot histogram of measurement counts.
        :param qubits: list of qubits
        :param runs: number of test runs (default=1000)
        :param save: file to save image if required
        """
        freq = quantum.counts_dict(self._simulator.state, qubits, runs=runs)
        plotting.plot_histogram(freq, save=save, ylabel='Counts')

    # ------------------ Wrapper methods for gates ------------------

    # In the following, 'c' stands for control and 't' for target.

    def ccu(self, u: ndarray, name: str, *qubits) -> None:
        """Add a controlled-controlled-U (CCU) gate.
        :param name: name of the gate
        :param u: unitary matrix
        :param qubits: list of qubits
        """
        qs = list(qubits)
        cu = gates.cu
        self._add_unitary(name, cu(cu(u)), qs, {'controls': 2})

    def ccx(self, c1: int, c2: int, t: int) -> None:
        """Add a controlled-controlled-X (CCX) gate.
        :param c1: control qubit
        :param c2: target qubit
        :param t: target qubit
        """
        self._add_gate('CCX', [c1, c2, t], {'controls': 2})

    def cp(self, phi: float, phi_text: str, c: int, t: int) -> None:
        """Add a controlled-phase (CP) gate.
        :param phi: phase angle
        :param phi_text: text of phase angle
        :param c: control qubit
        :param t: target qubit
        """
        self._add_param_gate('CP', [c, t],
                             {'args': phi, 'label': phi_text, 'controls': 1})

    def cs(self, c: int, t: int) -> None:
        """ Add a controlled-S (CS) gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CS', [c, t], {'controls': 1})

    def cswap(self, c: int, t1: int, t2: int) -> None:
        """ Add a controlled-swap (CSWAP) gate.
        :param c: control qubit
        :param t1: target qubit
        :param t2: target qubit
        """
        self._add_gate('CSWAP', [c, t1, t2], {'controls': 1})

    def ct(self, c: int, t: int) -> None:
        """ Add a controlled-T (CT) gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CT', [c, t], {'controls': 1})

    def cu(self, u: ndarray, name: str, *qubits) -> None:
        """Add a controlled-U (CU) gate.
        :param u: unitary matrix
        :param name: name of the gate
        :param qubits: list of qubits
        """
        qs = list(qubits)
        self._add_unitary(name, gates.cu(u), qs, {'controls': 1})

    def cx(self, c: int, t: int) -> None:
        """Add a controlled-X (CX) gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CX', [c, t], {'controls': 1})

    def cy(self, c: int, t: int) -> None:
        """Add a controlled-Y (CY) gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CY', [c, t], {'controls': 1})

    def cz(self, c: int, t: int) -> None:
        """Add a controlled-Z (CZ) gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CZ', [c, t], {'controls': 1})

    def h(self, t: int) -> None:
        """Add a Hadamard (H) gate.
        :param t: target qubit
        """
        self._add_gate('H', [t])

    def i(self, t: int) -> None:
        """Add an identity (I) gate.
        :param t: target qubit
        """
        self._add_gate('I', [t])

    def p(self, phi: float, phi_text: str, t: int) -> None:
        """Add a phase (P) gate.
        :param phi: phase angle
        :param phi_text: text value of phase angle
        :param t: target qubit
        """
        self._add_param_gate('P', [t], {'args': phi, 'label': phi_text})

    def rx(self, theta: float, theta_text: str, t: int) -> None:
        """Add an RX gate.
        :param theta: target qubit
        :param theta_text: text value of phase angle
        :param t: target qubit
        """
        self._add_param_gate('RX', [t], {'args': theta, 'label': theta_text})

    def ry(self, theta: float, theta_text: str, t: int) -> None:
        """Add an RY gate.
        :param theta: target qubit
        :param theta_text: text value of phase angle
        :param t: target qubit
        """
        self._add_param_gate('RY', [t], {'args': theta, 'label': theta_text})

    def s(self, t: int) -> None:
        """Add an S gate.
        :param t: target qubit
        """
        self._add_gate('S', [t])

    def swap(self, t1: int, t2: int) -> None:
        """Add a swap (SWAP) gate.
        :param t1: target qubit
        :param t2: target qubit
        """
        self._add_gate('SWAP', [t1, t2])

    def sx(self, t: int) -> None:
        """Add a sqrt(X) gate.
        :param t: target qubit
        """
        self._add_gate('SX', [t])

    def t(self, t: int) -> None:
        """Add a T gate.
        :param t: target qubit
        """
        self._add_gate('T', [t])

    def u(self, u: ndarray, name: str, *qubits):
        """Add a custom unitary gate (U).
        :param u: unitary matrix
        :param name: name of the gate
        :param qubits: list of qubits
        """
        self._add_unitary(name, u, list(qubits), {})

    def x(self, t: int) -> None:
        """Add an X gate.
        :param t: target qubit
        """
        self._add_gate('X', [t])

    def y(self, t: int) -> None:
        """Add a Y gate.
        :param t: target qubit
        """
        self._add_gate('Y', [t])

    def z(self, t: int) -> None:
        """Add a Z gate.
        :param t: target qubit
        """
        self._add_gate('Z', [t])

    def barrier(self) -> None:
        """Add a barrier to the circuit."""
        self._model.add_gate('barrier', [0, self._nqubits - 1])
