from setuptools import setup
from os.path import join, dirname

with open(join(dirname(__file__), 'requires.txt'), 'r') as f:
    install_requires = f.read().split("\n")
    install_requires = [x for x in install_requires if x[:4] != "git+"]

setup(
    name="purepage",
    version="1.0",
    description="purepage",
    author="guyskk",
    author_email="guyskk@qq.com",
    url="https://github.com/guyskk/purepage",
    license="MIT",
    packages=["purepage", "purepage.views"],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
