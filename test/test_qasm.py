"""
Pytest unit tests for qasm module.

Licensed under MIT license: see LICENSE.txt
Copyright (c) 2024 Jon Brumfitt
"""

from math import pi

from tinyqsim.qcircuit import QCircuit

PI = '\u03C0'  # Unicode pi


def test_to_qasm1():
    qc = QCircuit(4)
    qc.ccx(0, 1, 2)
    qc.ch(0, 1)
    qc.cp(2 * pi / 5, f'2{PI}/5', 2, 3)
    qc.crx(pi / 5, f'{PI}/5', 0, 1)
    qc.cry(pi / 6, f'{PI}/6', 2, 3)
    qc.crz(2 * pi / 3, f'2{PI}/3', 0, 1)
    # qc.cs(0,1) # Not in QASM2
    qasm = qc.to_qasm()

    exp = """OPENQASM 3;
include "stdgates.inc";
qreg q[4];
ccx q[0],q[1],q[2];
ch q[0],q[1];
cp(1.2566370614359172) q[2],q[3];
crx(0.6283185307179586) q[0],q[1];
cry(0.5235987755982988) q[2],q[3];
crz(2.0943951023931953) q[0],q[1];
"""
    assert qasm == exp


def test_to_qasm2():
    qc = QCircuit(4)
    qc.cswap(0, 1, 2)
    # qc.ct(0,1)  # Not in QASM2
    qc.cx(2, 3)
    qc.cy(0, 1)
    qc.cz(2, 3)
    qc.h(0)
    qc.p(pi / 3, f'{PI}/3', 0)
    qc.rx(2 * pi / 3, f'2{PI}/3', 1)
    qc.ry(2 * pi / 5, f'2{PI}/5', 2)
    qc.rz(3 * pi / 5, f'3{PI}/5', 3)
    qasm = qc.to_qasm()

    exp = """OPENQASM 3;
include "stdgates.inc";
qreg q[4];
cswap q[0],q[1],q[2];
cx q[2],q[3];
cy q[0],q[1];
cz q[2],q[3];
h q[0];
p(1.0471975511965976) q[0];
rx(2.0943951023931953) q[1];
ry(1.2566370614359172) q[2];
rz(1.8849555921538759) q[3];
"""
    assert qasm == exp


def test_to_qasm3():
    qc = QCircuit(4)
    qc.s(0)
    qc.sdg(1)
    qc.swap(2, 3)
    qc.sx(2)
    qc.t(0)
    qc.tdg(1)
    qc.x(0)
    qc.y(1)
    qc.z(2)
    qasm = qc.to_qasm()

    exp = """OPENQASM 3;
include "stdgates.inc";
qreg q[4];
s q[0];
sdg q[1];
swap q[2],q[3];
sx q[2];
t q[0];
tdg q[1];
x q[0];
y q[1];
z q[2];
"""
    assert qasm == exp
