#!/bin/bash

echo 更新代码
wget -r -X "oth","app/static/node_modules" -N -q -P .. ftp://192.168.56.1/

echo 结束所有uwsgi进程
killall -KILL uwsgi

echo 启动uwsgi http://0.0.0.0:5000
uwsgi --http 0.0.0.0:5000 -w app:app