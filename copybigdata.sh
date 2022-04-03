#!/bin/bash

for i in *.*
do
    cp -f $i ./../bigdata/$i ./build/$i
done