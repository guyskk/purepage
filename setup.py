# coding:utf-8

from setuptools import setup
setup(
    name="kkblog",
    version="0.0.4",
    description="kkblog",
    author="guyskk",
    url="https://github.com/guyskk/kkblog",
    license="MIT",
    packages=["kkblog", "kkblog.model", "kkblog.config"],
    py_modules=["manage"],
    install_requires=[
        'flask>=0.10.1',
        'pyjwt>=1.4',
        "flask-restaction>=0.17.3",
        "flask-cors>=2.0",
        "flask-cache>=0.13.0",
        "markdown>=2.6",
        "pony>=0.6.1",
        "pyquery>=1.2",
        "pygitutil>=0.0.5",
        "flask-mail>=0.9.1",
    ],
    dependency_links=[
        # "https://github.com/mitsuhiko/flask/tarball/master",
        # "https://github.com/ponyorm/pony/tarball/master",
    ],
    include_package_data=True,
    zip_safe=False,
)
