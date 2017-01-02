#!/bin/sh

HTTP_PORT=80
TV_IP=192.168.0.31
TCP_SERVER_PORT=8888
LOCAL_IP=192.168.0.29

iptables -t nat -A PREROUTING -p tcp -d $LOCAL_IP --dport $HTTP_PORT -j DNAT --to-destination $LOCAL_P:$TCP_SERVER_PORT -s $TV_IP
sysctl net.ipv4.ip_forward=1
