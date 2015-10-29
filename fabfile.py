# coding:utf-8
import sys
from fabric.api import env, cd, local, put, run
from fabric.api import sudo
from fabric.contrib.files import exists
try:
    import fab_settings as settings
except ImportError:
    print "You must provide a valid fab_settings.py module in this directory"
    sys.exit(1)

env.hosts = settings.hosts
repo_url = "https://github.com/guyskk/kkblog.git"
tmp_dir = "/tmp/kkblog-dist"


def deploy():

    # 清理临时目录
    if exists(tmp_dir):
        sudo("rm -R %s" % tmp_dir)
    run("mkdir %s" % tmp_dir)

    # 打包
    local("python setup.py sdist --formats gztar")
    put("dist/kkblog-1.0.tar.gz", tmp_dir)
    with cd(tmp_dir):
        run("tar -xzf kkblog-1.0.tar.gz && mv kkblog-1.0 kkblog")

    # 部署
    with cd("%s/kkblog" % tmp_dir):
        sudo("apt-get install -y --force-yes dos2unix")
        run("dos2unix deploy.sh")
        sudo("bash deploy.sh")
