"""
Quantum Circuit.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import isclose

import numpy as np
from numpy import ndarray
from numpy.linalg import norm

from tinyqsim import gates, quantum, utils, plotting
from tinyqsim.model import Model
from tinyqsim.schematic import Schematic
from tinyqsim.simulator import Simulator
from tinyqsim.utils import round_complex

EPS = 1e-12  # Threshold for ignoring small values


class QCircuit(object):
    """ Class representing a quantum circuit.

        QCircuit provides the main user interface for TinyQsim.
        A QCircuit instance represents a quantum circuit, with methods to add
        gates, query the state, plot data and perform quantum measurements.

        The big-endian qubit convention is used.
    """

    def __init__(self, nqubits: int, init='zeros', auto_exec=True) -> None:
        """Initialize QCircuit.
           :param: nqubits: number of qubits
           :param: init: initialization mode: 'zeros' or 'random'
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
        """Return a copy of the quantum state vector.
           :return: copy of the quantum state vector
        """
        return self._simulator.state_vector

    @state_vector.setter
    def state_vector(self, state: ndarray) -> None:
        """Setter for state_vector.
            :param state: state vector
        """
        if not isclose(norm(state), 1.0):
            raise ValueError(f'State vector must be normalised: {norm(state)}')
        if not len(state) == 2 ** self._nqubits:
            raise ValueError(f'State vector should have length {2 ** self._nqubits}')

        self._simulator.state_vector = state

    @property
    def n_qubits(self) -> int:
        """Return the number of qubits.
           :return: number of qbits
        """
        return self._nqubits

    def results(self) -> dict[int, int]:
        """Return the most recent results of measurements."""
        return self._simulator.results()

    # ----------------- Add components to the model -----------------

    def _check_qubits(self, qubits) -> None:
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
        self._check_qubits(qubits)
        self._model.add_gate(name, qubits, params)
        if self._auto_exec:
            self._simulator.apply(self._gates[name], qubits)

    def _add_param_gate(self, name: str, qubits: list[int], params: dict) -> None:
        """ Add a parameterized gate to the model.
            :param name: name of the gate
            :param qubits: Qubits
            :param params: Parameter dictionary
        """
        self._check_qubits(qubits)
        self._model.add_gate(name, qubits, params)
        if self._auto_exec:
            u = self._gates[name](params['args'])
            self._simulator.apply(u, qubits)

    def _add_measure(self, qubits: list[int]) -> ndarray:
        """ Add a measurement to the model.
            :param qubits: list of qubits
        """
        self._model.add_gate('measure', qubits)
        if self._auto_exec:
            return self._simulator.measure(qubits)

    def _add_reset(self, qubit: int) -> None:
        """ Add a reset to the model.
            :param qubit: qubit to be reset
        """
        self._model.add_gate('reset', [qubit])
        if self._auto_exec:
            self._simulator.reset(qubit)

    def _add_unitary(self, name: str, u: ndarray, qubits: list[int], params: dict) -> None:
        """ Add a unitary matrix to the model.
            :param name: name of the gate
            :param u: unitary matrix
            :param qubits: qubits
            :param params: Parameter dictionary
        """
        self._check_qubits(qubits)
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

    def execute(self) -> None:
        """Execute/re-execute the circuit."""
        self._simulator.execute(self._model)

    # -------------- Obtain information about the state -------------

    def components(self, decimals: int = 5, include_zeros: bool = False) -> dict:
        """Return complex components of state vector as a dictionary.
           :param decimals: number of decimal places (default=5)
           :param include_zeros: True to include zero values (default=False)
           :return: Dictionary of state components
        """
        comp = quantum.components_dict(self._simulator.state_vector)
        return {k: round_complex(v, decimals) for k, v in comp.items() if include_zeros or abs(v) > EPS}

    def probabilities(self, *qubits: int, decimals: int = 5,
                      include_zeros: bool = False) -> dict[str, float]:
        """ Return dictionary of the probabilities of each outcome.
            :param qubits: qubits (None => all)
            :param decimals: number of decimal places (default=5)
            :param include_zeros: True to include zero values (default=False)
            :return: dictionary of outcome->probability
        """
        if not qubits:
            qubits = range(self._nqubits)
        probs = quantum.probability_dict(self._simulator.state_vector, qubits)
        return {k: round(v, decimals) for k, v in probs.items() if include_zeros or v > EPS}

    def counts(self, *qubits: int, runs: int = 1000, rerun: bool = False,
               include_zeros: bool = False) -> dict[str, int]:
        """ Return measurement counts for repeated experiment.
            Any measurements within the circuit will be re-run if rerun=True.
            :param qubits: qubits (None => all)
            :param runs: Number of test runs (default=1000)
            :param rerun: True to re-run the whole experiment (default=False)
            :param include_zeros: True to include zero values (default=False)
            :return: frequencies of outcomes as a dictionary
        """
        if not qubits:
            qubits = range(self.n_qubits)
        if not rerun:
            dic = quantum.counts_dict(self._simulator.state_vector, list(qubits), runs)
        else:
            sim = self._simulator
            names = quantum.basis_names(len(qubits))
            count = np.zeros(2 ** len(qubits), dtype=int)
            for run in range(runs):
                sim.execute(self._model)
                probs = quantum.probabilities(sim.state_vector, qubits)
                k = np.random.choice(len(probs), None, p=probs)
                count[k] += 1
            dic = dict(zip(names, count))
        return {k: v for k, v in dic.items() if include_zeros or v > EPS}

    # ------------------ Measurement ------------------

    def measure(self, *qubits: int) -> ndarray:
        """Add a measurement gate to one or more qubits.
            :param qubits: qubits (None => all)
        """
        if not qubits:
            qubits = range(self._nqubits)
        return self._add_measure(list(qubits))

    def reset(self, qubit: int) -> None:
        """Reset the state of qubit to |0>.
        :param qubit: qubit index
        """
        self._add_reset(qubit)

    # -------------------------- Graphics ---------------------------

    def qubit_labels(self, labels: dict[int, str], numbers: bool = True) -> None:
        """Assign labels to qubits
            :param labels: Dictionary of qubit labels
            :param numbers: True to assign q0, q1,... as default labels
        """
        self._schematic.set_labels(labels, numbers=numbers)

    def draw(self, show: bool = True, save: str | None = None) -> None:
        """Draw the quantum circuit.
            :param: show: show the quantum circuit
            :param: save: file to save image if required
        """
        self._schematic.draw(self._model, show=show, save=save)

    def plot_probabilities(self, *qubits: int, save: str | None = False,
                           height: float = 1) -> None:
        """Plot histogram of probabilities of measurement outcomes.
            :param qubits: qubits (None => all)
            :param save: file to save image if required
            :param height: Scaling factor for plot height
        """
        if not qubits:
            qubits = range(self._nqubits)
        probs = quantum.probability_dict(self._simulator.state_vector, qubits)
        plotting.plot_histogram(probs, save=save, ylabel='Probability', height=height)

    def plot_counts(self, *qubits: int, runs: int = 1000, rerun: bool = False,
                    save: str | None = False, height: float = 1) -> None:
        """Plot histogram of measurement counts.
        :param qubits: qubits (None => all)
        :param runs: number of test runs (default=1000)
        :param rerun: True to re-run the whole experiment (default=False)
        :param save: file to save image if required
        :param height: Scaling factor for plot height
        """
        freq = self.counts(*qubits, runs=runs, rerun=rerun, include_zeros=True)
        plotting.plot_histogram(freq, save=save, ylabel='Counts', height=height)

    # ------------------ Wrapper methods for gates ------------------

    # In the following, 'c' stands for control and 't' for target.

    def ccu(self, u: ndarray, name: str, *qubits) -> None:
        """Add a controlled-controlled-U (CCU) gate.
        :param name: name of gate to appear in symbol
        :param u: unitary matrix
        :param qubits: list of qubits
        """
        qs = list(qubits)
        cu = gates.cu
        self._add_unitary(name, cu(cu(u)), qs, {'controls': 2})

    def ccx(self, c1: int, c2: int, t: int) -> None:
        """Add a controlled-controlled-X (CCX, aka Tofolli) gate.
        :param c1: control qubit
        :param c2: target qubit
        :param t: target qubit
        """
        self._add_gate('CCX', [c1, c2, t], {'controls': 2})

    def ch(self, c: int, t: int) -> None:
        """Add a controlled-H gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CH', [c, t], {'controls': 1})

    def cp(self, phi: float, phi_text: str, c: int, t: int) -> None:
        """Add a controlled-phase (CP) gate.
        :param phi: phase angle in radians
        :param phi_text: text annotation for phase angle
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
        """ Add a controlled-swap (CSWAP, aka Fredkin) gate.
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
        :param name: name of gate to appear in symbol
        :param qubits: list of qubits
        """
        qs = list(qubits)
        self._add_unitary(name, gates.cu(u), qs, {'controls': 1})

    def cx(self, c: int, t: int) -> None:
        """Add a controlled-X (CX, aka CNOT) gate.
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
        :param theta_text: text annotation for phase angle
        :param t: target qubit
        """
        self._add_param_gate('RX', [t], {'args': theta, 'label': theta_text})

    def ry(self, theta: float, theta_text: str, t: int) -> None:
        """Add an RY gate.
        :param theta: target qubit
        :param theta_text: text annotation for phase angle
        :param t: target qubit
        """
        self._add_param_gate('RY', [t], {'args': theta, 'label': theta_text})

    def s(self, t: int) -> None:
        """Add an S gate.
        :param t: target qubit
        """
        self._add_gate('S', [t])

    def sdg(self, t: int) -> None:
        """Add an S-dagger gate.
        :param t: target qubit
        """
        self._add_gate('Sdg', [t])

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

    def tdg(self, t: int) -> None:
        """Add an T-dagger gate.
        :param t: target qubit
        """
        self._add_gate('Tdg', [t])

    def u(self, u: ndarray, name: str, *qubits):
        """Add a custom unitary gate (U).
        :param u: unitary matrix
        :param name: name of gate to appear in symbol
        :param qubits: list of qubits
        """
        self._add_unitary(name, u, list(qubits), {})

    def x(self, t: int) -> None:
        """Add an X (NOT) gate.
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
