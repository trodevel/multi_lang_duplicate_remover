#!/bin/bash

INP=$1
OUTP=$2

[[ -z $INP ]]   && echo "ERROR: input file is not given" && exit 1
[[ -z $OUTP ]]  && echo "ERROR: output file is not given" && exit 1
[[ ! -f $INP ]] && echo "ERROR: input file $INP is missing" && exit 1

INP="${INP%%.*}"

./convert_xlsx_to_csv.sh $INP.4.en.ru.xlsx
./convert_xlsx_to_csv.sh $INP.4.ru.en.xlsx

# ru
cat $INP.4.ru.csv $INP.4.en.ru.csv | sort -n > $OUTP.ru.csv

# en
cat $INP.4.en.csv $INP.4.ru.en.csv | sort -n > $OUTP.en.csv
