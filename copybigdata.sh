#!/bin/bash

for i in "./../bigdata"/*.*
do
    echo $(basename $i)
    cp -f ./../bigdata/$(basename $i) ./build/$(basename $i)
done