#!/usr/bin/env bash

for FILE in $(git diff --staged --name-only --diff-filter=AMC "***.py")
do
  black $FILE
  git add $FILE
done
