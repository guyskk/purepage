# coding:utf-8

from fabric.api import *

# 使用远程命令的用户名

env.passwords = {
    # "kk@127.0.0.1:2333": "kk",
}
# 执行命令的服务器
env.hosts = [
    "kk@127.0.0.1:2333",
    # "guyskk@222.204.27.1:22"
]

DIST_DIR = "/tmp/kkblog/dist"

files = [
    "kkblog_nginx.conf",
    "kkblog_uwsgi.ini",
    "deploy.sh",
    "manage.sh",
    "manage.py",
    "requires.txt"
]


def pack():
    # 创建一个新的分发源，格式为 tar 压缩包
    local('python setup.py sdist --formats=gztar', capture=False)


def deploy():
    print("Executing on %(host)s as %(user)s" % env)
    # 定义分发版本的名称和版本号
    dist = local('python setup.py --fullname', capture=True).strip()
    # 创建发布目录
    run("test -d %s || mkdir -p %s" % (DIST_DIR, DIST_DIR))
    # 把 tar 压缩包格式的源代码上传到服务器
    put("dist/%s.tar.gz" % dist, "%s/kkblog.tar.gz" % DIST_DIR)
    for f in files:
        put(f, DIST_DIR)
    with cd(DIST_DIR):
        sudo("bash deploy.sh")
