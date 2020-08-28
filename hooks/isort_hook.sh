#!/bin/bash

for FILE in $(git diff --staged --name-only --diff-filter=AMC); do isort $FILE; done