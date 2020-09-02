#!/bin/bash
finalexit=0
for FILE in $(git diff --staged --name-only --diff-filter=AMC "***.py")
do
    echo ""
    echo ""
    echo "+++++++ testing file $FILE +++++++"
    echo ""
    pytest $FILE
    pytexit=$?
    if [ $pytexit != 5 ] && [ $pytexit != 0 ]
    then
    finalexit=1
    fi
done
exit $finalexit
