#!/bin/sh

if [ ! -d '/run/nginx' ]; then 
	mkdir /run/nginx
fi

while /bin/true; do 
	/usr/bin/supervisord
done