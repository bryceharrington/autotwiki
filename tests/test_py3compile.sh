#!/bin/bash

. data/bubu.lib

echo "# Python3 compilation verification"

display_result() {
    if [ $1 == 0 ]; then
        pass "${2} ${3}"
    else
        fail "${2} ${3}"
    fi
}

# Basic syntax checking
for script in $(find . -name "*.py"); do
    py3compile ${script}
    display_result $? ${script}
done

final_summary

exit 0
