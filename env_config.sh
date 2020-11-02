#!/usr/bin/env bash
#echo $CONDA_DEFAULT_ENV
# Install required packages from requirements.txt file
conda install pip
pip install -r requirements.txt
# Add environment to jupyter notebooks
python -m ipykernel install --user --name=$CONDA_DEFAULT_ENV
# Make hooks executable
chmod +x hooks/*_hook.sh
echo "Hook script files have been made executable"
