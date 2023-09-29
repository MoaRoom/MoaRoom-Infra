#!/bin/bash

start=`date +%s.%N`

/usr/bin/gcc $1 -o $2/test.out
$2/test.out > $2/values.txt

finish=`date +%s.%N`


diff=$( echo "$finish - $start" | bc -l )
/usr/bin/echo $diff > $2/time.txt