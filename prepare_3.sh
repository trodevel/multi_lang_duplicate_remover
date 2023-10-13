#!/bin/bash

INP=$1

[[ -z $INP ]]   && echo "ERROR: input file is not given" && exit 1
[[ ! -f $INP ]] && echo "ERROR: input file $INP is missing" && exit 1

INP="${INP%.*}"

python3.9 generate_similarity_map.py -i $INP.5.en.csv -o $INP.6.en.map.csv -s 90
python3.9 generate_similarity_map.py -i $INP.5.ru.csv -o $INP.6.ru.map.csv -s 90

python3.9 join_similarity_maps.py -i $INP.6.en.map.csv,$INP.6.ru.map.csv -o $INP.7.map.csv

python3.9 apply_similarity_map.py -m $INP.7.map.csv -i $INP.5.en.csv -o $INP.8.en.csv
python3.9 apply_similarity_map.py -m $INP.7.map.csv -i $INP.5.ru.csv -o $INP.8.ru.csv
