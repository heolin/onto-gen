#!/usr/bin/env bash

for f in cleared/*.txt
do
    filename=$(basename "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    ./lemmatize.py -i "$f" > "lem/$filename".txt
done
