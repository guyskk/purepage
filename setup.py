# coding:utf-8

from setuptools import setup
setup(
    name="kkblog",
    version="0.0.2",
    description="kkblog",
    author="kk",
    url="https://github.com/guyskk/kkblog",
    license="MIT",
    packages=["kkblog", "kkblog.model", "kkblog.config"],
    install_requires=[
        'flask>=0.1',
        'pyjwt>=1.4',
        "flask-restaction>=0.16.1",
        'validater>=0.7.3',
        "flask-cors>=2.0",
        "markdown>=2.6",
        "pony>=0.6",
        "pyquery>=1.2",
        "pygitutil>=0.0.3"
    ],
    dependency_links=[],
    include_package_data=True,
    zip_safe=False,
)
