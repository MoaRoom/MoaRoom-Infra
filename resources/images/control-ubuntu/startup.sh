#!/bin/bash
# set environment variables
i=1
while read line || [ -n "$line" ] ; do
  echo "export $line > /dev/null 2>&1" >> /etc/profile
  ((i+=1))
done < ./.env
source /etc/profile > /dev/null 2>&1

# no welcome message
chmod -x /etc/update-motd.d/*

# # ssl configuration
# mkdir -p /etc/nginx/ssl
# openssl req -new -x509 -nodes -newkey rsa:4096 -keyout localhost-nginx.key -out localhost-nginx.crt -days 365 -subj "/C=KR/ST=Seoul/L=Seoul/O=42Seoul/CN=localhost"
# mv localhost-nginx.key /etc/nginx/ssl
# mv localhost-nginx.crt /etc/nginx/ssl

# # 모든 프로토콜에 대해 호스트 키 생성
# ssh-keygen -A
# # SSH로 접속할 수 있는 유저 생성
# # 비밀번호로 접속하는 것을 막고 ssh key로만 접속할 수 있게 함.
# adduser --disabled-password ${SSH_USERNAME}
echo "root:${SSH_PASSWORD}" | chpasswd

mkdir -p /run/nginx
echo "<h1>THIS NGINX INDEX.HTML</h1>" >> /var/www/html/index.html


# run foreground and daemon
cd /root/workdir/server && python3 -m uvicorn main:app --reload --host=${SERVER_HOST} --port=$((${SERVER_PORT})) &
/usr/sbin/sshd &
/usr/sbin/nginx -g "daemon off;"