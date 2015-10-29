#!/bin/bash

tmp_dir=/tmp/kkblog-dist

app_dir=/var/www/kkblog
log_dir=/var/www/log
socket_dir=/var/www/socket
config_dir=/var/www/config
nginx_config_dir=${config_dir}/nginx
uwsgi_config_dir=${config_dir}/uwsgi
env_dir=${app_dir}/venv

echo install gcc,pip,virtualenv,uwsgi
if test $(gcc --version|wc -l) -eq 0
then
    apt-get install -y --force-yes build-essential
fi
if test $(pip --version|wc -l) -eq 0
then
    apt-get install -y --force-yes python-pip
fi
if test $(virtualenv --version|wc -l) -eq 0
then
    pip install virtualenv
fi
if test $(uwsgi --version|wc -l) -eq 0
then
    pip install uwsgi
fi

echo create app_dir
test -d $app_dir || mkdir $app_dir
test -d ${tmp_dir}/kkblog && cp -r ${tmp_dir}/kkblog ${app_dir}/../

test -d $log_dir || mkdir $log_dir
test -d $socket_dir || mkdir $socket_dir
test -d $config_dir || mkdir $config_dir
test -d $nginx_config_dir || mkdir $nginx_config_dir
test -d $uwsgi_config_dir || mkdir $uwsgi_config_dir
test -d $env_dir || virtualenv $env_dir

cd $app_dir
cp kkblog_nginx.conf $nginx_config_dir
cp kkblog_uwsgi.ini $uwsgi_config_dir

echo install kkblog
# insall lxml
apt-get install -y --force-yes libxml2-dev libxslt-dev lib32z1-dev python-dev
${env_dir}/bin/pip install -r requires.txt

echo reload uwsgi
if test $(pgrep uwsgi|wc -l) -eq 0
then
    uwsgi --emperor ${uwsgi_config_dir} --daemonize ${log_dir}/uwsgi_emperor.log
else
    touch ${uwsgi_config_dir}/kkblog_uwsgi.ini
fi

echo reload nginx
if test $(pgrep nginx|wc -l) -eq 0
then
    nginx
else
    nginx -s reload
fi

echo start uwsgi on startup
cp uwsgi.conf /etc/init
initctl reload-configuration

chown -R www-data:www-data $app_dir
chown -R www-data:www-data $socket_dir
chmod o+r ${log_dir}/*

pstree -apsAl

exit 0

