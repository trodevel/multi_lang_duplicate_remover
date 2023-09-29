#!/bin/bash

FL=$1

[[ -z $FL ]]   && echo "ERROR: input file is not given" && exit 1
[[ ! -f $FL ]] && echo "ERROR: input file $FL is missing" && exit 1

FO="${FL%.*}"

sort $FL > $FO.1.csv
uniq $FO.1.csv > $FO.2.csv

# enumerate
nl -s";" -nln -w1 $FO.2.csv > $FO.3.csv

RU="а-я"
DE="äöüß"
EN="a-z"
# ru
grep -i "[$RU]\+"  $FO.3.csv > $FO.4.ru.csv
# de
grep -i "[$DE]\+" $FO.3.csv > $FO.4.de.csv
# en
grep -i "[$EN]\+" $FO.3.csv | grep -v -i "[${RU}${DE}]\+" > $FO.4.en.csv
# other
grep -v -i "[${RU}${DE}${EN}]\+"  $FO.3.csv> $FO.4.other.csv
