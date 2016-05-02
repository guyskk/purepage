from setuptools import setup
from os.path import join, dirname

with open(join(dirname(__file__), 'requires.txt'), 'r') as f:
    install_requires = f.read().split("\n")

setup(
    name="purepage",
    version="1.0",
    description="purepage",
    author="guyskk",
    author_email="guyskk@qq.com",
    url="https://github.com/guyskk/purepage",
    license="MIT",
    packages=["couchdb", "purepage", "purepage.views"],
    py_modules=["flask_couchdb"],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
