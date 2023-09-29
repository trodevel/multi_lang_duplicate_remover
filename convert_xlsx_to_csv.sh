#!/bin/bash

INP=$1

[[ -z $INP ]] && echo "ERROR: INP is not given" && exit 1

OUTP=$( echo $INP | sed "s/\.xlsx/.csv/" )

xlsx2csv -d ";" $INP $OUTP

sed -i -e "s/;\s*/;/g" -e "s/;$//g" -e "s/;;$//" $OUTP
