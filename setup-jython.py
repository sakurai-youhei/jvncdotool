#!/usr/bin/env jython

import os, sys, re
import platform

README = """\


"""

# Workarounds for Jython to enable "setup.py bdist_egg" at least.
if platform.system()=="Java" and sys.version_info[:2]<(2.6):
    setattr(platform, "python_implementation", lambda: "Jython")

if not sys.executable:
    for p in sys.path:
        jython_jar_and_None = set(
            [re.match(r"^jython.*\.jar$", x) for x in p.split(os.path.sep)])
        if len(jython_jar_and_None)!=1:
            jython_jar_and_None.remove(None)
            jython_jar = jython_jar_and_None.pop().group()
            sys.executable = p.split(jython_jar)+jython_jar

externals = os.listdir(os.path.join(os.path.dirname(__file__), "externals"))
for ex in externals:
    sys.path.append(os.path.join(os.path.dirname(__file__), "externals", ex))

from setuptools import setup

setup(
    name='jvncdotool',
    version='0.0.1.dev0',
    description='Command line VNC client for Jython',
    install_requires=[
        'Twisted',
        "pymaging",
        "pymaging-png",
    ],
    url='https://github.com/sakurai-youhei/vncdotool',
    author='Youhei Sakurai',
    author_email='sakurai.youhei+jvncdotool@gmail.com',
    download_url='',

    entry_points={
        "console_scripts": [
            'vncdo=jvncdotool.command:vncdo',
            'vncdotool=jvncdotool.command:vncdo',
            'vnclog=jvncdotool.command:vnclog',
        ],
    },
    packages=['jvncdotool'],

    classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Framework :: Twisted',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Jython',
          'Programming Language :: Python :: 2.7',
          'Topic :: Multimedia :: Graphics :: Viewers',
          'Topic :: Software Development :: Testing',
    ],

    long_description=README,
)

