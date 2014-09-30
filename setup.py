# -*- coding: UTF-8 -*-

import setuptools
from distutils.core import setup

# http://stackoverflow.com/a/7071358/735926
import re
VERSIONFILE='edt2ics/__init__.py'
verstrline = open(VERSIONFILE, 'rt').read()
VSRE = r'^__version__\s+=\s+[\'"]([^\'"]+)[\'"]'
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)

setup(
    name='p7edt2ics',
    version=verstr,
    author='Baptiste Fontaine',
    author_email='b@ptistefontaine.fr',
    packages=['edt2ics'],
    url='https://github.com/bfontaine/edt2ics',
    license=open('LICENSE', 'r').read(),
    description='Paris Diderot CS dep. iCalendar schedule converter',
    long_description=open('README.rst', 'r').read(),
    install_requires=[
        'argparse >= 1.1',
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
       #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
       #'Programming Language :: Python :: 3.2',
       #'Programming Language :: Python :: 3.3',
       #'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts':[
            'edt2ics = edt2ics.cli:main'
        ]
    },
)
