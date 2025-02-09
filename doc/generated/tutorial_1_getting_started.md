$\newcommand{\bra}[1]{\left\langle{#1}\right|}
\newcommand{\ket}[1]{\left|{#1}\right\rangle}$

## Tutorial 1: Getting Started with TinyQsim

### Contents

- [Tutorial 1: Getting Started with TinyQsim](#tutorial-1-getting-started-with-tinyqsim)
  - [Contents](#contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [A Simple Example](#a-simple-example)
  - [Probabilities](#probabilities)
  - [Measurements](#measurements)
  - [Unitary Matrix](#unitary-matrix)
  - [Bloch Sphere](#bloch-sphere)
  - [Summary](#summary)

### Introduction

This Getting Started tutorial provides a quick introduction to TinyQsim through the use of a simple example.

TinyQsim is a quantum circuit simulator based on the quantum gate model. A 20-qubit Quantum Fourier Transform (QFT) takes about one second (running on a Mac Mini M2 Pro). The software is capable of simulating quantum circuits up to a maximum of 26 qubits, although this may take a couple of minutes, depending on the quantum circuit and computer.

TinyQsim is a Python library that is intended to be called from a Jupyter notebook. Notebooks provide a nice environment for experimenting with quantum algorithms and documenting them since they can contain executable code, together with its graphical output, as well as documentation including equations in LaTeX. This Getting Started guide is itself written in the form of a notebook.

The tutorials are provided as both Jupyter '.ipynb' notebook files and as '.md' Markdown files. The latter makes it possible to read the documentation without running a Jupyter server.

### Installation

TinyQsim can be downloaded from [https://github.com/jbrumf/tinyqsim](https://github.com/jbrumf/tinyqsim).

For installation instructions, see the README.md file in the source distribution.

### Documentation

Once the software is downloaded, see the API documentation in the 'doc/api' directory. In particular, browse the API of the 'qcircuit' module to familiarise yourself with the QCircuit class which provides the main interface to the simulator. The API documentation provides further information on the available methods and their arguments, options, defaults and types. It will be helpful to refer to this while reading tutorials.

- Tutorial 1 (this tutorial) is a Getting Started guide that provides a quick overview.
- Tutorial 2 looks at the features of TinyQsim in more detail.
- Tutorial 3 describes all the gates provided as well as custom gates.
- Tutorial 4 describes the low-level API, which is not normally needed

There are also a number of other notebooks providing more complex examples such as the Quantum Fourier Transform (QFT) and Quantum Phase Estimation (QPE).

### A Simple Example

The first step is to import the QCircuit class:


```python
from tinyqsim.qcircuit import QCircuit
```

For the example, we will create a 2-qubit quantum circuit 'qc' that creates an entangled state:


```python
qc = QCircuit(2)
```

The state is initialized to $\ket{00}$ by default, which we can confirm by printing it. The coefficient '1' is the associated complex amplitude.


```python
qc.display_state()
```


$\displaystyle 1\ \ket{00}$


Next, we will add some quantum gates:


```python
qc.x(1)  # Add an X gate on qubit 1
qc.h(0)  # Add an H gate on qubit 0
qc.cx(0, 1)  # Add a CX gate on qubits 0 and 1
```

Then we can draw the circuit:


```python
qc.draw()
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_18_0.png)
    


By default, the gates are executed as they are added to the circuit, so there is no need to run the simulator explicitly and we can print the state at any time.

The various symbols and gates in the circuit diagram are explained in tutorial 3. This example has a Hadamard (H) gate, a NOT (X) gate and controlled-NOT (CX) gate. It creates the following entangled state:

$\ket{\psi}=\frac{1}{\sqrt{2}}\ket{01} + \frac{1}{\sqrt{2}}\ket{10}$

We can confirm this by displaying the state:


```python
qc.display_state()
```


$\displaystyle 0.70711\ \ket{01} + 0.70711\ \ket{10}$


The 'display_state' method displays the state using LaTeX for use in a Jupyter notebook. A LaTeX prefix can be included if required.
For example:


```python
qc.display_state(prefix=r'\ket{\psi} = ')
```


$\displaystyle \ket{\psi} = 0.70711\ \ket{01} + 0.70711\ \ket{10}$


The format may be customised in various ways as shown in the following examples:


```python
qc.display_state(decimals=4, include_zeros=False, trim=True)
qc.display_state(decimals=4, include_zeros=True, trim=True)
qc.display_state(decimals=4, include_zeros=True, trim=False)
```


$\displaystyle 0.7071\ \ket{01} + 0.7071\ \ket{10}$



$\displaystyle 0\ \ket{00} + 0.7071\ \ket{01} + 0.7071\ \ket{10} + 0\ \ket{11}$



$\displaystyle 0.0000\ \ket{00} + 0.7071\ \ket{01} + 0.7071\ \ket{10} + 0.0000\ \ket{11}$


It is also possible to format the state as plain text using 'format_state' instead of 'display_state'. This is useful when using TinyQsim from a Python script instead of from a Jupyter notebook.


```python
print(qc.format_state())
```

    0.70711|01⟩ + 0.70711|10⟩


Once the output is longer than a few lines, the 'sum-of-kets' notation becomes hard to read. It is then better to display the results as a table, using the 'table' option (This option is not currently supported by 'display_state').


```python
print(qc.format_state('table', include_zeros=True))
```

    |00⟩  0
    |01⟩  0.70711
    |10⟩  0.70711
    |11⟩  0


The raw state vector is available from the 'state_vector' property as a numpy array:


```python
qc.state_vector
```




    array([0.        , 0.70710678, 0.70710678, 0.        ])



### Probabilities

The probabilities of different measurement outcomes are the squares of the absolute values of the amplitudes of the state components:


```python
qc.probability_array()
```




    array([0. , 0.5, 0.5, 0. ])



It is convenient to display the probabilities along with the ket labels of the associated basis states using the 'format_probabilities' method. This method should be called in a 'print' statement to ensure proper formatting. 


```python
print(qc.format_probabilities())
```

    |01⟩  0.5
    |10⟩  0.5



```python
print(qc.format_probabilities(decimals=3, include_zeros=True))
```

    |00⟩  0
    |01⟩  0.5
    |10⟩  0.5
    |11⟩  0


The probability distribution can be plotted as follows:


```python
qc.plot_probabilities()
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_39_0.png)
    


The 'format_probabilities' and 'plot_probabilities' methods are intended for use with circuits that do *not* contain any measurement operations, since these would collapse the state. The probabilities tell us the probabilities of different outcomes if we were to perform a measurement, but it does not perform a measurement so there is no collapse.

### Measurements

A real quantum computer does not allow us to see the quantum state. Measuring the state causes it to collapse to one of the basis states according to the probabilities shown above. If we want to estimate the probabilities on a quantum computer, we have to run the circuit many times and look at the frequency of different outcomes.

With a simulator, we have the advantage that we have access to the state and can directly calculate the probabilities of different measurement outcomes without actually performing a measurement. This provides a useful performance improvement when we don't actually need measurements.

We can simulate this probabilistic outcome using the 'counts' or 'plot_counts' methods. For example:


```python
qc.plot_counts(runs=1000)
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_43_0.png)
    



```python
qc.counts(runs=1000)
```




    {'01': 527, '10': 473}



If we call 'counts' or 'plot_counts' again, it simulates another 1000 runs, so the counts are likely to be different:


```python
qc.counts(runs=1000)
```




    {'01': 491, '10': 509}



The default mode of 'counts' is to resample the probability distribution from a single run. This is suitable when the circuit contains no measurements. This is much more efficient than running the circuit many times and can be an important consideration for circuits containing more than a few qubits.

If we want to simulate measurements that collapse the state, we must add measurement operations to the quantum circuit as follows:


```python
qc.measure()
qc.draw()
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_49_0.png)
    


If we display the state after the measurements, it will have collapsed to either $\ket{01}$ or $\ket{10}$:


```python
qc.display_state()
```


$\displaystyle 1\ \ket{01}$


The 'counts' or 'plot_counts' methods can be called using the 'repeat' or 'measure' mode so that they actually run the circuit many times to generate measurement counts, rather than just resampling the output state of a single run. The difference between 'repeat' and 'measure' is discussed in the next tutorial. For this simple example, either can be used.


```python
qc.plot_counts(mode='measure', runs=1000)
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_53_0.png)
    


### Unitary Matrix

Individual quantum gates implement unitary operators expressed as unitary matrices. Complete circuits built from gates can also be expressed as a unitary matrix, provided that the circuit contains no measurement operations.

It is sometimes useful to get the unitary matrix corresponding to a circuit. The matrix can become very large if there are many qubits, so this is mostly of interest for simple circuits of a few qubits.


```python
qc = QCircuit(2)
qc.x(1)
qc.h(0)
qc.cx(0, 1)
qc.draw()
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_56_0.png)
    



```python
u = qc.to_unitary()
print(u)
```

    [[ 0.          0.70710678  0.          0.70710678]
     [ 0.70710678  0.          0.70710678  0.        ]
     [ 0.70710678  0.         -0.70710678  0.        ]
     [ 0.          0.70710678  0.         -0.70710678]]


### Bloch Sphere

TinyQsim allows the state of a single qubit to be plotted on the Bloch sphere:


```python
from tinyqsim.bloch import plot_bloch

qc1 = QCircuit(1)  # This must be 1 qubit
qc1.h(0)
qc1.t(0)
qc1.draw()
qc1.display_state()
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_60_0.png)
    



$\displaystyle 0.70711\ \ket{0} + (0.5+0.5j)\ \ket{1}$


The state vector is plotted in red:


```python
plot_bloch(qc1.state_vector, scale=1.0)
```


    
![png](tutorial_1_getting_started_files/tutorial_1_getting_started_62_0.png)
    


### Summary

This has been a quick introduction to TinyQsim. The next notebook goes into the various features in more detail. The API documentation, particularly of the QCircuit class, provides further details of all the methods including their arguments and defaults.
