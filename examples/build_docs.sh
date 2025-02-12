#/bin/bash

# Generates Markdown and/or HTML versions of Jupyter Notebooks.

if [[ "$PWD" != */tinyqsim ]]
then
    echo "Script must be run from tinyqsim directory"
    exit
fi						       

cd examples

export OUTH=../doc/html/
export OUTM=../release/generated/

# Generate HTML versions of notebooks
# mkdir -p $OUTH
# jupyter nbconvert --output-dir=$OUTH --to html tutorial_1_getting_started.ipynb
# jupyter nbconvert --output-dir=$OUTH --to html tutorial_2_exploring_further.ipynb
# jupyter nbconvert --output-dir=$OUTH --to html tutorial_3_guide_to_gates.ipynb
# jupyter nbconvert --output-dir=$OUTH --to html tutorial_4_low_level_api.ipynb
# jupyter nbconvert --output-dir=$OUTH --to html example_2_QFT4.ipynb
# jupyter nbconvert --output-dir=$OUTH --to html example_3_quantum_fourier_transform.ipynb
# jupyter nbconvert --output-dir=$OUTH --to html example_4_quantum_phase_estimation.ipynb

# Generate Markdown versions of notebooks
mkdir -p $OUTM
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_1_getting_started.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_2_exploring_further.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_3_guide_to_gates.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown tutorial_4_low_level_api.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_2_QFT4.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_3_quantum_fourier_transform.ipynb
jupyter nbconvert --output-dir=$OUTM --to markdown example_4_quantum_phase_estimation.ipynb
