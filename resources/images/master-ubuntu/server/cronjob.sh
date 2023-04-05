#!/bin/bash
  
crontab -l > file1
echo "$1 $2 $3 $4 * /usr/bin/python3 /root/workdir/server/getAssignments.py $5  > /proc/1/fd/1 2>/proc/1/fd/2" >> file1
cat file1 | crontab -
rm -rf file1

service cron restart