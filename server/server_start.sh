#!/bin/bash

sudo pkill gunicorn

#sleep 1
#pgrep gunicorn

sudo /usr/local/bin/api_hour api_hour_server:Container -b=unix:/travelhow.sock -w=17 --preload --graceful-timeout=30 --timeout=60 --threads=16 -D

sleep 1

#echo "-"
pgrep gunicorn -n
echo "server restarted"

service nginx status

if $BASH_ARGV == ""