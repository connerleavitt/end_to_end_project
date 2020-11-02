## PREREQUISITES ## files used as input to create the target
SHELL:=/usr/bin/env bash
## Run the makefile by running "make"
CONDA_ENV_NAME=twitter_project
## RULES ##
# Create a conda environment called test_conda_1
all: create activate
create:
	conda create --name $(CONDA_ENV_NAME)
activate:
	@echo ""
	@echo "Environment $(CONDA_ENV_NAME) created"
	@echo "Please activate it by running"
	@echo "    'conda activate $(CONDA_ENV_NAME)'"
	@echo "and then finish setting up the environment by running"
	@echo "    'bash env_config.sh'"
	@echo ""
	@echo ""
clean:
	conda env remove --name $(CONDA_ENV_NAME)
