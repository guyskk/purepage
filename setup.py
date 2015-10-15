# coding:utf-8

from setuptools import setup
setup(
    name="kkblog",
    version="0.0.3",
    description="kkblog",
    author="kk",
    url="https://github.com/guyskk/kkblog",
    license="MIT",
    packages=["kkblog", "kkblog.model", "kkblog.config"],
    # py_modules=["manage"],
    install_requires=[
        'flask>=0.10.1',
        'pyjwt>=1.4',
        "flask-restaction>=0.17.1",
        "flask-cors>=2.0",
        "markdown>=2.6",
        "pony>=0.6.1",
        "pyquery>=1.2",
        "pygitutil>=0.0.3"
    ],
    dependency_links=[
        # "https://github.com/mitsuhiko/flask/tarball/master",
        # "https://github.com/ponyorm/pony/tarball/master",
    ],
    include_package_data=True,
    zip_safe=False,
)
