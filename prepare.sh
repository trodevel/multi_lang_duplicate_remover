#!/bin/bash

FL=$1

[[ -z $FL ]]   && echo "ERROR: input file is not given" && exit 1
[[ ! -f $FL ]] && echo "ERROR: input file $FL is missing" && exit 1

FO="${FL%%.*}"

sort $FL > $FO.srt.csv
uniq $FO.srt.csv > $FO.srt.uniq.csv

# enumerate
nl -s";" -nln -w1 $FO.srt.uniq.csv > $FO.srt.uniq.num.csv

RU="а-я"
DE="äöüß"
EN="a-z"
# ru
grep -i "[$RU]\+"  $FO.srt.uniq.num.csv > $FO.srt.uniq.num.ru.csv
# de
grep -i "[$DE]\+" $FO.srt.uniq.num.csv > $FO.srt.uniq.num.de.csv
# en
grep -i "[$EN]\+" $FO.srt.uniq.num.csv | grep -v -i "[${RU}${DE}]\+" > $FO.srt.uniq.num.en.csv
# other
grep -v -i "[${RU}${DE}${EN}]\+"  $FO.srt.uniq.num.csv> $FO.srt.uniq.num.other.csv
