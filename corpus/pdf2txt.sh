#!/usr/bin/env bash

for f in pdf/*.pdf
do
    filename=$(basename "$f")
    extension="${filename##*.}"
    filename="${filename%.*}"
    pdftotext "$f" "txt/$filename".txt
done
