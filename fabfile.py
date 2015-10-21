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


def deploy(from_git=False):

    # 清理临时目录
    if exists(tmp_dir):
        sudo("rm -R %s" % tmp_dir)
    run("mkdir %s" % tmp_dir)

    # 更新代码
    if from_git:
        with cd(tmp_dir):
            run("git clone %s" % repo_url)
    else:
        local("git archive HEAD --output ./kkblog.zip")
        put("./kkblog.zip", tmp_dir)
        run("unzip {0}/kkblog.zip -d {0}/kkblog".format(tmp_dir))
        put("./kkblog_config.py", "%s/kkblog" % tmp_dir)

    # 部署
    with cd("%s/kkblog" % tmp_dir):
        sudo("bash manage.sh")
