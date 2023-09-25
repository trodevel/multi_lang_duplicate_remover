#!/bin/bash

INP=$1
OUTP=$2

[[ -z $INP ]]   && echo "ERROR: input file is not given" && exit 1
[[ -z $OUTP ]]  && echo "ERROR: output file is not given" && exit 1
[[ ! -f $INP ]] && echo "ERROR: input file $INP is missing" && exit 1

FO="${INP%%.*}"

./convert_xlsx_to_csv.sh $FO.srt.uniq.num.en.ru.xlsx
./convert_xlsx_to_csv.sh $FO.srt.uniq.num.ru.en.xlsx

# ru
cat $FO.srt.uniq.num.ru.csv $FO.srt.uniq.num.en.ru.csv > $OUTP.ru.csv

# en
cat $FO.srt.uniq.num.en.csv $FO.srt.uniq.num.ru.en.csv > $OUTP.en.csv
