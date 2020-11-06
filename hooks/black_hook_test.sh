#!/usr/bin/env bash

function py_file_search() {
  #Run the find command on all files that end with the .py extension
  git diff --name-only --diff-filter=AMC -name "*.py"
}
#Run the black auto-formatter on the result of the py_file_search function
black $(py_file_search)