#!/bin/bash
set_remote_port()
{
 cat <<-EOF >/lib/systemd/system/docker-tcp.socket
[Unit]
Description=Docker Socket for the API

[Socket]
ListenStream=2376
BindIPv6Only=both
Service=docker.service

[Install]
WantedBy=sockets.target
EOF
}

set_daemon_conf()
{
    touch /etc/docker/daemon.json
 cat <<-EOF >/etc/docker/daemon.json
{
    "registry-mirrors":["https://docker.mirrors.ustc.edu.cn"],

    "insecure-registries":["$registry_address"],

    "tlsverify": true,

    "tlscacert": "/etc/docker/cert/ca.pem",

    "tlscert": "/etc/docker/cert/server-cert.pem",

    "tlskey": "/etc/docker/cert/server-key.pem"
}
EOF
}

gen_ss_docker_file()
{
    cat <<-EOF >ss_docker_file
FROM ubuntu:latest
RUN mkdir -p /opt
ADD scan_slave.tar.gz  /opt/
WORKDIR /opt/scan_slave/
CMD [ "/bin/bash", "-c", "/opt/scan_slave/docker_init.sh" ]
EOF
}
gen_cs_docker_file()
{
    cat <<-EOF >cs_docker_file
FROM nginx:latest
RUN mkdir -p /opt
ADD cms.tar.gz  /opt/
WORKDIR /opt/cms/
CMD [ "/bin/bash", "-c", "/opt/cms/docker_init.sh" ]
EOF
}

unstall_config()
{
rm /etc/docker -fr
rm /lib/systemd/system/docker-tcp.socket
}

if [ $# != 4  ]; then
    echo "usage: $0  registry_addres server_ip redis_ip mongo_ip"
    echo "example $0 192.168.3.241:5000"
    exit 1
fi

registry_address=$1
server_ip=$2
redis_ip=$3
mongo_ip=$4

#unstall_config

#mkdir /etc/docker
cd /tmp/init_install
let cpus=`cat /proc/cpuinfo |grep "processor"|wc -l `
echo -e " step 1/6) install docker"
# apt-get purge docker docker-engine docker.io -y 
# apt-get autoremove -y
# apt-get update &&  apt-get install curl  -y
# curl -sSL https://get.docker.com/ | sh 
echo -e " step 2/6) set remote port"
#set_remote_port
#systemctl enable docker-tcp.socket
#systemctl stop docker
#systemctl start docker-tcp.socket
#echo -e " step 3/6) set registry "
#set_daemon_conf
#if [ ! -f "server_cert.tar.gz" ];then
#    echo "server cert not exits"
#J    exit 1
#fi
##tar -xvf ./server_cert.tar.gz 
#rm /etc/docker/cert -fr
#mv server_cert /etc/docker/cert
#echo -e " step 4/6 docke service restart "
#service docker restart
#
#docker run hello-world | grep -q "Hello from Docker!"
#if [ $? == 0 ]; then
#    echo -e "Docker Install Successfully"
#    docker rm $(docker ps -a -q)
#else
#    echo -e "docker Install Failded"
#    exit 1
#fi
#
#echo -e " step 5/6 start scan_slave "
#gen_ss_docker_file
#docker rmi -f ss_image >/dev/null 2>&1
#docker build -f ss_docker_file -t ss_image .
#for ((i=0;i<cpus*2;i++));
#do
#    docker rm -f ss_container$i >/dev/null 2>&1
#    docker run  --name ss_container$i --restart always --add-host  masterhost:$server_ip --add-host redis:$redis_ip --–cpu-shares 512  -d ss_image
#done
echo -e " step 6/6 start cms_slave "
gen_cs_docker_file
#docker rmi -f cs_image >/dev/null 2>&1
#docker build -f cs_docker_file -t cs_image .
#for ((i=0;i<cpus;i++));
#do
#    docker rm -f cs_container$i >/dev/null 2>&1
#    docker run  --name cs_container$i --restart always --add-host masterhost:$server_ip --add-host redis:$redis_ip --add-host mongo:$mongo_ip --cpu-shares 1024  -d cs_image
#done
##rm /tmp/* -fr
#echo  -e "\033[34m all done \033[0m"
