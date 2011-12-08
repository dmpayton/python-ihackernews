import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ihackernews',
    version='1.0.0',
    description='A Python library for the iHackerNews API.',
    license='MIT',
    url='https://github.com/dmpayton/python-ihackernews',
    author='Derek Payton',
    author_email='derek.payton@gmail.com',
    py_modules=['ihackernews'],
    install_requires=['requests'],
    classifiers = (
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ),
)
