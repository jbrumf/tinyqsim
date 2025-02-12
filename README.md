## TinyQsim: Tiny Quantum Circuit Simulator

TinyQsim is a tiny quantum circuit simulator based on the quantum gate model.

Note: TinyQSim should not be confused with the Tiny-Q project that has subsequently appeared in the PyPI software repository with the name TinyQSim. The two are not related.

---

<!-- TOC -->

- [TinyQsim: Tiny Quantum Circuit Simulator](#tinyqsim-tiny-quantum-circuit-simulator)
  - [Overview](#overview)
  - [Documentation and Examples](#documentation-and-examples)
  - [Installation](#installation)
  - [Jupyter Notebooks](#jupyter-notebooks)
  - [Known Issues](#known-issues)
  - [Release Notes](#release-notes)
  - [License](#license)

<!-- TOC -->

### Overview

TinyQsim was originally started as a fun project to learn about quantum computation and as a framework to explore new ideas. The aim was to 'keep it simple', rather than worrying about optimization. Nevertheless, it is capable of simulating a 20-qubit Quantum Fourier Transform in about one second (tested on a Mac Mini M2). This should make it sufficient for most textbook examples and learning about quantum computing.

### Documentation and Examples

The TinyQsim documentation and examples can be found at:

- [https://jbrumf.github.io/tinyqsim/](https://jbrumf.github.io/tinyqsim/)

### Installation

These instructions apply to macOS and Linux systems, but the software should also run on Windows.

First, download TinyQSim using the "Code" button on the GitHub page:

- https://github.com/jbrumf/tinyqsim
 
The resulting folder will be called tinyqsim or tinyqsim-main.

It is recommended to install the software in a virtual environment, using an environment manager such as Conda or venv.

For example, to create and activate a Python virtual environment using conda:

```
  conda create -n tinyqsim python=3.12
  conda activate tinyqsim
```

Then install tinyqsim in that environment:

```
  cd tinyqsim  # The downloaded folder
  pip install .
```

Create a working directory somewhere on your computer for your own files (e.g. Jupyter notebooks). For example:

```
  mkdir mywork  # Not in the tinyqsim directory
```

### Jupyter Notebooks

The example programs are in the form of Jupyter Notebooks. These provide a nice environment for experimenting with quantum algorithms. Documentation can be integrated with the code and include equations etc.

A notebook session can be started as follows:

```
  cd mywork
  conda activate tinyqsim
  jupyter notebook
```

If you wish to run the notebooks in the `examples` folder, it is suggested that you first copy them to the `mywork` folder, so that you can experiment with them without modifying the original downloaded copy.

The examples are also included in the documentation, so that they can be browsed without installing the software or running a Jupyter server.

### Known Issues

**1: Warning Messages on macOS Sequoia**

On macOS Sequoia, the following warning messages may appear when drawing circuits and plots from a Python script:
```
python[70884:21253510] +[IMKClient subclass]: chose IMKClient_Modern
python[70884:21253510] +[IMKInputSession subclass]: chose IMKInputSession_Modern
```

This appears to be a problem with macOS Sequoia as other software is also affected.

### Release Notes

See the companion [RELEASE_NOTES.md](RELEASE_NOTES.md) file for information on recent changes.

### License

MIT License (see the [LICENSE](LICENSE) file)
