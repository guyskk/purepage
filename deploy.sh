#!/bin/bash

dist_dir=/tmp/kkblog/dist
app_dir=/var/www/nginx/kkblog
log_dir=/var/www/nginx/log
config_dir=/var/www/nginx/config
env_dir=/var/www/nginx/kkblog/python_env

echo create $app_dir
test -d $app_dir || mkdir $app_dir
cd $app_dir

echo create $log_dir
test -d $log_dir || mkdir $log_dir

echo create virtualenv
test -d $env_dir || virtualenv $env_dir
${env_dir}/bin/pip install uwsgi

echo create $config_dir
test -d $config_dir || mkdir $config_dir

echo copy config to $config_dir
cp ${dist_dir}/kkblog_nginx.conf $config_dir
cp ${dist_dir}/kkblog_uwsgi.ini $config_dir

echo copy some scripts to $app_dir
cp ${dist_dir}/manage.py $app_dir
cp ${dist_dir}/manage.sh $app_dir
cp ${dist_dir}/requires.txt $app_dir

echo unpack kkblog_dist
test -d kkblog_dist && rm -R kkblog_dist
mkdir kkblog_dist
tar xf ${dist_dir}/kkblog.tar.gz -C kkblog_dist --strip-components 1

echo start app
bash manage.sh

exit 0



