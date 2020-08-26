#!/bin/bash

for FILE in *.py; do isort $FILE; done