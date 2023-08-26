#!/bin/bash

start=`date +%s.%N`

/usr/bin/python3 $1 > values.txt

finish=`date +%s.%N`
diff=$( echo "$finish - $start" | bc -l )

echo $diff > time.txt