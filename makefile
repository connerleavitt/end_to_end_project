## Run the makefile by running the command "make"

## PREREQUISITES ## files used as input to create the target
SHELL:=/usr/bin/env bash
CONDA_ENV_NAME=test_conda_1

## TARGETS AND RULES ##

# Targets to be run with the "make" command are listed as a rule in the "all" target
all: create activate

# Create a conda environment called test_conda_1
create:
	conda create --name $(CONDA_ENV_NAME) --file requirements.txt

# The activate target will prompt the user to run conda activate on the newly made environment.
# Once it is run, the user will run env_config.sh to activate and add the environment to jupyter notebooks and then make the hooks executable
activate:
	@echo ""
	@echo "Environment $(CONDA_ENV_NAME) created"
	@echo "Please activate it by running"
	@echo "    'conda activate $(CONDA_ENV_NAME)'"
	@echo "and then finish setting up the environment by running"
	@echo "    'bash env_config.sh'"
	@echo ""
	@echo ""

# The clean target will not be run because it is not listed above in the "all" target. The command to run this target is "make clean"
clean:
	conda env remove --name $(CONDA_ENV_NAME)
