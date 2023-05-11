FROM ubuntu:20.04

USER root

# non interactive cmd
ARG DEBIAN_FRONTEND=noninteractive

# ubuntu:18.04의 경우 필요
# RUN add-apt-repository main
# RUN add-apt-repository universe
# RUN add-apt-repository restricted
# RUN add-apt-repository multiverse 
# RUN add-apt-repository backports

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get autoclean 
RUN apt-get dist-upgrade

## SSH

RUN echo "deb http://archive.ubuntu.com/ubuntu vivid main restricted universe" >> /etc/apt/sources.list # libffi-dev
RUN apt-get install -y ssh openssh-server sudo curl vim git openssh-client telnet net-tools nginx python3.8 python3-pip libc-dev libffi-dev gcc cron
# 컨테이너 이미지 파일의 크기를 줄이기 위해 apt 수행 중 생성된 임시 파일들을 삭제해준다.
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN mkdir /var/run/sshd

# root 계정으로의 로그인을 허용한다. 아래 명령을 추가하지 않으면 root 계정으로 로그인이 불가능하다. 
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
# 응용 프로그램이 password 파일을 읽어 오는 대신 PAM이 직접 인증을 수행 하도록 하는 PAM 인증을 활성화
RUN sed -ri 's/UsePAM yes/# UsePAM yes/g' /etc/ssh/sshd_config
# 로그인 후 motd 나타나게
RUN sed -ri 's/PrintMotd no/PrintMotd yes/g' /etc/ssh/sshd_config

RUN mkdir /root/.ssh

EXPOSE 22

RUN mkdir /root/workdir
WORKDIR /root/workdir
COPY . /root/workdir

## API server
RUN pip3 install -r ./server/requirements.txt

EXPOSE 8003

## NGINX

VOLUME ["/data", "/etc/nginx/site-enabled", "/var/log/nginx"] 

EXPOSE 80

## WebSSh ( with Python3 )
RUN pip3 install -r ./webssh/requirements.txt 

EXPOSE 8886

## run ssh connection and nginx with startup.sh
RUN chmod +x /root/workdir/startup.sh
CMD ["./startup.sh"]


# tags
## 1.0: local version
### 1.1: api entity testing version
### 1.2: port list check version
## 2.1: k8s version