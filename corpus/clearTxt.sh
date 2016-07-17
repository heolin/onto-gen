#!/usr/bin/env bash

for f in txt/*.txt
do
    filename=$(basename "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    cat "$f" | ./clear_txt.py -b blacklist.list -s stopwords.list > "cleared/$filename".txt
done
