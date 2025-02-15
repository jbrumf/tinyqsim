## TinyQsim Design Notes

This document provides some informal notes on the design of TinyQsim, as well as some ideas for further development.

<!-- TOC -->

- [TinyQsim Design Notes](#tinyqsim-design-notes)
  - [Introduction](#introduction)
  - [Simulation](#simulation)
  - [Performance](#performance)
  - [Endianness](#endianness)
  - [Software Modules](#software-modules)

<!-- TOC -->


### Introduction

TinyQsim was originally started as a fun project to learn about quantum computation and as a framework to explore new ideas. The aim was to 'keep it simple', rather than worrying about optimization. Nevertheless, it is capable of simulating a 20-qubit Quantum Fourier Transform in about one second. This is sufficient for most textbook examples.

The software is intended as a tool for interactive experiments. It is written in Python, using Jupyter notebooks as an environment for interaction. TinyQsim works in an incremental fashion by executing each gate as it is added to the circuit, so that the state is always up to date. This makes it very easy to examine the state, probabilities, etc, at any time, without having to run a simulator on the model each time. This is very convenient for interactive use, but limits the scope for circuit optimization. However, there is an experimental deferred-execution mode that allows a circuit to be constructed before it is run.

### Simulation

When a new instance of QCircuit is created, the quantum state is initialized to the all-zero state $\ket{000\dots 0}$. Executing a quantum circuit just involves applying each gate in the circuit in turn to the quantum state as a unitary operator.

TinyQsim represents the quantum state internally as a tensor, represented by a multi-dimensional array with one dimension per qubit, with each tensor subscript corresponding to a dimension. This is much more efficient than applying matrices to a state vector. It allows gates, which are also represented as tensors, to be applied to specific qubits of the state. However, the state is presented to the user as a normal state vector by the QCircuit API.

For example, consider the following circuit:

<div style="text-align: center;">
<img src="assets_dnotes/circuit.png" alt="QFT_benchmark" width="80"/>
</div>

The 2-qubit unitary CX gate, which we will represent by the tensor $U$, is applied to qubits (3,1) of a 4-qubit quantum state $S$. This can be expressed in Einstein summation notation as the tensor contraction:

$\qquad U_{ijdb}\,S_{abcd}\,\rightarrow S_{ajci}$

The Python implementation can do this using the numpy 'einsum' fuction as follows:

```
  s = einsum('ijdb,abcd->ajci', u, s)
```

Numpy implements multi-dimensional arrays as 'strided' arrays. The internal data structure is a one-dimensional array with a separate small 'stride' array that holds the step size between elements for each dimension. The order of dimensions (e.g. qubits) may be permuted simply by permuting the strides, without altering the data array. The same one-dimensional data-array may have multiple 'views' each with its own stride array.

Consequently, the state-vector and tensor representations of the state can share the same data array, simply by creating a new view. A unitary operator may be applied to the required qubits specified by tensor indices, making use of the strides array.

For example, a tensor view 't' of an n-qubit state vector 's' can be created as follows:

```
   t = s.reshape([2] * n)
```

Similarly, a tensor view 'u' of a k-qubit unitary matrix 'm', representing a quantum operator, can be created as follows':
```
   u = m.reshape([2] * k * 2)
```   

TinyQsim also uses 'einsum' to construct a unitary-matrix representation of a quantum circuit. It is also used to calculate measurement probabilities for a subset of qubits by summing over the remaining qubits.

### Performance

The following graph shows the execution time of a Quantum Fourier Transform (QFT) plotted against the numbers of qubits. The time axis is logarithmic, so a straight line corresponds to a time complexity that is exponential in the number of qubits.

The test was run on a Mac Mini M2 Pro with 32GB of RAM, starting with a random N-qubit state for each run. The times are for execution of the QFT algorithm, excluding the initialisation of the random state.

<div style="text-align: center;">
<img src="assets_dnotes/TinyQsim_benchmark.png" alt="QFT_benchmark" width="550"/>
</div>

The green plot shows the time taken for a one-qubit QFT (which is just a single Hadamard gate) on the most-significant qubit. This provides a baseline against which to compare an N-qubit QFT. Although the Hadamard gate is only applied to one qubit, it will normally change all elements of the state vector. Hence the time complexity is of order $\mathcal{O}(2^N)$. The plot shows that the actual execution time increases by a factor of 2.12 for each qubit that is added.

The approximate time to run a given algorithm will be this baseline time multiplied by the number of qubits in the circuit, if run on the same computer, assuming simple one or two qubit gates.

The blue plot shows the execution time for an N-qubit QFT operating on the full N-qubit state. The QFT algorithm has a complexity of $\mathcal{O}(N^2)$ gates. On a real quantum computer, this is also the time complexity if it is assumed that the different gates take equal times. However, in the simulation, the time taken per gate approximately doubles for each qubit, so the overall time complexity is expected to be $\mathcal{O}(N^2\ 2^N) \approx \mathcal{O}(2^N)$.

In conclusion, the simulator is quite responsive for interactive use with up to 20 qubits. However, with 28 qubits a QFT of all the qubits takes around 1000 seconds. Of course, these figures depend on the processor's performance and memory available.

There are a number of ways in which the performance could be further improved, but an initial design goal of TinyQsim was to keep it simple.

### Endianness

Some books, papers and online resources use the *big-endian* convention in which qubit 0 is the most-significant qubit, while others use the *little-endian* convention, in which qubit 0 is the least significant qubit. This can lead to confusion when comparing examples from different sources.

The big-endian convention was chosen for TinyQsim as it is popular in books and published papers.

### Software Modules

The Python software modules are as follows:

| Module    | Purpose                                             | 
|:----------|:----------------------------------------------------|
| qcircuit  | User API for a quantum circuit                      |
| quantum   | Functions for quantum operations                    |       
| gates     | Gates defined as unitary matrices                   |
| model     | Model of a quantum circuit                          |
| simulator | Simulation of state evolution                       |
| unitary_sim | Creates unitary matrix from circuit model         |
| schematic | Graphics for drawing quantum circuits               |
| plotting  | Functions for plotting histograms etc               |
| bloch     | Graphics for Bloch sphere                           |
| format    | Formatting of data for display                      |
| utils     | General utility functions                           |

QCircuit is an API wrapper that presents the quantum circuit to the user as an object. Most of the actual functionality is in the other modules.
