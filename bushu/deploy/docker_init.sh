#!/bin/bash

/usr/bin/python /opt/web.py &
/etc/init.d/nginx start
service keepalived start
while true;do
    echo 'sleeping 1'
    sleep 10
done
