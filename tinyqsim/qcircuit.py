"""
Quantum Circuit.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import isclose

import numpy as np
from IPython.display import Math, display
from numpy import ndarray
from numpy.linalg import norm

from tinyqsim import gates, quantum, utils, plotting, format, unitary_sim, qasm
from tinyqsim.format import state_kets, format_table
from tinyqsim.model import Model
from tinyqsim.schematic import Schematic
from tinyqsim.simulator import Simulator


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

    # --------------- Miscellaneous ---------------

    def basis_names(self, nqubits: int = 0, kets: bool = False) -> list[str]:
        """Return a list of basis names.
        :param nqubits: number of qubits (default is for current state)
        :param kets: format as ket symbol
        :return: list of basis names
        """
        nq = self.n_qubits
        if nqubits != 0:
            nq = nqubits
        return quantum.basis_names(nq, kets)

    def results(self) -> dict[int, int]:
        """Return the most recent results of measurements.
        :return: results of most recent measurements"""
        return self._simulator.results()

    # ----------------- Add components to the model -----------------

    def _check_qubits(self, qubits) -> None:
        """ Validate qubit indices.
            :param qubits: list of qubits
        """
        if min(qubits) < 0 or max(qubits) >= self._nqubits:
            raise ValueError(f'Qubit indices out of range: {qubits}')

    def _add_gate(self, name: str, qubits: list[int], params: dict = None) -> None:
        """ Add a gate operating on one or more qubits to the model.
            :param name: name of the gate
            :param qubits: qubits
            :param params: parameter dictionary
        """
        self._check_qubits(qubits)
        self._model.add_gate(name, qubits, params)
        if self._auto_exec:
            self._simulator.apply(self._gates[name], qubits)

    def _add_gates(self, name: str, qubits: list[int], params: dict = None) -> None:
        """ Add zero or more one-qubit gates to the model.
            :param name: name of the gate
            :param qubits: qubit(s)
            :param params: parameter dictionary
        """
        if len(qubits) == 0:
            return
        self._check_qubits(qubits)
        for q in qubits:
            self._model.add_gate(name, [q], params)
            if self._auto_exec:
                self._simulator.apply(self._gates[name], [q])

    def _add_param_gate(self, name: str, qubits: list[int], params: dict) -> None:
        """ Add a parameterized gate operating on one or more qubits to the model.
            :param name: name of the gate
            :param qubits: Qubits
            :param params: Parameter dictionary
        """
        self._check_qubits(qubits)
        self._model.add_gate(name, qubits, params)
        if self._auto_exec:
            u = self._gates[name](params['args'])
            self._simulator.apply(u, qubits)

    def _add_param_gates(self, name: str, qubits: list[int], params: dict) -> None:
        """ Add zero or more one-qubit parameterized gates to the model.
            :param name: name of the gate
            :param qubits: qubits
            :param params: parameter dictionary
        """
        if len(qubits) == 0:
            return
        self._check_qubits(qubits)
        u = self._gates[name](params['args'])
        for q in qubits:
            self._model.add_gate(name, [q], params)
            if self._auto_exec:
                self._simulator.apply(u, [q])

    def _add_measure(self, qubits: list[int]) -> ndarray | None:
        """ Add a measurement to the model.
            :param qubits: list of qubits
        """
        self._model.add_gate('measure', qubits)
        if self._auto_exec:
            return self._simulator.measure(qubits)
        else:
            return None

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

    def execute(self, init='zeros') -> None:
        """Execute/re-execute the circuit.
        The init='none' option skips the initialization.
        :param init: Initial state - 'zeros' | 'random' | 'none'
        """
        self._simulator.execute(self._model, init)

    def to_unitary(self):
        """Return unitary matrix of this circuit.
        The circuit must not contain measurements or resets.
        :return: unitary matrix
        """
        return unitary_sim.UnitarySimulator().execute(self._model)

    # -------------- Obtain information about the state -------------

    def format_state(self, mode='kets', decimals: int = 5, include_zeros: bool = False,
                     trim: bool = True, edge: int = 4) -> str:
        """Return state vector formatted for printing.\n
        The 'edge' option includes any results excluded by 'include_zeros'.
        :param mode: 'kets' | 'table'| 'latex'
        :param decimals: number of decimal places (default=5)
        :param include_zeros: True to include zero values (default=False)
        :param trim: trim trailing fractional zeros
        :param edge: Number of items before and after ellipsis (table only)
        :return: Formatted string
        """
        match mode:
            case 'kets':
                return state_kets(self._simulator.state_vector, decimals=decimals,
                                  include_zeros=include_zeros, trim=trim, latex=False)
            case 'latex':
                return state_kets(self._simulator.state_vector, decimals=decimals,
                                  include_zeros=include_zeros, trim=trim, latex=True)

            case 'table':
                return format_table(self._simulator.state_vector,
                                    decimals=decimals, include_zeros=include_zeros,
                                    trim=trim, edge=edge)
            case _:
                raise ValueError(f'Invalid mode: {mode}')

    def display_state(self, prefix: str = '', decimals: int = 5,
                      include_zeros=False, trim=True) -> None:
        """Display state in notebook in ket notation using LaTeX.\n
        This method is equivalent to 'display(Math(format_state('latex', \\<args\\>))).
        :param prefix: prefix string
        :param decimals: number of decimal places
        :param include_zeros: whether to include zero values
        :param trim: trim trailing fractional zeros
        """
        ltx = format.latex_state(self._simulator.state_vector, prefix=prefix,
                                 decimals=decimals, include_zeros=include_zeros, trim=trim)
        display(Math(ltx))

    def format_probabilities(self, *qubits: int, decimals: int = 5,
                             include_zeros: bool = False, trim: bool = True,
                             edge: int = 4) -> dict[str, str]:
        """ Return probabilities of each outcome formatted for printing.
            :param qubits: qubits (None => all)
            :param decimals: number of decimal places (default=5)
            :param include_zeros: True to include zero values (default=False)
            :param trim: trim trailing fractional zeros
            :param edge: Number of items before and after ellipsis
            :return: basis-state->probability string
        """
        if not qubits:
            qubits = range(self._nqubits)

        probs = quantum.probabilities(self._simulator.state_vector, qubits)
        return format_table(probs, decimals=decimals, include_zeros=include_zeros,
                            trim=trim, edge=edge)

    def probability_dict(self, *qubits: int) -> dict[str, float]:
        """ Return dictionary of the probabilities of each outcome.
            :param qubits: qubits (None => all)
            :return: dictionary mapping basis-state->probability value
        """
        if not qubits:
            qubits = range(self._nqubits)
        return quantum.probability_dict(self._simulator.state_vector, qubits)

    # FIXME: Return type might change to be like state_vector (TBC)
    def probability_array(self, *qubits) -> ndarray:
        """ Return array of probabilities of each outcome.
            :param qubits: qubits (None => all)
            :return: array of probabilities for each basis state
        """
        if not qubits:
            qubits = range(self._nqubits)
        return quantum.probabilities(self._simulator.state_vector, qubits)

    def _final_counts(self, qubits: range | list[int], runs: int):
        """Return counts of measuring circuit outputs.
        :param qubits: qubits to be measured
        :param runs: number of runs
        """
        sim = self._simulator
        names = quantum.basis_names(len(qubits))
        count = np.zeros(2 ** len(qubits), dtype=int)
        for run in range(runs):
            sim.execute(self._model)
            probs = quantum.probabilities(sim.state_vector, qubits)
            key = np.random.choice(len(probs), None, p=probs)
            count[key] += 1
        return dict(zip(names, count.tolist()))

    def _measurement_counts(self, qubits: range | list[int], runs) -> dict:
        """Return counts for specified qubits.
        :param qubits: qubits to be measured
        :param runs: number of runs
        """
        nbits = len(qubits)
        count = dict(zip(quantum.basis_names(nbits), [0] * 2 ** nbits))
        for run in range(runs):
            self._simulator.execute(self._model)
            r = self._simulator.results()
            k = 2 ** (nbits - 1)
            n = 0
            for i, qi in enumerate(qubits):
                n += k * r.get(qi, 0)
                k //= 2
            key = ''.join([i for i in bin(n)[2:].zfill(nbits)])
            count[key] += 1
        return count

    def counts(self, *qubits: int, runs: int = 1000, mode: str = 'resample',
               include_zeros: bool = False) -> dict[str, int]:
        """ Return measurement counts for repeated experiment.
        :param qubits: qubits (None => all)
        :param runs: Number of test runs (default=1000)
        :param mode: 'resample' | 'repeat' | 'measure'
        :param include_zeros: True to include zero values (default=False)
        :return: frequencies of outcomes as a dictionary
        """
        if not qubits:
            qubits = range(self.n_qubits)

        match mode:
            case 'resample':
                dic = quantum.counts_dict(self._simulator.state_vector, list(qubits), runs)
            case 'repeat':
                dic = self._final_counts(qubits, runs)
            case 'measure':
                dic = self._measurement_counts(qubits, runs)
            case _:
                raise ValueError(f'Invalid mode: {mode}')
        return {k: v for k, v in dic.items() if include_zeros or v > 0}

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

    def plot_probabilities(self, *qubits: int, show=True, save: str | None = False,
                           height: float = 1, ylim: list[float] | None = None) -> None:
        """Plot histogram of probabilities of measurement outcomes.
        See the 'counts' method for further details.
        :param qubits: qubits (None => all)
        :param show: show the plot
        :param save: file to save image if required
        :param height: Scaling factor for plot height
        :param ylim: Y-axis limits [min, max]
        """
        if not qubits:
            qubits = range(self._nqubits)
        probs = quantum.probability_dict(self._simulator.state_vector, qubits)
        plotting.plot_histogram(probs, show=show, save=save, ylabel='Probability',
                                height=height, ylim=ylim)

    def plot_counts(self, *qubits: int, runs: int = 1000, mode: str = 'resample',
                    show=True, save: str | None = False, height: float = 1) -> None:
        """Plot histogram of measurement counts.
        See the 'probabilities' method for further details.
        :param qubits: qubits (None => all)
        :param runs: number of test runs (default=1000)
        :param mode: 'resample' | 'repeat' | 'measure'
        :param show: show the plot
        :param save: file to save image if required
        :param height: Scaling factor for plot height
        """
        freq = self.counts(*qubits, runs=runs, mode=mode, include_zeros=True)
        plotting.plot_histogram(freq, show=show, save=save, ylabel='Counts', height=height)

    # ------------------ I/O ------------------

    def to_qasm(self) -> str:
        """Return an OpenQASM version of the quantum circuit.
           Some TinyQsim constructs are not supported.
           :return: OpenQASM version of the quantum circuit
         """
        return qasm.to_qasm(self._model)

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
        :param c2: control qubit
        :param t: target qubit
        """
        self._add_gate('CCX', [c1, c2, t], {'controls': 2})

    def ch(self, c: int, t: int) -> None:
        """Add a controlled-H gate.
        :param c: control qubit
        :param t: target qubit
        """
        self._add_gate('CH', [c, t], {'controls': 1})

    def cp(self, phi: float, label: str, c: int, t: int) -> None:
        """Add a controlled-phase (CP) gate.
        :param phi: phase angle in radians
        :param label: text annotation for phase angle
        :param c: control qubit
        :param t: target qubit
        """
        self._add_param_gate('CP', [c, t],
                             {'args': phi, 'label': label, 'controls': 1})

    def crx(self, theta: float, label: str, c: int, t: int) -> None:
        """Add a CRX gate.
        :param theta: target qubit
        :param label: text annotation for angle
        :param c: control qubit
        :param t: target qubit
        """
        self._add_param_gate('CRX', [c, t],
                             {'args': theta, 'label': label, 'controls': 1})

    def cry(self, theta: float, label: str, c: int, t: int) -> None:
        """Add a CRY gate.
        :param theta: target qubit
        :param label: text annotation for angle
        :param c: control qubit
        :param t: target qubit
        """
        self._add_param_gate('CRY', [c, t],
                             {'args': theta, 'label': label, 'controls': 1})

    def crz(self, theta: float, label: str, c: int, t: int) -> None:
        """Add a CRZ gate.
        :param theta: target qubit
        :param label: text annotation for angle
        :param c: control qubit
        :param t: target qubit
        """
        self._add_param_gate('CRZ', [c, t],
                             {'args': theta, 'label': label, 'controls': 1})

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

    def h(self, ts: int | list[int]) -> None:
        """Add one or more Hadamard (H) gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('H', ts)

    def i(self, ts: int | list[int]) -> None:
        """Add one or more identity (H) gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('I', ts)

    def p(self, phi: float, label: str, ts: int | list[int]) -> None:
        """Add a phase (P) gate.
        :param phi: phase angle
        :param label: text value of phase angle
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_param_gates('P', ts, {'args': phi, 'label': label})

    def rx(self, theta: float, label: str, ts: int | list[int]) -> None:
        """Add an RX gate.
        :param theta: target qubit
        :param label: text annotation for angle
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_param_gates('RX', ts, {'args': theta, 'label': label})

    def ry(self, theta: float, label: str, ts: int | list[int]) -> None:
        """Add an RY gate.
        :param theta: target qubit
        :param label: text annotation for angle
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_param_gates('RY', ts, {'args': theta, 'label': label})

    def rz(self, theta: float, label: str, ts: int | list[int]) -> None:
        """Add an RZ gate.
        :param theta: target qubit
        :param label: text annotation for angle
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_param_gates('RZ', ts, {'args': theta, 'label': label})

    def s(self, ts: int | list[int]) -> None:
        """Add one or more S gates.
        :param ts: target qubit
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('S', ts)

    def sdg(self, ts: int | list[int]) -> None:
        """Add one or more S-dagger (SDG) gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('Sdg', ts)

    def swap(self, t1: int, t2: int) -> None:
        """Add a swap (SWAP) gate.
        :param t1: target qubit
        :param t2: target qubit
        """
        self._add_gate('SWAP', [t1, t2])

    def sx(self, ts: int | list[int]) -> None:
        """Add one or more sqrt(X) gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('SX', ts)

    def t(self, ts: int | list[int]) -> None:
        """Add one or more T gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('T', ts)

    def tdg(self, ts: int | list[int]) -> None:
        """Add one or more T-dagger gatea.
        :param ts: target qubita
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('Tdg', ts)

    def u(self, u: ndarray, name: str, *qubits):
        """Add a custom unitary gate (U).
        :param u: unitary matrix
        :param name: name of gate to appear in symbol
        :param qubits: list of qubits
        """
        self._add_unitary(name, u, list(qubits), {})

    def x(self, ts: int | list[int]) -> None:
        """Add one or more Pauli X (NOT) gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('X', ts)

    def y(self, ts: int | list[int]) -> None:
        """Add one or more Pauli Y gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('Y', ts)

    def z(self, ts: int | list[int]) -> None:
        """Add one or more Pauli Z gates.
        :param ts: target qubits
        """
        if isinstance(ts, int):
            ts = [ts]
        self._add_gates('Z', ts)

    def barrier(self) -> None:
        """Add a barrier to the circuit."""
        self._model.add_gate('barrier', [0, self._nqubits - 1])
