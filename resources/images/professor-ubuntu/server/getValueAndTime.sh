#!/bin/bash

start=`date +%s.%N`

/usr/bin/python3 $1 > values.txt

finish=`date +%s.%N`
diff=$( echo "$finish - $start" | bc -l )

/usr/bin/echo $diff > time.txt