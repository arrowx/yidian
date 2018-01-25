#!/bin/bash
#mkdir -p ~/$NGINX1/www ~/$NGINX1/logs ~/$NGINX1/conf

nginxs=(
"nginx1"
"nginx2"
)

webs=(
"web1"
"web2"
"web3"
"web4"
)

#FROM xujian:keepalived
gen_nginx_docker_file()
{
    cat <<-EOF >$1"_docker_file"
FROM xujian:ok
RUN mkdir -p /opt
RUN mkdir -p /www
ADD docker_init.sh /opt/
ADD check_nginx.sh /etc/keepalived/
ADD $1/keepalived/keepalived.conf /etc/keepalived/
ADD $1/conf/nginx.conf.1 /etc/nginx/nginx.conf
ADD $1/www/index.html /www
CMD ["/bin/bash","-c","/opt/docker_init.sh"]
EOF
}

gen_web_docker_file()
{
    cat <<-EOF >$1"_docker_file"
FROM xujian:aptupdate
RUN mkdir -p /opt
ADD $1/web.py /opt/
CMD ["/usr/bin/python","/opt/web.py"]
EOF
}

#clean old nginxs
for container in "${nginxs[@]}"
do
    docker rm -f $container >/dev/null 2>&1
    docker rmi -f $container >/dev/null 2>&1
done

#clean old webs
for web in "${webs[@]}"
do
    docker rm -f $web >/dev/null 2>&1
    docker rmi -f $web >/dev/null 2>&1
done

#create network
ipstart="172.19.0."
docker network rm newnetwork
docker network create --subnet=$ipstart'0/24' newnetwork

i=11

for container in "${nginxs[@]}"
do
    gen_nginx_docker_file $container
    docker build -f $container"_docker_file" -t $container .
    #docker run  --name $container --network newnetwork --ip $ipstart$i -v $PWD/$container/conf/nginx.conf:/etc/nginx/nginx.conf -v $PWD/$container/www:/www -d $container
    docker run  --name $container --network newnetwork --cap-add=NET_ADMIN --ip $ipstart$i -d $container
    let i=$i+1
done

i=21
for web in "${webs[@]}"
do
    gen_web_docker_file $web
    docker build -f $web"_docker_file" -t $web .
    docker run  --name $web --network newnetwork --cap-add=NET_ADMIN --ip $ipstart$i -d $web
    let i=$i+1
done
