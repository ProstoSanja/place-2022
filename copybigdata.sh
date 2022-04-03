#!/bin/bash

for i in "./../bigdata"/*.*
do
    cp -f ./../bigdata/$(basename $i) ./build/$(basename $i)
done