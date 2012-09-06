#!/usr/bin/env python
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

try:
    license = open('LICENSE').read()
except:
    license = None


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def desc():
    return read('README.rst')

setup(
    name='django-sockjs-tornado',
    version='0.0.1',
    author='Peter Bengtsson',
    author_email='mail@peterbe.com',
    packages=['django_sockjs_tornado'],
    namespace_packages=['django_sockjs_tornado'],
    scripts=[],
    url='http://github.com/peterbe/django-sockjs-tornado/',
    license=license,
    description='Makes it easy to run a SockJS server in Django through Tornado',
    long_description=desc(),
    requires=['tornado', 'sockjs'],
    install_requires=[
        'tornado >= 2.1.1',
        'sockjs-tornado >= 0.0.4'
    ],
    zip_safe=False,
)
