# TinyQsim User Guide


### Contents

<!-- TOC -->

- [TinyQsim User Guide](#tinyqsim-user-guide)
    - [Contents](#contents)
  - [Getting Started](#getting-started)
    - [Introduction](#introduction)
    - [Installation](#installation)
    - [A Simple Example](#a-simple-example)
  - [Further Details](#further-details)
    - [Creating a Quantum Circuit](#creating-a-quantum-circuit)
    - [Building the Circuit](#building-the-circuit)
    - [Drawing the Circuit](#drawing-the-circuit)
      - [1: In a Jupyter Notebook](#1-in-a-jupyter-notebook)
      - [2: Run from a Python Script](#2-run-from-a-python-script)
    - [Labelling the Qubits](#labelling-the-qubits)
    - [Inspecting the State (without collapse)](#inspecting-the-state-without-collapse)
      - [Quantum State Vector](#quantum-state-vector)
      - [Components of State](#components-of-state)
      - [Probabilities](#probabilities)
      - [Measurement Counts](#measurement-counts)
    - [Quantum Measurement (with collapse)](#quantum-measurement-with-collapse)
      - [Measure](#measure)
      - [Reset](#reset)
    - [Bloch Sphere](#bloch-sphere)

<!-- TOC -->

----

## Getting Started

### Introduction

This guide provides a short introduction to using TinyQsim. The companion [TinyQsim Gates](TinyQsim_gates.md) Guide describes the circuit symbols and the different kinds of gates that can be used to build a quantum circuit.

The Jupyter notebooks in the 'examples' directory contain some more-detailed examples.

### Installation

TinyQsim can be downloaded from [https://github.com/jbrumf/tinyqsim](https://github.com/jbrumf/tinyqsim).

For installation instructions, see the README file in the source distribution.

Once the software is downloaded, see the API documentation:

- [TinyQSim API](api/index.html)

In particular, select the 'qcircuit' module to browse the documentation of the QCircuit class, through which you will interact with the simulator. It may be helpful to refer to this while reading the User Guide. 

### A Simple Example

We will start with a simple example that gives a brief overview of some of the main features of TinyQsim. Subsequent sections then look at these in more detail.

The examples in this document require the following Python imports:

```
from tinyqsim.qcircuit import QCircuit
import numpy as np
```

The main interface to the simulator is through the QCircuit class.

First, let us create a quantum circuit 'qc' with 2 qubits:

```
  qc = QCircuit(2)
```

Then add some quantum gates:

```
  qc.x(1)       # Add an X gate on qubit 1
  qc.h(0)       # Add an H gate on qubit 0
  qc.cx(0, 1)   # Add a CX gate on qubits 0 and 1
```

Next, draw the circuit:

```
  qc.draw()
```

<div style="text-align: center;">
<img src="assets/bell_1.png" alt="bell_1" height=120/>
</div>

The various symbols are explained in the companion [TinyQsim Gates Guide](TinyQsim_gates.md).

This circuit creates the entangled quantum state: $\frac{1}{\sqrt{2}}\ket{01} + \frac{1}{\sqrt{2}}\ket{10}$.

We can confirm this by printing the components of the quantum state:

```
  print(qc.components())
```
The output is in the form of a Python dictionary, with zero values omitted by default:

Output: {'01': (0.7071+0j), '10': (0.7071+0j)}

The probabilities of the different measurement outcomes are the squares of the absolute values:
```
  print(qc.probabilities())
```
Output: {'01': 0.5, '10': 0.5}

The probability distribution can be plotted as follows:

```
  qc.plot_probabilities()
```

<div style="text-align: center;">
<img src="assets/bell_probs.png" alt="bell_probs" width=350/>
</div>

With a real quantum computer, the only way to get a result is to perform a quantum measurement that collapses the state to one of the basis states. Probabilities are estimated by running the program many times and looking at the frequencies of the various outcomes.

With a simulation, we have direct access to the quantum state and can simply calculate the probabilities. Consequently, it is often not necessary to make collapse measurements.

However, if required, we can sample the probability distribution to see the kind of spread of counts we might get if we made quantum measurements and ran the experiment many times.

```
  qc.plot_counts(runs=1000)
```

<div style="text-align: center;">
<img src="assets/bell_counts.png" alt="bell_counts" width=350/>
</div>

Note that the counts on a real quantum computer may also fluctuate as a result of noise and decoherence, but these effects are not modelled by TinyQsim.

In its default mode, the plot_counts function does not re-execute measurements in the circuit, so it is assumed that this function is used *instead of* adding measurements to the circuit.

If collapse measurements are required, they can be performed by adding measurements to the circuit as follows:

```
  qc.measure()
  print(qc.results())
  qc.draw()
```
Output: {0:0, 1:1}

<div style="text-align: center;">
<img src="assets/bell_2.png" alt="bell_1" height=120/>
</div>

For more-complex examples, see the Jupyter notebooks in the 'examples' directory. 

---

## Further Details

The following sections provide some more detail on the functions introduced by the simple example above.

Documentation of the QCircuit API can be found in the [TinyQSim API](api/index.html). In particular, refer to the API of the QCircuit class in the 'qcircuit' submodule.

### Creating a Quantum Circuit

A quantum circuit is created using the QCircuit constructor. For example, to create a circuit with 2 qubits:

```
  qc = QCircuit(2)
```
See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

By default the quantum state is initialized to $\ket{00\dots 0}$. If a different initial state is required, it may be configured using quantum gates.

It is also possible to set the state using the `state_vector` property. The vector must have a norm of 1 and a length of $2^K$, where K is the number of qubits. For example:

```
  qc = QCircuit(2)
  qc.state_vector = np.array([0, 1, 0, 0])
```

The circuit can also be initialized with a random quantum state by using the following keyword argument:

```
  qc = QCircuit(2, init='random')
```

### Building the Circuit

The various gates and other components that can be used to build a quantum circuit are described in the [TinyQsim Gates](TinyQsim_gates.md) guide. This also explains the circuit symbols and several other matters relating to the use of gates.

The available gates include: CCU, CCX, CH, CP, CS, CSWAP, CT, CU, CX, CY, CZ, H, I, P, RX, RY, S, SDG, SWAP, SX, T, TDG, U, X, Y and Z. It is also possible to define custom gates, including ones with parameters and controls.

The Gates guide also describes other symbols including those for the 'barrier', 'measure' and 'reset' operations.

### Drawing the Circuit

The quantum circuit can be drawn using the QCircuit 'draw' method. The following are some examples of usage:
```
  qc.draw()
  qc.draw(show=False, save='image.png')
```

See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

If the circuit has a large number of gates, it may get reduced in size to fit in the window. The following sections explain how to zoom and pan the view.

#### 1: In a Jupyter Notebook

- Double click on the circuit in the notebook. This will zoom the circuit and display scroll bars.
- Then click on the area to the left of the qubit numbers. This will expand the view vertically so that all qubits are visible.
- If the circuit is too wide to fit in the window, the horizontal scroll bar can be used to explore the circuit.

#### 2: Run from a Python Script

If TinyQsim is run from a Python program, instead of from a notebook, the circuit will appear in a window with controls at the bottom for zooming and panning the view. A region can be zoomed into with the magnifier tool and then the view can be panned using the pan tool (which has 4 arrows).

### Labelling the Qubits

By default, the qubit lines in the schematic are labelled q0, q1, q2, etc. It is possible to add text to the labels as shown in the following example:

```
  KET0 = '|0\u27E9'
  
  qc = QCircuit(3)
  qc.qubit_labels({0: "Alice's qubit", 
                   1: "Bob's qubit",
                   2: KET0})
  qc.ccx(0,1,2)
  qc.draw()
```

<div style="text-align: center;">
<img src="assets/qubit_labels.png" alt="qubit_labels" height=180/>
</div>

The labels are defined as a Python dictionary. This need only contain entries for qubits that require a custom label. Other qubits will just get the default labels q0, q1,...

The example shows how the ket symbol $\ket{0}$ can be defined and used in a label.

### Inspecting the State (without collapse)

On a real quantum computer, it is not possible to examine the quantum state without collapsing it to one of the basis states of the measurement basis. Consequently, quantum algorithms usually end with a measurement of the quantum state, yielding the result as a classical state. The program is often run many times and the frequencies of the various outcomes are used to estimate their probabilities.

The situation is different with a quantum simulator like TinyQsim. We have direct access to the quantum state and can calculate the probabilities without performing any collapse measurements.

Four methods and properties are provided that allow you to access the state in different ways:

```
  qc.state_vector
  qc.components()
  qc.probabilities()
  qc.counts()
```

The 'state_vector' property returns a copy of the raw state vector as a numpy array. This is useful if you want to write some Python code to perform your own processing of the result.

However, for just examining the state, the other three methods may be more useful. These return the result as a Python dictionary with keys that are the labels of the basis states. By default, any elements that have probabilities close to zero are omitted to make the output easier to read.

The following subsections describe these methods in more detail.

#### Quantum State Vector

The quantum state vector can be accessed via a property of the quantum circuit. This returns a copy of the internal state as a numpy array.

For example:
```
  print(qc.state_vector)
```

Example output for state $\frac{1}{\sqrt{2}}\ket{01} + \frac{1}{\sqrt{2}}\ket{10}$ :

```
  [0. 0.70710678 0.70710678 0.]
```

It is often useful to format the state vector to make it more readable. This can be done using the numpy 'printoptions' context manager. 

For example, to print the state components to 4 decimal places:

```
 with np.printoptions(precision=4, suppress=True):
      print(qc.state_vector)
```

The state vector may have many thousands or millions of elements so, by default, only the first and last few are printed. This behaviour can be controlled as follows:

```
  with np.printoptions(threshold=100, edgeitems=10):
      print(qc.state_vector)
```

Alternatively, the whole state vector can be printed as follows:

```
  with np.printoptions(threshold=sys.maxsize):
      print(qc.state_vector)
```

The keywords have the following meanings:

- `suppress`  : Print in fixed-point notation
- `precision` : Set the number of decimal places
- `threshold` : Number of items that triggers summarization
- `edgeitems` : Number of array items to print at start/end of summarization

See the numpy 'printoptions' documentation for details and further options.

#### Components of State

The projection of the quantum state onto each basis vector can be obtained as follows. This is similar to just printing the state except that the result is in the form of a Python dictionary with keys that are the labels the basis states. This is not a measurement, so the state is not collapsed.

Examples:

```
  qc.components()
  qc.components(decimals=4)
  qc.components(include_zeros=True)
```

See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

Example output for state $\frac{1}{\sqrt{2}}\ket{01} + \frac{1}{\sqrt{2}}\ket{10}$ :

```
  {'01': (0.7071+0j), '10': (0.7071+0j)}
```

#### Probabilities

The probabilities of a measurement returning each of the basis states can be obtained as follows. This is not a measurement, so the state is not collapsed. 

The qubits to be considered are given as arguments. If they are omitted, all qubits are used.

Examples:
```
  qc.probabilities()
  qc.probabilities(1,2, decimals=3)
  qc.probabilities(1,2, include_zeros=True)
```

See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

Example output for state $\frac{1}{\sqrt{2}}\ket{01} + \frac{1}{\sqrt{2}}\ket{10}$ :

```    
  {'01': 0.5, '10': 0.5}
```

So, the probabilties of the measurement outcomes are:

```math
p(\ket{01}) = 0.5, \quad p(\ket{10})= 0.5
```

The 'probabilities' method is normally used *instead of* placing measurements at the end of the circuit. If it is used *after* output measurements, the state will have already been collapsed, so the result will be a single state with probability 1.0, if all the requested qubits have been measured. If only some have been measured, the probabilities returned will be the probabilities of the possible outcomes still remaining after the measurement.

Occasionally, a circuit may include a mid-circuit measurement or qubit reset operation. In this case, the probabilities are with respect to the initial outcome of the mid-circuit measurement. In this situation, it may be better to use the 'counts' method instead of 'probabilities', since this has an option to re-run the whole circuit.

In addition to the 'probabilities' method, which returns a dictionary, there is a similar 'plot_probabilities' method that plots the results as a histogram.

<div style="text-align: center;">
<img src="assets/bell_probs.png" alt="bell_probs" width=350/>
</div>

Examples:

```
  qc.plot_probabilities()
  qc.plot_probabilities(1,2)
  qc.plot_probabilities(save='probabilities.png')
```
See the QCircuit API documentation for further details.

#### Measurement Counts

The quantum state cannot be observed on a real quantum computer, so it is common to perform measurements at the end of the quantum circuit and run the program many times to find the frequency with which each outcome occurs. This provides an approximation to the true probabilities that improves as the number of test runs is increased.

TinyQsim provides the following method that simulates such a sequence of test runs and returns a dictionary of the counts for each basis state. It does not affect the state (except when the 'rerun' option is used). If you want the state to be updated, just follow it with a call to 'measure'.

The arguments specify the qubits to be measured. If they are omitted, all qubits are measured.

Examples:
```
  qc.counts()
  qc.counts(1,2)
  qc.counts(1,2, runs=500)
  qc.counts(1,2, rerun=True)
  qc.counts(1,2, include_zeros=True)
```

See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

Example output for state $\frac{1}{\sqrt{2}}\ket{01} + \frac{1}{\sqrt{2}}\ket{10}$ :

```
  {'01': 503, '10': 497}
```

Bu default, 'counts' simply computes the probability distribution for the various outcomes and takes multiple samples from that distribution. Like the probabilites method, it is intended to be used *instead of* placing measurements on the outputs of the circuit. This is sufficient if the circuit contains no (mid-circuit) measurement.

If mid-circuit measurements (or resets) are present, the option 'rerun=True' can be used to force re-execution of the whole circuit. This also works if there are measurements on the outputs.

If there are no measurements, then the default approach is faster as the circuit is only executed once. This may be important when the circuit has many qubits.

In addition to the 'counts' method, which returns a dictionary, there is a similar 'plot_counts' method that plots the results as a histogram.

<div style="text-align: center;">
<img src="assets/bell_counts.png" alt="bell_counts" width=350/>
</div>

Examples:
```
  qc.plot_counts()
  qc.plot_counts(1,2)
  qc.plot_counts(1,2, runs=500)
  qc.plot_counts(1,2, rerun=True)
  qc.plot_counts(save='counts.png')
```
See the QCircuit API documentation for further details.

### Quantum Measurement (with collapse)

#### Measure

A quantum measurement may be performed on one or more qubits. This collapses the state as it would on a real quantum computer. 

The arguments specify the qubits to be measured. If they are omitted, all qubits are measured.

Examples:
```
  print(qc.measure())       # Measure all qubits
  m0, m1 = qc.measure(0,1)  # Measure qubits 0 and 1
```

<div style="text-align: center;">
<img src="assets/measure01.png" alt="measure01" height="115"/>
</div>

See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

The 'measure' method returns the result of the measurement so that it can be printed or saved, as required.

#### Reset

The 'reset' operation resets a qubit to the $\ket{0}$ state. One application is to allow a qubit to be reused, which is useful since the maximum number of qubits available is quite limited. For example, ancilla qubits may no longer be needed once they have been used, so it may be possible to reset them and reuse them in a later part of the circuit.

Example:
```
  qc.reset(0)  # Reset qubit 0 to |0>
```
<div style="text-align: center;">
<img src="assets/reset.png" alt="reset" height="65"/>
</div>

See the qcircuit module in the API documentation for full details, including all parameters, options, types and defaults.

An alternative to a reset is to "uncompute" a qubit by executing the inverse of the preceding operations on the qubit in reverse order to return it to its initial state. This has the advantage that it is a proper unitary operation.

The behaviour of reset is equivalent to a measurement of the qubit followed by an X operation conditional on the measurement result being 1. This forces the qubit into the $\ket{0}$ state. Any other qubits that were entangled with the reset qubit are affected in the same way as if the reset were a measurment.

Although 'reset' effectively performs a measurement, it is not included in the output of the 'results' call. If this is needed, the 'reset' should be preceded by an explicit measurement.

### Bloch Sphere

A state of a qubit may be mapped onto a sphere, known as the Bloch sphere:

```math
\ket{\psi} = \cos(\frac{\theta}{2})\ket{0} + e^{i\phi} \sin(\frac{\theta}{2})\ket{1}
```

where $0 \le\theta\le\pi\,$ and $\,0\le\phi\le2\pi$.

<div style="text-align: center;">
<img src="assets/bloch.png" alt="bloch" width="300"/>
</div>

The Bloch sphere is mostly useful for single qubits because the qubits of a multi-qubit system can become *entangled* such that the qubits no longer have individual pure states. However, the sphere is a useful way to visualize and learn about the effects of single-qubit gates, which can then be used as part of a multi-qubit system.

The support for the Bloch Sphere in TinyQsim is at the prototype stage, so the details are likely to change. At present, it can display the Bloch sphere for a pair of angles, $\phi$ and $\theta$. For example:

```
  from tinyqsim.plot_bloch import plot_bloch
  phi = pi / 2
  theta = pi / 2
  plot_bloch(phi, theta)
```

The sphere can be rotated with the mouse when run from a Python program. When run from a Jupyter notebook, the orientation is fixed. However, the view point can be set using the optional parameters azimuth and elevation in degrees:

```
  plot_bloch(phi, theta, azimuth=35, elevation=10)
```

The following example shows how to create a one-qubit quantum circuit, use gates to configure the state and then plot the state on the Bloch sphere.

For example:

```
  from tinyqsim.bloch import plot_bloch, qubit_to_bloch

  qc = QCircuit(1)  # This must be 1 qubit
  qc.h(0)
  qc.p(pi/3, f'{PI}/3', 0)
  qc.draw()
  plot_bloch(*qubit_to_bloch(qc.state_vector))
```

<div style="text-align: center;">
<img src="assets/bloch_cct.png" alt="bloch_cct" height="65"/>
</div>

<div style="text-align: center;">
<img src="assets/bloch_sphere.png" alt="bloch_sphere" width="250"/>
</div>

The Hadamard gate rotates the state vector from its initial +Z direction $\ket{0}$ to the +X direction $\ket{+}$. Then the P($\pi$/3) gate rotates it by $\pi/3$ radians clockwise about the Z axis to the position shown by the red arrow.