"""
Export circuit in OpenQASM format (prototype).

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024-25 Jon Brumfitt
"""

from io import StringIO

from tinyqsim.model import Model

# QASM = 'OPENQASM 2.0;\ninclude "qelib1.inc";'
QASM = 'OPENQASM 3;\ninclude "stdgates.inc";'

# Note: u, cu and ccu are omitted as they use angles in OpenQASM instead of matrices.
#       The i, cs and ct gates are excluded as they are not supported by OpenQASM-3.
SIMPLE_GATES = ['ccx', 'ch', 'cp', 'crx', 'cry', 'crz', 'cswap', 'cx', 'cy', 'cz', 'h', 'hs', 'p',
                'rx', 'ry', 'rz', 's', 'sdg', 'swap', 'sx', 't', 'tdg', 'x', 'y', 'z']


def _write_gate(f: StringIO, name: str, args: str, qubits: list[int]) -> None:
    """Write a single gate entry to StringIO.
    :param f: file-like object
    :param name: gate name
    :param args: gate arguments
    :param qubits: gate qubits
    """
    if args != '':
        args = '(' + str(args) + ')'
    f.write(f'{name}{args} ')
    qargs = ','.join([f'q[{i}]' for i in qubits])
    f.write(f'{qargs};\n')


def to_qasm(model: Model):
    """Return an OpenQASM representation of a circuit.
    This does not currently support measurement, resets or 'U' gates.
    Gates i, cs & ct are not in the OpenQASM-3 specification.
    :param model: Circuit model
    :return: StringIO representation of circit 'qc'
    """
    nq = model.n_qubits

    with StringIO() as f:
        f.write(f'{QASM}\n')
        f.write(f'qreg q[{nq}];\n')

        for (uc_name, qubits, params) in model.items:
            name = uc_name.lower()
            args = params.get('args', '')
            if name in SIMPLE_GATES:
                _write_gate(f, name, args, qubits)
            else:
                raise ValueError(f'Gate not supported: {name}')

        return f.getvalue()
