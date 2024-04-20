## TinyQsim: Tiny Quantum Circuit Simulator

TinyQsim is a tiny quantum circuit simulator based on the quantum gate model.

<!-- TOC -->

* [TinyQsim: Tiny Quantum Circuit Simulator](#tinyqsim-tiny-quantum-circuit-simulator)
    * [Background](#background)
    * [Installation](#installation)
    * [Jupyter Notebooks](#jupyter-notebooks)
    * [Examples](#examples)
    * [Documentation](#documentation)
    * [License](#license)

<!-- TOC -->

### Background

The original version of the simulator was written during the first UK Covid-19 lockdown in 2020. The intention in writing it was to learn about quantum computation, rather than to produce a practical simulator. However, it is capable of running simple quantum algorithms with at least 10 qubits and up to 12 with a few seconds wait (on a Mac Mini M2).

### Installation

These instructions apply to macOS or Linux systems, although the software can also be installed on Windows.

It is recommended to install the software in a virtual environment, using an environment manager such as Conda:

```
  cd tinyqsim
  conda env create -f environment.yml
  conda activate tinyqsim
  conda update --all
  python setup.py install
```

Create a working directory on your computer for your own files. Then copy the TinyQsim examples folder there, so you have a copy to work with.

For example:

```
  mkdir mywork  # Not in the tinyqsim directory
  cd mywork
  cp -r <path_to_tinyqsim>/examples .
```

### Jupyter Notebooks

The example programs are in the form of Jupyter Notebooks. Notebooks provide a nice environment for experimenting with quantum algorithms. Documentation can be integrated with the code and include equations etc.

A notebook session can be started as follows:

```
  mkdir mywork
  conda activate tinyqsim
  jupyter notebook
```

Then navigate to the 'examples' folder.

### Documentation

The TinyQsim documentation can be viewed online on GitHub:

- https://github.com/jbrumf/tinyqsim/tree/main/doc/index.md

The Markdown files for the documentation can also be found in the `tinyqsim/doc` directory. These files require a Markdown viewer with LaTeX support.

### Examples

Examples are provided in the form of Jupyter notebooks. These are located in the `tinyqsim/examples` directory. Alternatively, a rendered version of the notebooks including their output can be found on GitHub:

- https://github.com/jbrumf/tinyqsim/tree/main/examples/

The current examples include:

- Example 1: Tutorial introduction to TinyQsim:
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_1.ipynb
- Example 2: 4-Qubit Quantum Fourier Transform
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_2.ipynb
- Example 3: Parameterized N-qubit QFT
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_3.ipynb

### License

MIT License (see the [LICENSE](LICENSE) file)






