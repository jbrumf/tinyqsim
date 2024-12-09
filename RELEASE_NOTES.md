## Release Notes

No formal releases of TinyQsim have yet been made, but here a few comments on the latest updates. See the API documentation for further details.

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

There was previously a lot of overlap and unnecessary duplication between the Markdown documentation and Jupyter notebook examples. This resulted in extra work maintaining two versions.

These two forms of documentation have now been merged into Jupyter notebooks and brought up to date. The 'nbconvert' tool is used to create copies in Markdown for the 'doc' directory. This approach would also make it easy to generate an HTML version of the documentation and examples if required at a later date.

This restructuring has the added benefit that errors in the examples are more easily detected since the example code in the notebooks is actually executed.

### General

- Numpy was recently upgraded to version 2. Numpy arrays now print with the type of each element prefixing the scalar values. This made the output from some the TinyQsim methods difficult to read, so some changes were needed to the code.

- The documentation, examples and test-cases have been updated to reflect the above changes.
