#!/usr/bin/env bash
set -e # exit when any command fails
BUILD_DIR=../shared_objects/
mkdir -p $BUILD_DIR

for file in $([ -z "$@" ] && echo $(dirname "$0")/* || echo "$@")  ; do
    if [[ $file != *.c ]]; then
        echo $file is not a c source file!
        continue
    fi

    if [[ $file == *parallel.c ]]; then
      options='-fopenmp'
    else
      options=''
    fi

    gcc $options -Ofast -shared -Wl,-soname,cfunc -fPIC $file -o $BUILD_DIR$(basename $file .c).so
    echo $file compiled with $options!
done
