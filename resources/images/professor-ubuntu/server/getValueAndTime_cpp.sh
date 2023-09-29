#!/bin/bash

start=`date +%s.%N`

/usr/bin/g++ -o $2/test $1
$2/test > $2/values.txt
/usr/bin/rm -rf $2/test

finish=`date +%s.%N`


# diff=$( echo "$finish - $start" | bc -l )
# /usr/bin/echo $diff > $2/time.txt
/usr/bin/echo "" > $2/time.txt