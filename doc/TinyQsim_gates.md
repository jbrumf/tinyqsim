## TinyQsim Gates

This document describes the quantum gates implemented by TinyQsim.

<!-- TOC -->

- [TinyQsim Gates](#tinyqsim-gates)
- [Introduction](#introduction)
  - [Summary of Gates](#summary-of-gates)
  - [Other Elements](#other-elements)
  - [Imports and Definitions](#imports-and-definitions)
  - [Symbols and Notation](#symbols-and-notation)
  - [Controlled Gates](#controlled-gates)
  - [Anti-Controlled Gates](#anti-controlled-gates)
  - [Angle Parameters](#angle-parameters)
  - [Custom Gates](#custom-gates)
  - [Parameterized Custom Gates](#parameterized-custom-gates)
  - [Global Phase](#global-phase)
- [Gates in Alphabetical Order](#gates-in-alphabetical-order)
  - [CCU](#ccu)
  - [CCX (aka Toffoli) Gate](#ccx-aka-toffoli-gate)
  - [CH Gate](#ch-gate)
  - [CP Gate](#cp-gate)
  - [CS Gate](#cs-gate)
  - [CSWAP (aka Fredkin) Gate](#cswap-aka-fredkin-gate)
  - [CT Gate](#ct-gate)
  - [CU](#cu)
  - [CX (aka CNOT) Gate](#cx-aka-cnot-gate)
  - [CY Gate](#cy-gate)
  - [CZ Gate](#cz-gate)
  - [H Gate](#h-gate)
  - [I (aka ID) Gate](#i-aka-id-gate)
  - [P Gate](#p-gate)
  - [RX Gate](#rx-gate)
  - [RY Gate](#ry-gate)
  - [S Gate](#s-gate)
  - [Sdg Gate](#sdg-gate)
  - [SWAP Gate](#swap-gate)
  - [SX (aka V, SQRTX) Gate](#sx-aka-v-sqrtx-gate)
  - [T Gate](#t-gate)
  - [Tdg Gate](#tdg-gate)
  - [U Gate](#u-gate)
  - [X (aka NOT) Gate](#x-aka-not-gate)
  - [Y Gate](#y-gate)
  - [Z Gate](#z-gate)
- [Non-Unitary Operations](#non-unitary-operations)
  - [Measure](#measure)
  - [Reset](#reset)
- [Other Symbols](#other-symbols)
  - [Barrier](#barrier)

<!-- TOC -->

## Introduction

### Summary of Gates

| API                               | Description                              | 
|:----------------------------------|:-----------------------------------------|
| qc.ccu(matrix, label, c1, c2, *t) | Controlled-controlled-U gate             |
| qc.ccx(c1, c2, t)                 | Controlled-controlled-X (aka Toffoli)    |
| qc.ch(c, t)                       | Controlled-H                             |
| qc.cp(phi, label, c, t)           | Controlled-P                             |
| qc.cs(c, t)                       | Controlled-S                             |
| qc.cswap(c, t1, t2)               | Controlled SWAP (aka Fredkin)            |
| qc.ct(c, t)                       | Controlled-T                             |
| qc.cu(matrix, label, c, *t)       | Controlled-U gate                        |
| qc.cx(c, t)                       | Controlled-X (aka CNOT)                  |
| qc.cy(c, t)                       | Controlled-Y                             |
| qc.cz(c, t)                       | Controlled-Z                             |
| qc.h(t)                           | Hadamard                                 |
| qc.i(t)                           | Identity (aka ID)                        |
| qc.p(phi, label, t)               | Phase: 'phi' radians about Z axis        |
| qc.rx(theta, label, t)            | Rotation by 'theta' radians about X axis |
| qc.ry(theta, label, t)            | Rotation by 'theta' radians about Y axis |
| qc.s(t)                           | pi/2 phase (S = sqrt(Z))                 |
| qc.sdg(t)                         | -pi/2 phase (S-dagger)                   |
| qc.swap(t1, t2)                   | Swap 2 qubits                            |
| qc.sx(t)                          | Sqrt(X) (aka V, SQRTX)                   |
| qc.t(t)                           | pi/4 phase (T = sqrt(S))                 |
| qc.tdg(t)                         | -pi/4 phase (T dagger)                   |
| qc.u(matrix, label, *t)           | Use unitary matrix as a gate             |
| qc.x(t)                           | Pauli X (aka NOT)                        |
| qc.y(t)                           | Pauli Y                                  |
| qc.z(t)                           | Pauli Z                                  |

The argument names are abbreviations for:

```
  c      Control qubit
  t      Target qubit
  *t     One or more target qubits
  label  Text label
  phi    Angle in radians
  theta  Angle in radians
```

### Other Elements

The following are additional circuit elements that are strictly not gates because they are not reversible unitary operations.

| API                               | Description                              | 
|:----------------------------------|:-----------------------------------------|
| qc.barrier()                      | Insert barrier in circuit (not a gate)   |
| qc.measure(*t)                    | Measurement operation (not a gate)       |
| qc.reset(t)                       | Reset qubit to |0>                       |

### Imports and Definitions

The examples in the following sections assume that the following imports and definitions have been made:

```
from tinyqsim.qcircuit import QCircuit
import numpy as np
from math import pi

PI = '\u03C0'  # Unicode PI
```

Unicode $\pi$ is useful for annotating parameterized gates that have an angle argument, so that the angle is clear from the quantum circuit schematic.

### Symbols and Notation

The examples assume that a QCircuit instance has been created with the name 'qc'.
For example:

```
qc = QCircuit(2)
```

An instance of a gate (e.g. the CX gate) can then be added to the circuit as follows:

```
qc.cx(0, 1)
```

The 'draw' command can then be used to draw the quantum circuit:

```
qc.draw()
```

<div style="text-align: center;">
<img src="assets/cx_gate.png" alt="cx_gate" width="80"/>
</div>

The horizontal lines represent the qubits of the quantum circuit, which are labelled q0, q1, q2, etc.

Gate names are usually upper case (e.g. 'CX') whereas the corresponding QCircuit method names are lower case (e.g. 'cx').

The CX gate has the following API:

```
cx(c: int, t: int)
   c : the control qubit
   t : the target qubit
```

The call `qc.cx(0,1)` creates an instance of the gate with the control connected to qubit q0 and the target connected to q1.

If the arguments had been in the reverse order, q1 would have been the control and q0 the target, as shown here:

```
qc.cx(1,0)
```

<div style="text-align: center;">
<img src="assets/cx_gate10.png" alt="cx_gate10" width="80"/>
</div>

In a quantum circuit the gates are often applied to non-consective qubits, such as q0 and q2. For example:

```
qc = QCircuit(3)
qc.cx(0, 2)
```

<div style="text-align: center;">
<img src="assets/cx_gate02.png" alt="cx_gate02" width="80"/>
</div> 

The vertical line passes over q1 without a dot, as q1 plays no role. If there were a dot on q1, it would indicate a gate with two controls, which would make it a CCX gate. For example:

```
qc = QCircuit(3)
qc.ccx(0,1,2)  # CCX with 3 arguments
```

<div style="text-align: center;">
<img src="assets/ccx_gate.png" alt="ccx_gate" width="80"/>
</div>

Since, swapping the two controls of a CCX makes no difference, the symbol does not distinguish between them.

Finally, custom gates are represented by a rectangle as they have no special symbol. See the following example:

```
qc = QCircuit(5)
qc.ccu(mygate, 'U1', 0, 3, 1, 4)
```

<div style="text-align: center;">
<img src="assets/ccu0314_gate.png" alt="ccu0314_gate" width="80"/>
</div>  

Note the following points about this example:

- The dotted line on qubit q2 indicates that it just passes through without playing a role.

- The first two arguments (0, 3) of the call are the control qubits, which are indicated by a dot. The control qubits may be inside or outside the box as shown here.

- The numbers (0, 1) in the symbol indicate that these are arguments 0 and 1 for the unitary U (excluding controls). In the example, these are connected to qubits q1 and q4.

### Controlled Gates

Gates can have a *controlled* variant. The control enables the operation of the gate.

The controlled version CU of a gate U applies the gate if the control is $\ket{1}$. For example, for a one-qubit gate defined by the unitary matrix $U$:

```math
CU = \ket{0}\bra{0} \otimes I + \ket{1}\bra{1} \otimes U
```

Since the input may be in a superposition of $\ket{0}$ and $\ket{1}$, the result is the superposition of the CU gate applied to the two components.

TinyQsim provides controlled versions of many of the common gates. For example, CX is a controlled version of the X gate. Controls are denoted by a solid dot in the symbol, as shown in the earlier examples of the CX gate. It is possible for a gate to have multiple controls, such as the CCX gate.

A generic U gate is provided that allows a unitary matrix $U$ to be applied as a gate. This has CU and CCU variants. See the sections on the U, CU and CCU gates below for details.

### Anti-Controlled Gates

Anti-controlled gates are ones where the control is inverted, so that it disables the operation instead of enabling it. These are sometimes drawn like a controlled gate but with a hollow (white) control dot instead of a solid (black) one.

TinyQsim does not have specific support for them, but the same effect can be created by sandwiching a control between two X gates, as shown here:

<div style="text-align: center;">
<img src="assets/anti_control.png" alt="anti_control" height="110"/>
</div>

### Angle Parameters

One-qubit gates typically implement rotations of the state vector on the Bloch sphere. Some of these are fixed-angle rotations, such as X, Y, Z, S, T, etc. Others allow a user-specified rotation angle.

The P, CP, RX and RY gates have two parameters for the angle. The first is the angle in radians and the second is a label for the circuit symbol that shows the angle in a convenient form, such as a multiple of $\pi$.

The following examples show how to specify the label using a simple ASCII 'pi' or a Unicode $\pi$.

```
  PI = '\u03C0'  # PI unicode character
  
  qc.p(pi/3, 'pi/3', 1)      # ASCII 'pi/3'
  qc.p(pi/3, f'{PI}/3', 1)   # Unicode PI/3
```

<div style="text-align: center;">
<img src="assets/p_gate_pi3.png" alt="p_gate_pi3" width="80"/>
</div>

### Custom Gates

Custom gates are possible using the U gate that takes a unitary matrix as an argument. For example:

```
u1 = numpy.array([[1, 0, 0, 0],  # Define a unitary matrix
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1]])
                 
qc = QCircuit(2)
qc.u(u1, 'U1', 0, 1)  # Apply the matrix as a gate
```

This automatically generates a symbol which is labelled with the string given as the second argument.

<div style="text-align: center;">
<img src="assets/u2_gate.png" alt="u2_gate" width="80"/>
</div>

There are also CU and CCU variants for controlled-U and controlled-controlled-U gates.

For further details see the 'U' gate in the [TinyQsim Gates](TinyQsim_gates.md) guide.

### Parameterized Custom Gates

A parameterized gate can be defined as a function that returns a unitary matrix.

For example, suppose that we wish to create the following custom parameterized phase gate.

```math
\text{RK}(k) =\begin{bmatrix}1 & 0 \\ 0 & e^{\large\frac{2\pi i}{2^k}}\end{bmatrix}
```

One way to define it is:

```
  def rk(k: int):
      return np.array([[1, 0], [0, cexp(1j * 2 * pi / 2 ** k)]])
```

Alternatively, we could define it in terms of the existing P (phase) gate, as follows:

```
  def rk(k: int):
      return gates.P(2 * pi / 2 ** k)
```

In either case, the gate can be added to the circuit like this:

```
  qc.QCircuit(4)
  qc.u(rk(3), 'RK', 2)  # Add rk(3) to qubit 2
```

### Global Phase

Some gates may appear to be equivalent, but actually differ in a subtle way.

For example, the RX(theta) gate performs a rotation by 'theta' radians about the X axis, whilst the X gate performs a rotation by $\pi$ about the X axis. So it might seem that $RX(\pi) = X$.

However, because of the way they are defined:

```math
RX(\pi) = \begin{bmatrix}
0 & -i \\ -i  & 0
\end{bmatrix}\quad\textrm{and}\quad
X = \begin{bmatrix}
0 & 1 \\ 1  & 0
\end{bmatrix}
```

Hence $X=i\,RX(\pi)$.

A global phase term has no effect on any experiment we can perform. Consider a quantum state with a global phase term $e^{i\phi}$:

```math
 \ket{\psi} = e^{i\phi}(\alpha_0 \ket{0} + \alpha_1 \ket{1})
 ```

Then the probability of the measurement outcome $\ket{0}$, for example, is:

```math
\begin{align*}
p(\ket{0}) &= (e^{i\phi}\alpha_0)^*\, (e^{i\phi}\alpha_0)\\
&=\alpha_0^*\,\alpha_0\\
&=|\alpha_0|^2
\end{align*}
```

where $^*$ denotes complex conjugation.

Consequently, the global phase term has no effect on the measurement outcome.

This extends to a multi-qubit system since:

```math
(e^{i\phi} \ket{\psi}) \otimes \ket{\chi} = e^{i\phi}(\ket{\psi} \otimes \ket{\chi})
```

----

## Gates in Alphabetical Order

### CCU

The CCU gate is a controlled-controlled custom unitary gate. See the U gate for further details.

It applies unitary matrix U to the target qubit if both the controls are $\ket{1}$.

<div style="text-align: center;">
<img src="assets/ccu_gate.png" alt="ccx_gate" width="80"/>
</div>

```
Example:
   u = numpy.array([[0,1],[1,0]])
   qc.ccu(u, 'U', 0, 1, 2)
   
API:
   ccu(u: ndarray, name: str, c1: int, c2: int, *t: int)
      u    : unitary numpy matrix
      name : Name of gate   
      c1   : the first control qubit
      c2   : the second control qubit
      *t   : the target qubits
```

The unitary matrix is of size $2^k \times 2^k$ for $k$ target qubits.

### CCX (aka Toffoli) Gate

The CCX gate is a controlled-controlled-X gate. See the X gate for further details.

It applies an X (NOT) operation to the target qubit if both the controls are $\ket{1}$.

<div style="text-align: center;">
<img src="assets/ccx_gate.png" alt="ccx_gate" width="80"/>
</div>

```
Example:
   qc.ccx(0, 1, 2)
   
API:
   ccx(c1: int, c2: int, t: int)
      c1 : the first control qubit
      c2 : the second control qubit
      t  : the target qubit
```

### CH Gate

The CH gate is a controlled version of the H gate. See the H gate for further details.

<div style="text-align: center;">
<img src="assets/ch_gate.png" alt="ch_gate" width="80"/>
</div>

```
Example:
   qc.ch(0, 1)

API:
   ch(c: int, t: int)
      c : the control qubit
      t : the target qubit
```

### CP Gate

The CP gate is a controlled version of the P gate. See the P gate for further details.

The first argument is the phase angle in radians. The second argument is the phase angle as a string that is used to label the circuit symbol. The phase angles are typically multiples of 'pi', so it is convenient to use the unicode 'pi' in the text string. See the P gate for further details.

<div style="text-align: center;">
<img src="assets/cp_gate.png" alt="cp_gate" width="80"/>
</div>

```
Example:
   qc.cp(pi/2, f'{PI}/2', 0, 1)

API:
   cp(phi: float, phi_text: str, c: int, t: int)
      phi      : the phase angle in radians
      phi_text : Text annotation for the angle
      c        : the control qubit
      t        : the target qubit
```

### CS Gate

The CS gate is a controlled version of the S gate. See the S gate for further details.

<div style="text-align: center;">
<img src="assets/cs_gate.png" alt="cs_gate" width="80"/>
</div>

```
Example:
   qc.cs(0, 1)

API:
   cs(c: int, t: int)
      c : the control qubits
      t : the target qubit
```

### CSWAP (aka Fredkin) Gate

The CSWAP gate is a controlled version of the SWAP gate. See the SWAP gate for further details.

<div style="text-align: center;">
<img src="assets/cswap_gate.png" alt="cswap_gate" width="80"/>
</div>

```
Example:
   qc.cswap(0, 1, 2)

API:
   cswap(c: int, t1: int, t2: int)
      c  : the control qubits
      t1 : the first target qubit
      t2 : the second target qubit
```

### CT Gate

The CT gate is a controlled version of the T gate. See the T gate for further details.

<div style="text-align: center;">
<img src="assets/ct_gate.png" alt="ct_gate" width="80"/>
</div>

```
Example:
   qc.ct(0, 1)

API:
   ct(c: int, t: int)
      c : the control qubit
      t : the target qubit
```

### CU

The CU gate is a controlled custom unitary gate. See the U gate for further details.

It applies unitary matrix U to the target qubit if the control is $\ket{1}$.

<div style="text-align: center;">
<img src="assets/cu_gate.png" alt="cu_gate" width="80"/>
</div>

```
Example:
   u = numpy.array([[0,1],[1,0]])
   qc.cu(u, 'U', 0, 1)
   
API:
   cu(u: ndarray, name: str, c: int, *t: int)
      u    : unitary numpy matrix
      name : Name of gate   
      c    : the control qubit
      *t    : the target qubits
```

The unitary matrix is of size $2^k \times 2^k$ for $k$ target qubits.

### CX (aka CNOT) Gate

The CX gate is a controlled version of the X gate. It is also known as the CNOT gate. It plays an important role in quantum algorithms.

<div style="text-align: center;">
<img src="assets/cx_gate.png" alt="cx_gate" width="80"/>
</div>

```
Exammple:
   qc.cx(0, 1)

API:
   cx(c: int, t: int)
      c : the control qubit
      t : the target qubit
```

### CY Gate

The CY gate is a controlled version of the Y gate. See the Y gate for further details.

<div style="text-align: center;">
<img src="assets/cy_gate.png" alt="cy_gate" width="80"/>
</div>

```
Example:
   qc.cy(0, 1)

API:
   cy(c: int, t: int)
      c : the control qubit
      t : the target qubit
```

### CZ Gate

The CZ gate is a controlled version of the Z gate. See the Z gate for further details.

<div style="text-align: center;">
<img src="assets/cz_gate.png" alt="cz_gate" width="80"/>
</div>

```
Example:
   qc.cz(0, 1)

API:
   cz(c: int, t: int)
      c : the control qubit
      t : the target qubit
```

### H Gate

The Hadamard (H) gate is an important gate in quantum computing because it can create a superposition from a basis state. It can also be used to switch between the Z basis and the X basis.

<div style="text-align: center;">
<img src="assets/h_gate.png" alt="h_gate" width="80"/>
</div>

```
Example:
  qc.h(0)

API:
   h(t: int)
      t : the target qubit
```

The H gate is described by the following matrix:

```math
H = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1 \\ 1 & -1 \end{bmatrix}
```

### I (aka ID) Gate

The I gate is the identity gate. The physical implementation in a quantum computer is simply 'do nothing'. Although it has no effect, it can be useful when analysing circuits. It is usually just drawn as a line, but may occasionally be made explicit as follows:

<div style="text-align: center;">
<img src="assets/i_gate.png" alt="i_gate" width="80"/>
</div>

```
Example:
   qc.i(0)

API:
   i(t: int)
      t : the target qubit
```

The I gate is described by the identity matrix:

```math
I = \begin{bmatrix}1 & 0 \\ 0 & 1 \end{bmatrix}
```

### P Gate

The phase gate P rotates the phase of a qubit around the Z axis in the Bloch sphere.

<div style="text-align: center;">
<img src="assets/p_gate.png" alt="p_gate" width="80"/>
</div>

The P gate is described by the following matrix:

```math
P(\phi) =\begin{bmatrix}1 & 0 \\ 0 & e^{i\phi} \end{bmatrix}
```

```
Example:
    qc.p(pi/2, f'{PI}/2', 0)

API:
   p(phi: float, label: str, t: int)
      phi   : the phase angle in radians
      label : text label for the angle
      t     : the target qubit
```

The first argument is the phase angle in radians. The second argument is the phase angle as a string. The phase angles are typically multiples of $\pi$, so it is convenient to use unicode $\pi$ in the text string.

When the phase gate is applied to a qubit $\alpha_0\ket{0} + \alpha_1\ket{1}$, the result is:

```math
\begin{bmatrix}1 & 0 \\ 0 & e^{i\phi} \end{bmatrix}\begin{bmatrix}\alpha_0 \\ \alpha_1 \end{bmatrix}=\begin{bmatrix}\alpha_0 \\ \alpha_1 e^{i\phi}\end{bmatrix}
```

Note that all the phase is applied to the $\ket{1}$ state. It is not necessary to apply separate phases to the two basis states as only the relative phase matters. The global phase does not affect the measurement outcome.

The following are special cases of the phase gate that have their own names as they are frequently used:

```math
\begin{align*}
Z &= P(\pi)\\[0.3em]
S &= P(\frac{\pi}{2})= \sqrt{Z}\\[0.3em]
T &= P(\frac{\pi}{4})= \sqrt{S}
\end{align*}
```

### RX Gate

The RX gate performs a rotation by 'theta' radians about the X axis of the Bloch Sphere.

<div style="text-align: center;">
<img src="assets/rx_gate.png" alt="rx_gate" width="80"/>
</div>

```
Example:
   qc.rx(pi/4, f'{PI}/4', 0)

API:
   rx(theta: float, t: int)
      theta : the angle in radians
      label : text label for the angle
      t     : the target qubit
```

The RX gate is described by the following matrix:

```math
RX(\theta) = \begin{bmatrix}
\cos(\frac{\theta}{2}) & -i\sin(\frac{\theta}{2}) \\
 -i \sin(\frac{\theta}{2}) & \cos(\frac{\theta}{2}) \end{bmatrix}
```

Note: RX($\pi$) and X differ by a global phase of $i$:

```math
RX(\pi) = \begin{bmatrix}
0 & -i \\ -i  & 0
\end{bmatrix}\quad\textrm{whereas}\quad
X = \begin{bmatrix}
0 & 1 \\ 1  & 0
\end{bmatrix}
```

Hence $X=i\,RX(\pi)$.

### RY Gate

The RY gate performs a rotation by 'theta' radians about the Y axis of the Bloch Sphere.

<div style="text-align: center;">
<img src="assets/ry_gate.png" alt="ry_gate" width="80"/>
</div>

```
Example:
   qc.ry(pi/4, f'{PI}/4', 0)

API:
   ry(theta: float, t: int)
      theta : the angle in radians
      label : text label for the angle
      t     : the target qubit
```

The RY gate is described by the following matrix:

```math
RY(\theta) =  \begin{bmatrix}
\cos(\frac{\theta}{2}) & -\sin(\frac{\theta}{2}) \\
 \sin(\frac{\theta}{2}) & \cos(\frac{\theta}{2}) \end{bmatrix}
```

Note: RY($\pi$) and Y differ by a global phase:

```math
RY(\pi) = \begin{bmatrix}
0 & -1 \\ 1  & 0
\end{bmatrix}\quad\textrm{whereas}\quad
Y = \begin{bmatrix}
0 & -i \\ i  & 0
\end{bmatrix}
```

Hence $Y=i\,RY(\pi)$.

### S Gate

The S gate performs a phase rotation by $\pi/2$ radians. It can be thought of as the square-root of the Z gate. Applying it twice is equivalent to a Z gate.

<div style="text-align: center;">
<img src="assets/s_gate.png" alt="s_gate" width="80"/>
</div>

```math
S=\sqrt{Z}
```

```
Example:
   qc.s(0)

API:
   s(t: int)
      t : the target qubit
```

The S gate is described by the following matrix:

```math
S =\begin{bmatrix}1 & 0 \\ 0 & i \end{bmatrix}
```

### Sdg Gate

The Sdg (S-dagger) $S^\dagger$ gate is the conjugate transpose of the S gate. It performs a phase rotation by $-\pi/2$ radians.

<div style="text-align: center;">
<img src="assets/sdg_gate.png" alt="sdg_gate" width="80"/>
</div>

```
Example:
   qc.sdg(0)

API:
   sdg(t: int)
      t : the target qubit
```

The Sdg gate is described by the following matrix:

```math
Sdg =\begin{bmatrix}1 & 0 \\ 0 & -i \end{bmatrix}
```

### SWAP Gate

The SWAP gate swaps the state of two qubits.

<div style="text-align: center;">
<img src="assets/swap_gate.png" alt="swap_gate" width="80"/>
</div>

```
Example:
   qc.swap(0, 1)

API:
   swap(c: int, t1: int, t2: int)
      t1 : the first target qubit
      t2 i: the second target qubit
```

The SWAP gate is described by the following matrix:

```math
SWAP =\begin{bmatrix}1&0&0&0 \\ 0&0&1&0 \\ 0&1&0&0 \\ 0&0&0&1 \end{bmatrix}
```

### SX (aka V, SQRTX) Gate

The SX gate can be thought of as the square-root of the X gate. Applying it twice is equivalent to an X gate:

<div style="text-align: center;">
<img src="assets/sx_gate.png" alt="sx_gate" width="80"/>
</div>

```math
SX=\sqrt{X}
```

```
Example:
   qc.sx(0)

API:
   sx(t: int)
     t : the target qubit
```

The SX gate is described by the following matrix:

```math
SX =\frac{1}{\sqrt{2}}\begin{bmatrix}1+i & 1-i \\ 1-i & 1+i \end{bmatrix}
```

Note that $V^\dagger$ is the other square-root of X.

### T Gate

The T gate performs a phase rotation by $\pi/4$ radians. It can be thought of as the square-root of the S gate. Applying it twice is equivalent to a S gate:

<div style="text-align: center;">
<img src="assets/t_gate.png" alt="t_gate" width="80"/>
</div>

```math
T = \sqrt{S}
```

```
Example:
   qc.t(0)

API:
   t(t1: int)
      t1 : the target qubit
```

The T gate is described by the following matrix:

```math
T =\begin{bmatrix}1 & 0 \\ 0 & e^{i\frac{\pi}{4}} \end{bmatrix}
```

Somewhat confusingly, the T gate is sometimes known as the $\pi/8$ gate. This because it can be written in a symmetrical form (up to global phase) as:

```math
T =\begin{bmatrix} e^{i\frac{\pi}{8}}& 0 \\ 0 & e^{i\frac{\pi}{8}} \end{bmatrix}
```

### Tdg Gate

The Tdg (T-dagger) $T^\dagger$ gate is the conjugate transpose of the T gate. It performs a phase rotation by $-\pi/4$ radians.

<div style="text-align: center;">
<img src="assets/tdg_gate.png" alt="tdg_gate" width="80"/>
</div>

```
Example:
   qc.tdg(0)

API:
   tdg(t: int)
      t : the target qubit
```

The Tdg gate is described by the following matrix:

```math
Tdg =\begin{bmatrix}1 & 0 \\ 0 & e^{-i\frac{\pi}{4}} \end{bmatrix}
```

### U Gate

The U gate takes a $2^N \times 2^N$ unitary matrix and applies it as an N-qubit gate. The simplest case is a single-qubit gate, which has a 2x2 matrix.

<div style="text-align: center;">
<img src="assets/u_gate.png" alt="u_gate" width="80"/>
</div>

```
Example:
   u = numpy.array([[0,1],[1,0]])
   qc.u(u, 'U', 0)
   
API:
   u(u: ndarray, name: str, *t: int)
      u    : unitary numpy matrix
      name : Name of gate   
      *t    : the target qubits
```

The unitary matrix is of size $2^k \times 2^k$ for $k$ target qubits.

### X (aka NOT) Gate

The X gate is the quantum NOT operator. It is a rotation by $\pi$ about the X axis of the Bloch sphere.

<div style="text-align: center;">
<img src="assets/x_gate.png" alt="x_gate" width="80"/>
</div>

```
Example:
   qc.x(0)

API:
   x(t: int)
      t : the target qubit
```

The X gate is described by the following matrix:

```math
X =\begin{bmatrix}0 & 1 \\ 1 & 0 \end{bmatrix}
```

### Y Gate

The Y gate It is a rotation by $\pi$ about the Y axis of the Bloch sphere.

<div style="text-align: center;">
<img src="assets/y_gate.png" alt="y_gate" width="80"/>
</div>

```
Example:
   qc.y(0)

API:
   y(t: int)
      t : the target qubit
```

The Y gate is described by the following matrix:

```math
Y = \begin{bmatrix}0 & -i \\ i & 0 \end{bmatrix}
```

### Z Gate

The Z gate It is a rotation by $\pi$ about the Z axis of the Bloch sphere.

<div style="text-align: center;">
<img src="assets/z_gate.png" alt="z_gate" width="80"/>
</div>

```
Example:
   qc.z(0)
   
API:
   z(t: int)
      t : the target qubit
```

The Z gate is described by the following matrix:

```math
Z =\begin{bmatrix}1&0 \\ 0&-1 \end{bmatrix}
```

## Non-Unitary Operations

This section covers circuit elements that are not considered to be quantum gates because they are not reversible unitary operations.

### Measure

The 'measure' operation performs a quantum measurement on one or more qubits.

<div style="text-align: center;">
<img src="assets/measure01.png" alt="measure01" width="80"/>
</div>

The use of 'measure' is discussed in the TinyQsim User Guide.

```
Example:
   qc.measure(0, 1)

API:
   measure(t1, t2, ... : int)
      t1, t2, ... : the qubits to be measured
```

If the argument list is left blank, then all qubits will be measured.

### Reset

The 'reset' operation resets a qubit to the $\ket{0}$ state.

<div style="text-align: center;">
<img src="assets/reset.png" alt="reset" width="80"/>
</div>

It is equivalent to a measurement of the qubit, followed by an X operation conditional on the measurement result being 1.

## Other Symbols

### Barrier

A barrier is drawn in the circuit as a vertical dotted line, like a fence separating sections of the circuit. Its main use is to prevent circuit optimizations crossing boundaries. This does not apply to TinyQsim since it currently does no circuit optimization. However, a barrier can still be useful for separating parts of the circuit for clarify, for example to separate initialization from processing.

<div style="text-align: center;">
<img src="assets/barrier.png" alt="barrier" width="80"/>
</div>

```
Example:
   qc.barrier()
   
API:
   barrier()
```
