#!/bin/bash

tmp_dir=/tmp/kkblog-dist

app_dir=/var/www/kkblog
log_dir=/var/www/log
config_dir=/var/www/config
nginx_config_dir=${config_dir}/nginx
uwsgi_config_dir=${config_dir}/uwsgi
env_dir=${app_dir}/venv

test -d $app_dir || mkdir $app_dir
test -d ${tmp_dir}/kkblog && cp -r ${tmp_dir}/kkblog ${app_dir}/../

test -d $log_dir || mkdir $log_dir
test -d $config_dir || mkdir $config_dir
test -d $nginx_config_dir || mkdir $nginx_config_dir
test -d $uwsgi_config_dir || mkdir $uwsgi_config_dir
test -d $env_dir || virtualenv $env_dir

cd $app_dir
cp kkblog_nginx.conf $nginx_config_dir
cp kkblog_uwsgi.ini $uwsgi_config_dir

echo install kkblog
# ${env_dir}/bin/pip install -e $app_dir
${env_dir}/bin/pip install -r requires.txt

echo reload uwsgi
if test $(pgrep -f uwsgi | wc -l) -eq 0; then
    uwsgi --emperor ${uwsgi_config_dir} --daemonize ${log_dir}/uwsgi_emperor.log
else
    touch ${uwsgi_config_dir}/kkblog_uwsgi.ini
fi

echo reload nginx
if test $(pgrep -f nginx | wc -l) -eq 0; then
    nginx
else
    nginx -s reload
fi

chown -R www-data:www-data $app_dir
chmod 755 $log_dir
chmod 766 $log_dir/*

pgrep -a uwsgi
pgrep -a nginx

exit 0