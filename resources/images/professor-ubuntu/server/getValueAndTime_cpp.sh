#!/bin/bash

start=`date +%s.%N`

/usr/bin/g++ -o $2/test $1
$2/test > values.txt

finish=`date +%s.%N`


diff=$( echo "$finish - $start" | bc -l )
/usr/bin/echo $diff > time.txt