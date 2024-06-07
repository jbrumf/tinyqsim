## TinyQsim: Tiny Quantum Circuit Simulator

TinyQsim is a tiny quantum circuit simulator based on the quantum gate model.

<!-- TOC -->

- [TinyQsim: Tiny Quantum Circuit Simulator](#tinyqsim-tiny-quantum-circuit-simulator)
  - [Overview](#overview)
  - [Installation](#installation)
  - [Jupyter Notebooks](#jupyter-notebooks)
  - [Documentation](#documentation)
  - [Examples](#examples)
  - [License](#license)

<!-- TOC -->

### Overview

TinyQsim was originally started as a fun project to learn about quantum computation and as a framework to explore new ideas. The aim was to 'keep it simple', rather than worrying about optimization. Nevertheless, it is capable of simulating a 20-qubit Quantum Fourier Transform in about one second (tested on a Mac Mini M2). This is sufficient for most textbook examples.

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
  cd mywork
  conda activate tinyqsim
  jupyter notebook
```

Then navigate to the 'examples' folder.

### Documentation

The TinyQsim documentation can be viewed online on GitHub:

- https://github.com/jbrumf/tinyqsim/tree/main/doc/index.md

The Markdown files for the documentation can also be found in the `tinyqsim/doc` directory. These files require a Markdown viewer with LaTeX support.

API document is located in the `tinyqsim/doc/api` directory. This cannot be viewed on GitHub as GitHub does not render HTML pages. Instead, open your downloaded copy of `tinyqsim/doc/api/index.html` in a browser. 

### Examples

Examples are provided in the form of Jupyter notebooks. These are located in the `tinyqsim/examples` directory. Alternatively, a rendered version of the notebooks including their output can be found on GitHub:

- https://github.com/jbrumf/tinyqsim/tree/main/examples/

The examples currently include:

- Example 1: Tutorial introduction to TinyQsim:
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_1_tutorial.ipynb
- Example 2: 4-Qubit Quantum Fourier Transform
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_2_QFT4.ipynb
- Example 3: Parameterized N-qubit QFT
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_3_QFT.ipynb
- Example 4: Quantum Phase Estimation
    - https://github.com/jbrumf/tinyqsim/blob/main/examples/example_4_QPE.ipynb

### License

MIT License (see the [LICENSE](LICENSE) file)






