#!/bin/bash

. data/bubu.lib

echo "# Basic script syntax checks"

display_result() {
    if [ $1 == 0 ]; then
        pass "${2} ${3}"
    else
        fail "${2} ${3}"
    fi
}

ignorable() {
    for ext in '~' '~c' .pyc .o ; do
        if [ ${file_name%${ext}} != ${file_name} ]; then
            return 0
        fi
    done
    return 1
}

# Basic syntax checking
for script in bin/* apport/* ; do
    file_type=$(file -b ${script})
    file_name=$(basename $script)

    # Compiled objects and other cruft
    if ignorable ${file_name} ; then
        continue
    fi

    # Bash
    case ${file_type} in
        *troff*)
            ;;
        *byte-compiled*)
            ;;
        *bash*)
            bash -n $script >/dev/null 2>&1
            display_result $? 'bash' ${script}
            ;;
        *Bourne*)
            bash -n $script >/dev/null 2>&1
            display_result $? 'bash' ${script}
            ;;
        *perl*)
            perl -c $script >/dev/null 2>&1
            display_result $? 'perl' ${script}
            ;;
        *?ython*script*)
            python3 -m py_compile ${script}
            display_result $? 'python3' ${script}
	    if [ -e ${script}c ]; then
		rm ${script}c
	    fi
            ;;
        *directory*)
            ;;
        *) echo "Unknown script type '${file_type}'"
            display_result 1 ${script}
    esac
done

final_summary

exit 0
