#!/bin/bash

file1=${1?param missing - from file.}
file2=${2?param missing - to file.}

if [ ! -f "$file1" ]; then
    echo "Missing input1 file" 1>&2
    exit
fi

if [ ! -f "$file2" ]; then
    echo "Missing input2 file" 1>&2
    exit
fi

file1_cln=$( mktemp )
file2_cln=$( mktemp )

tr -d '\n' < "$file1" > "$file1_cln"
tr -d '\n' < "$file2" > "$file2_cln"
file1_len=$( wc -c < "$file1_cln" )
file2_len=$( wc -c < "$file2_cln" )

if (( $file1_len != $file2_len )); then
    (
        echo "File length mismatch"
        echo "len(${file1}): ${file1_len}"
        echo "len(${file2}): ${file2_len}"
    ) 1>&2
fi

diff <(tr -d '\n' < "$file1") <(tr -d '\n' < "$file2")

if (( $? == 0 )); then
    echo "files match!" 1>&2
fi
