"""
Quantum Circuit.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import isclose

import numpy as np
from numpy import ndarray
from numpy.linalg import norm

import tinyqsim
from tinyqsim import gates, quantum, utils
from tinyqsim.model import Model
from tinyqsim.schematic import Schematic
from tinyqsim.simulator import Simulator


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

    def add_gate(self, name: str, cqubits: list[int], tqubits: list[int]) -> None:
        """ Add a gate to the model.
            :param name: name of the gate
            :param cqubits: control qubits
            :param tqubits: target qubits
        """
        self._model.add_gate(name, cqubits, tqubits)
        if self._auto_exec:
            self._simulator.apply(self._gates[name], cqubits, tqubits)

    def add_param_gate(self, name: str, cqubits: list[int], tqubits: list[int], args: list) -> None:
        """ Add a parameterized gate to the model.
            :param name: name of the gate
            :param cqubits: control qubits
            :param tqubits: target qubits
            :param args: list of arguments
        """
        self._model.add_gate(name, cqubits, tqubits, args)
        if self._auto_exec:
            u = self._gates[name](args[0])
            self._simulator.apply(u, cqubits, tqubits)

    def add_measure(self, qubits: list[int]) -> None:
        """ Add a measurement to the model.
            :param qubits: list of qubits
        """
        self._model.add_gate('measure', [], qubits)
        m = None
        if self._auto_exec:
            m, self._simulator.state = quantum.measure_qubits(self._simulator.state, qubits)
        return m

    def add_unitary(self, name: str, u: ndarray, cqubits: list[int], tqubits: list[int]) -> None:
        """ Add a unitary matrix to the model.
            :param name: name of the gate
            :param u: unitary matrix
            :param cqubits: control qubits
            :param tqubits: target qubits
        """
        self._model.add_gate('U', cqubits, tqubits, [name, u])
        if self._auto_exec:
            if not utils.is_unitary(u):
                raise ValueError('Matrix must be unitary')
            self._simulator.apply(u, cqubits, tqubits)

    # ----------------- Execution of quantum circuit ----------------

    def execute(self) -> None:
        """Execute the circuit."""
        self._simulator.execute(self._model)

    # -------------------------- Graphics ---------------------------

    def draw(self, scale: float = 1, show=True, save: str = None) -> None:
        """Draw the quantum circuit.
            :param: scale: scale factor (default=1)
            :param: show: show the quantum circuit
            :param: save: file to save image if required
        """
        self._schematic.draw(self._model, scale=scale, show=show, save=save)

    # -------------- Obtain information about the state -------------

    # Real-time: Does not go in a circuit
    def counts(self, nruns: int = 1000, include_zeros: bool = False) -> dict[str, int]:
        """ Return measurement counts for repeated experiment.
            The state is not changed (collapsed).
            :param nruns: Number of test runs (default=1000)
            :param include_zeros: True to include zero values (default=False)
            :return: frequencies of outcomes as a dictionary
        """
        return quantum.counts(self._simulator.state, nruns, include_zeros)

    # Real-time: Does not go in a circuit
    def components(self, decimals: int = 5, include_zeros: bool = False) -> dict:
        """Return complex components of state vector as a dictionary.
           :param decimals: number of decimal places (default=5)
           :param include_zeros: True to include zero values (default=False)
           :return: Dictionary of state components
        """
        return quantum.components(self._simulator.state, decimals=decimals, include_zeros=include_zeros)

    # Real-time: Does not go in a circuit
    def probabilities(self, decimals: int = 5, include_zeros: bool = False) \
            -> dict[str, float]:
        """ Return map of the probabilities of each outcome.
            :param decimals: number of decimal places (default=5)
            :param include_zeros: True to include zero values (default=False)
            :return: dictionary of outcome->probability
        """
        return quantum.probabilities(self._simulator.state, decimals, include_zeros)

    # ------------------------- Measurement -------------------------

    def measure(self, *qubits: int) -> None:
        """ Measure qubits (not a unitary operator).
            :param qubits: qubits (None => all)
            :return: measurement outcome
        """
        if len(qubits) == 0:  # Measure all qubits
            qubits = range(self._nqubits)
        return self.add_measure(list(qubits))

    # ------------------ Wrapper methods for gates ------------------

    # In the following, 'c' stands for control and 't' for target.

    def ccu(self, u: ndarray, name: str, *qubits) -> None:
        """Add a controlled-controlled-U (CCU) gate."""
        qs = list(qubits)
        cu = gates.cu
        self.add_unitary(name, cu(cu(u)), qs[0:2], qs[2:])

    def ccx(self, c1: int, c2: int, t: int) -> None:
        """Add a controlled-controlled-X (CCX) gate."""
        self.add_gate('CCX', [c1, c2], [t])

    def cp(self, phi: float, phi_text: str, c: int, t: int) -> None:
        """ Add a controlled-phase (CP) gate."""
        self.add_param_gate('CP', [c], [t], [phi, phi_text])

    def cs(self, c: int, t: int) -> None:
        """ Add a controlled-S (CS) gate."""
        self.add_gate('CS', [c], [t])

    def cswap(self, c: int, t1: int, t2: int) -> None:
        """ Add a controlled-swap (CSWAP) gate."""
        self.add_gate('CSWAP', [c], [t1, t2])

    def ct(self, c: int, t: int) -> None:
        """ Add a controlled-T (CT) gate."""
        self.add_gate('CT', [c], [t])

    def cu(self, u: ndarray, name: str, *qubits) -> None:
        """Add a controlled-U (CU) gate."""
        qs = list(qubits)
        self.add_unitary(name, gates.cu(u), qs[0:1], qs[1:])

    def cx(self, c: int, t: int) -> None:
        """Add a controlled-X (CX) gate."""
        # self.add_gate('CX', [], [c, t])
        self.add_gate('CX', [c], [t])

    def cy(self, c: int, t: int) -> None:
        """Add a controlled-Y (CY) gate."""
        self.add_gate('CY', [c], [t])

    def cz(self, c: int, t: int) -> None:
        """Add a controlled-Z (CZ) gate."""
        self.add_gate('CZ', [c], [t])

    def h(self, t: int) -> None:
        """Add a Hadamard (H) gate."""
        self.add_gate('H', [], [t])

    def i(self, t: int) -> None:
        """Add an identity (I) gate."""
        self.add_gate('I', [], [t])

    def p(self, phi: float, phi_text: str, t: int) -> None:
        """Add a phase (P) gate."""
        self.add_param_gate('P', [], [t], [phi, phi_text])

    def rx(self, theta: float, theta_text: str, t: int) -> None:
        """Add an RX gate."""
        self.add_param_gate('RX', [], [t], [theta, theta_text])

    def ry(self, theta: float, theta_text: str, t: int) -> None:
        """Add an RY gate."""
        self.add_param_gate('RY', [], [t], [theta, theta_text])

    def s(self, t: int) -> None:
        """Add an S gate."""
        self.add_gate('S', [], [t])

    def swap(self, t1: int, t2: int) -> None:
        """Add a swap (SWAP) gate."""
        self.add_gate('SWAP', [], [t1, t2])

    def sx(self, t: int) -> None:
        """Add a sqrt(X) gate."""
        self.add_gate('SX', [], [t])

    def t(self, t: int) -> None:
        """Add a T gate."""
        self.add_gate('T', [], [t])

    def u(self, u: ndarray, name: str, *qubits):
        """Add a custom unitary gate (U)."""
        self.add_unitary(name, u, [], list(qubits))

    def x(self, t: int) -> None:
        """Add an X gate."""
        self.add_gate('X', [], [t])

    def y(self, t: int) -> None:
        """Add a Y gate."""
        self.add_gate('Y', [], [t])

    def z(self, t: int) -> None:
        """Add a Z gate."""
        self.add_gate('Z', [], [t])

    def barrier(self) -> None:
        """Add a barrier to the circuit."""
        self._model.add_gate('barrier', [], [0, self._nqubits - 1])
