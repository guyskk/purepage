#!/bin/bash

echo 更新代码
rm -R app
wget ftp://192.168.56.1/ -r -X "oth","app/static/node_modules" -N -nv -P ..

echo 复制nginx配置文件到/etc/nginx/sites-enabled
sudo cp kkblog_nginx.conf /etc/nginx/sites-enabled

echo 结束所有uwsgi进程
killall -KILL uwsgi

echo 启动uwsgi
uwsgi --ini kkblog_uwsgi.ini

echo 重启nginx
sudo service nginx restart

echo 查看uwsgi进程
pgrep -a uwsgi

echo 查看nginx进程
pgrep -a nginx




