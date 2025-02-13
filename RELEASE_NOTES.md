## Release Notes (14 February 2025)

- A change has been made to the numbering of gate arguments shown in the gate symbol of custom gates. These now include control qubits in the count. This change only affects the graphics, not the behaviour of the gates.

- Minor corrections and updates to documentation.

## Release Notes (12 February 2025)

### Changes to QCircuit Class

- A 'to_unitary' method has been added to QCircuit to return the unitary matrix of a circuit.

- A 'basis_names' method has been added to QCircuit which returns an array of the names (i.e. labels) of the basis states.

Some API changes have been made to create a cleaner separation of concerns between data content and presentation. This includes some new formatting options.

  - The 'components' method has been replaced by 'format_state'.

  - The 'probabilities' method has been replaced the following methods:
    - format_probabilities()
    - probability_dict()
    - probability_array()

### Documentation and Examples

The documentation was previously in the form of Markdown files. This led to some compatibility issues with different Markdown viewers and tools, particularly where there was embedded LaTeX. Consequently, the documentation has been converted into HTML and placed on GitHub Pages:

- [https://jbrumf.github.io/tinyqsim/](https://jbrumf.github.io/tinyqsim/)

There was previously a lot of overlap and unnecessary duplication between the Markdown documentation and Jupyter notebook examples. This resulted in extra work maintaining two versions.

The master copy of the tutorials and examples are now in the form of Jupyter notebooks in the 'examples' directory. This has the benefit that errors in the example code are more easily detected as they are actually executed. HTML files are generated from the notebooks for inclusion in the documentation.

### Other Updates

- Numpy was recently upgraded to version 2. Numpy arrays now print with the type of each element prefixing the scalar values. This made the output from some the TinyQsim methods difficult to read, so some changes were needed to the code.

- The documentation, examples and test-cases have been updated to reflect the above changes.
