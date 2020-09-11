#!/usr/bin/env bash

# Install required packages from requirements.txt file
#conda install --file requirements.txt

# Add environment to jupyter notebooks
python -m ipykernel install --user --name=$CONDA_DEFAULT_ENV
echo "Environment has been added to jupyter notebook"

# Make hooks executable
chmod +x hooks/*_hook.sh
echo "Hooks have been made executable"

