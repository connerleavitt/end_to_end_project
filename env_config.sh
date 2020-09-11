#!/usr/bin/env bash
#This file will first add the newly made environment to jupyter notebooks and make any hook file executable

# Add environment to jupyter notebooks
python -m ipykernel install --user --name=$CONDA_DEFAULT_ENV
echo "Environment has been added to jupyter notebook"

# Make hooks executable
chmod +x hooks/*_hook.sh
echo "Hooks have been made executable"

