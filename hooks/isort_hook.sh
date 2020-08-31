#!/bin/bash

for FILE in $(git diff --staged --name-only --diff-filter=AMC "***.py")
do
    isort $FILE
    git add $FILE
done
