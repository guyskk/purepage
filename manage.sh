#!/bin/bash

app_dir=/var/www/nginx/kkblog
config_dir=/var/www/nginx/config
env_dir=/var/www/nginx/kkblog/python_env

cd $app_dir

echo install kkblog
# ${env_dir}/bin/pip install -r requires.txt
cd kkblog_dist
${env_dir}/bin/python setup.py develop 
cd ..

echo reload uwsgi
if test $(pgrep -f nginx | wc -l) -eq 0; then
    ${env_dir}/bin/uwsgi --ini ${config_dir}/kkblog_uwsgi.ini
else
    ${env_dir}/bin/uwsgi -s reload --ini ${config_dir}/kkblog_uwsgi.ini
fi

echo reload nginx
if test $(pgrep -f nginx | wc -l) -eq 0; then
    nginx
else
    nginx -s reload
fi

pgrep -a uwsgi
pgrep -a nginx

exit 0