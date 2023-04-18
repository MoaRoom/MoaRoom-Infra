#!/bin/bash

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

# Banner
# cp /root/workdir/issue.net /etc/issue.net # 원격 접속 시도 시
# cp /root/workdir/issue.net /etc/issue     # 콘솔 접속 시도 시
cp /root/workdir/motd /etc/motd        # 로그인 성공 시


# run foreground and daemon
# # wssh --fbidhttp=False &
# python3 ./webssh/run.py &
python3 ./webssh/run.py --fbidhttp=False & # --certfile='/root/.ssh/keys/tls.crt' --keyfile='/root/.ssh/keys/tls.key' &
cd /root/workdir/server && python3 -m uvicorn main:app --reload --host=0.0.0.0 --port=8001 &
/usr/sbin/sshd &
/usr/sbin/nginx -g "daemon off;"



