## TinyQsim Release Notes

### Release Note (15 May 2025)

- Added support for multiple instantiation of single-qubit gates, applied to a list of qubits
- Updated Tutorials 2 & 3 to include multiple instatiation of gates
- plot_probabilities has a new 'ylim' option
- Added new section to Tutorial 2 on the use of registers
- Updated Example 4 to use multiple instantiation
- Added Example 5: Grover's Algorithm

---

### Release Notes (19 March 2025)

- Moved Quantum Computing Basics document to a new project as it is of more general applicability:
  - https://github.com/jbrumf/qc_basics
  - https://jbrumf.github.io/qc_basics/Quantum_computing_basics.html

---

### Release Notes (25 February 2025)

- Added gates: RZ, CRX, CRY, CRZ
- Added prototype code to export circuit as OpenQASM-3
- Added new functions to quantum module:
  - swap_vector_endianness, swap_unitary_endianness
- Documentation:
  - Updated TinyQsim Design Notes
  - Updated Guide to Gates document 

--- 

### Release Notes (21 February 2025)

- Increased maximum number of qubits
- Rewrote much of the Design Notes document
- Added new sections to Quantum Computing Basics document
- Corrections to Low-Level API doc and tutorial 2

---

### Release Notes (14 February 2025)

- A change has been made to the numbering of gate arguments shown in the gate symbol of custom gates. These now include control qubits in the count. This change only affects the graphics, not the behaviour of the gates.

- Minor corrections and updates to documentation.

---

### Release Notes (12 February 2025)

#### Changes to QCircuit Class

- A 'to_unitary' method has been added to QCircuit to return the unitary matrix of a circuit.

- A 'basis_names' method has been added to QCircuit which returns an array of the names (i.e. labels) of the basis states.

Some API changes have been made to create a cleaner separation of concerns between data content and presentation. This includes some new formatting options.

  - The 'components' method has been replaced by 'format_state'.

  - The 'probabilities' method has been replaced the following methods:
    - format_probabilities()
    - probability_dict()
    - probability_array()

#### Documentation and Examples

The documentation was previously in the form of Markdown files. This led to some compatibility issues with different Markdown viewers and tools, particularly where there was embedded LaTeX. Consequently, the documentation has been converted into HTML and placed on GitHub Pages:

- [https://jbrumf.github.io/tinyqsim/](https://jbrumf.github.io/tinyqsim/)

There was previously a lot of overlap and unnecessary duplication between the Markdown documentation and Jupyter notebook examples. This resulted in extra work maintaining two versions.

The master copy of the tutorials and examples are now in the form of Jupyter notebooks in the 'examples' directory. This has the benefit that errors in the example code are more easily detected as they are actually executed. HTML files are generated from the notebooks for inclusion in the documentation.

#### Other Updates

- Numpy was recently upgraded to version 2. Numpy arrays now print with the type of each element prefixing the scalar values. This made the output from some the TinyQsim methods difficult to read, so some changes were needed to the code.

- The documentation, examples and test-cases have been updated to reflect the above changes.
