#!/bin/bash

FL=$1

[[ -z $FL ]]   && echo "ERROR: input file is not given" && exit 1
[[ ! -f $FL ]] && echo "ERROR: input file $FL is missing" && exit 1

FO="${FL%%.*}"

sort $FL > $FO.srt.csv
uniq $FO.srt.csv > $FO.srt.uniq.csv

# enumerate
nl -s";" -nln -w1 $FO.srt.uniq.csv > $FL.srt.uniq.num.csv
# ru
grep -i "[а-я]+" $FL.srt.uniq.num.ru.csv
# de
grep -i "[äöüß]+" $FL.srt.uniq.num.de.csv
# en
grep -v -i "[а-яäöüß]+" $FL.srt.uniq.num.en.csv
