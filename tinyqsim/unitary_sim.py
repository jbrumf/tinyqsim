"""
Simulator to create a unitary matrix from a circuit model.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

import numpy as np
from numpy import ndarray

from tinyqsim.gates import GATES
from tinyqsim.model import Model
from tinyqsim.quantum import unitary_to_tensor, tensor_to_unitary, compose_tensor


class UnitarySimulator:
    """ Simulator to create a unitary matrix from a circuit.
        The circuit must not contain measurements or resets.
    """

    def execute(self, model: Model) -> ndarray:
        """Create unitary matrix from a circuit model.
        :param model: circuit model
        :return: unitary matrix
        """
        nq = model.n_qubits
        gates = GATES
        unitary = unitary_to_tensor(np.eye(2 ** nq))

        # For each gate, create a tensor that applies the gate to the
        # specified qubits, then use this to update the circuit unitary.
        for (name, qubits, params) in model.items:
            ug = None
            match name:
                case 'U':  # Custom unitary
                    ug = params['unitary']
                case 'P' | 'CP' | 'RX' | 'RY' | 'RZ' | 'CRX' | 'CRY' | 'CRZ':  # Param gate
                    ug = gates[name](params['args'])
                case 'measure' | 'reset':
                    raise ValueError('Circuit is not unitary')
                case 'barrier':
                    pass
                case _:  # Simple non-parameterized gate
                    ug = gates[name]

            if ug is not None:
                tgate = unitary_to_tensor(ug)
                unitary = compose_tensor(unitary, tgate, qubits)

        return tensor_to_unitary(unitary).T
