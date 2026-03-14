#/bin/bash

# Generates Markdown versions of Jupyter Notebooks.

if [[ "$PWD" != */tinyqsim ]]
then
    echo "Script must be run from tinyqsim directory"
    exit
fi						       

cd examples

export OUTM=../release/generated/


# Generate Markdown versions of notebooks
mkdir -p $OUTM
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_1_getting_started.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_2_exploring_further.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_3_guide_to_gates.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_1_interference.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_2_phase_kickback.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_3_quantum_fourier_transform.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_4_quantum_phase_estimation.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_5_shors_algorithm.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_6_grovers_algorithm.ipynb

