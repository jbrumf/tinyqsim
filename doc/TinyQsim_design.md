## TinyQsim Design

This document provides some informal notes on the background and design of TinyQsim, as well as some ideas for further development.

<!-- TOC -->

- [TinyQsim Design](#tinyqsim-design)
    - [Background](#background)
    - [Endianness](#endianness)
    - [Execution Model](#execution-model)
    - [Simulation](#simulation)
    - [Software Modules](#software-modules)
    - [Matrix Expansion](#matrix-expansion)
    - [Qubit Permutation](#qubit-permutation)
    - [The Future](#the-future)

<!-- TOC -->

### Background

TinyQsim was originally started as a fun project during the first Covid lockdown, with the aim of learning about quantum computation. I have often found that writing code to simulate something is a good way to learn about it. Coding the ideas forces you to explore many subtle details, resulting in a deeper understanding. It's a bit like the way you really only get to properly understand maths by trying to solve problems, not just by reading a book or attending a lecture.

The aim was to 'keep it simple', rather than worrying about optimization. Nevertheless, TinyQsim is capable of simulating a 12-qubit Quantum Fourier Transform in a few seconds.

Because the code is simple, it should be easy to modify, providing a basis for experiments with new ideas, such as alternative quantum programming paradigms.

### Endianness

Some books, papers and online resources use the
*big-endian* convention in which qubit 0 is the most-significant qubit, while others use the
*little-endian* convention, in which qubit 0 is the least significant qubit. This can lead to confusion when comparing examples from different sources.

The big-endian convention was chosen for TinyQsim as it was easier to try out examples from the books I was reading at the time. It should not be too difficult to add an option for selecting big or little endian mode. The internal quantum measurement code already makes provision for it.

Single-qubit gates and the 2-qubit SWAP gate are the same for both endiannesses. Controlled gates differ according to endianness but the controlled vesions are all created using the function 'cu(u)' in the 'gates' module, so support for endian-selection of gates can all be done in one place.

It is envisaged that there could be an optional 'endian' argument for the QCircuit constructor to specify the endianness:

```
  qc = QCircuit(6, endian='little')
```

### Execution Model

TinyQsim is intended as a tool for interactive experiments. It is written in Python, with Jupyter notebooks providing a nice environment for interaction. TinyQsim works in an incremental fashion by executing each gate as it is added, so that the state is always up to date. This makes it very easy to examine the state, probabilities, etc, at any time, without having to run a simulator on the model each time. It is very convenient for interactive use, but it limits the scope for circuit optimization.

```
  qc = QCircuit(8)
  ...  Add gates
  print(qc.state_vector)
```

An alternative approach, used by some quantum development tools, is to first construct a complete circuit, then compile it with optimization for execution on a simulator or real quantum computer.

TinyQsim has adopted a hybrid approach. Gates are added to the circuit model but, by default, are applied to the state as they are added. (The model is also used as input for drawing the circuit schematic.) However, as an experimental feature, it is also possible to inhibit incremental execution and instead give an explict 'execute' command, which could potentially include optimization. It is envisaged that a circuit could be developed in incremental mode and then run with a larger number of qubits in explicit execution mode.

```
  qc = QCircuit(8, auto_exec=False)
  ...  Add gates
  qc.execute()
  print(qc.state_vector)
```

The execute command would typically be given after defining the circuit, but it can be given at any time, in which case it could either optimize and execute the whole circuit up to that point, or it could just optimize and run the commands added since the previous execute command.

Another possibility would be for the execute command to be triggered implicitly whenever the user gives a command that requires the state vector. This would allow optimization without the need for explicit execute commands.

```
  qc = QCircuit(8, auto_exec=False)  # Incremental mode disabled
  ...  Add gates
  print(qc.state_vector)  # Triggers execution
  ...  Add more gates
  print(qc.state_vector)  # Triggers execution
```

The execute command has no real use at the moment as there is no optimization, but it provides an architectural placeholder for further work.

### Simulation

TinyQsim starts by creating an initial quantum state vector of size $2^K$ for a $K$-qubit circuit. Then, as each gate is added, the gate's unitary matrix is expanded to a $2^K\times 2^K$ matrix that maps the gate onto the relevant qubits. The state is then updated by multiplying it by the matrix. This is obviously very inefficient but it is satisfactoryfor up to about 12 qubits.

Using this approach, every application of even a one-qubit gate requires expanding it to a $2^K\times 2^K$ matrix. For example, a 10-qubit circuit requires a $2^{10}\times 2^{10}$ matrix of complex numbers. A complex number requires two floating-point numbers that are typically 64 bits, so the total size of the matrix is 16 MB. This starts to get slow by the time we reach 12-qubit circuits with 256 MB matrices.

Using the circuit-model approach, the quantum circuit could, for example, be modelled by a Directed Acyclic Graph (DAG) representing the partial order of operations. Rewrite rules could, for example, be applied to simplify and combine elements building up progressively larger matrices. The size of the matrix increases by a factor 4 for each qubit that is added, so there is an advantage in combining smaller sub-circuits in a bottom-up manner.

### Software Modules

The main software modules are as follows:

| Module    | Purpose                                             | 
|:----------|:----------------------------------------------------|
| qcircuit  | API wrapper to present circuit as an object         |
| quantum   | Most of the quantum computations                    |       
| gates     | Definitions of basic gates as unitary matrices      |
| model     | Model of circuit (currently just a list of gates)   |
| schematic | Graphics for drawing quantum circuit                |
| simulator | Execution of model or just single commands          |
| utils     | Utility functions that are not specific to TinyQsim |
| bloch     | Prototype graphics for Bloch sphere                 |

QCircuit is an API wrapper that presents the quantum circuit to the user as an object. Most of the actual functionality is in the other modules. This decoupling allows the possibility of alternative user interfaces etc.

### Matrix Expansion

To apply a K-qubit gate (i.e. $2^K\times 2^K$ unitary matrix $U$) to an N-qubit quantum state (i.e. $2^N$ vector of complex numbers) $\ket{\psi}$, it is necessary to expand the gate to $N$ qubits.

First, consider the simple case that the gate is applied to $K$ consecutive qubits, starting at qubit 'q'.

```math
M = I^{\otimes q} \otimes U \otimes I^{\otimes (N - q - K)}
```

where $\otimes$ denotes the tensor product.

The tensor product of $n$ identical states $\ket{\psi}$ is written as a *tensor power*. For example:

```math
\qquad\ket{\psi}^{\otimes n}=\ket{\psi}\otimes\dots\otimes\ket{\psi}
```

### Qubit Permutation

In practice, the gate may be applied to non-consecutive qubits which may not even be in the same order. TinyQsim simply expands the matrix, as described above and performs a quantum permutation on the gate qubits.

These approaches to applying a gate's unitary matrix to a quantum state are very-non-optimal, but easy to implement, following the 'keep it simple' approach. In fact, it works surprisingly well, allowing circuits of up to about 12 qubits.

There is a lot of scope for optimization and improvement, but this was not the goal of the Tiny Quantum Simulator.

### The Future

TinyQsim was originally written as a learning exercise. Although there many other much-better quantum simulators available that I could use, I may occasionally add some new features to TinyQsim because it has been a fun project.
