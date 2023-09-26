#!/bin/bash
crontab -l > file1
echo "$1 $2 $3 $4 * /bin/bash /root/workdir/server/getAssignments.sh $5 $6 $7  > /proc/1/fd/1 2>/proc/1/fd/2" >> file1
cat file1 | crontab -
rm -rf file1

service cron restart