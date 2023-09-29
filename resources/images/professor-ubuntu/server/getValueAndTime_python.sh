#!/bin/bash

start=`date +%s.%N`

/usr/bin/python3 $1 > $2/values.txt

finish=`date +%s.%N`


# diff=$( echo "$finish - $start" | bc -l )
# /usr/bin/echo $diff > $2/time.txt
/usr/bin/echo "" > $2/time.txt