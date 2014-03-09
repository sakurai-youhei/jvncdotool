#!/usr/bin/env jython

import os, sys, re
import platform

README = open('README-jvncdotool.md', 'r').read()

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

setuptools_dir=os.path.join(os.path.dirname(__file__), "externals", "setuptools-3.0.2")
sys.path.append(setuptools_dir)
from setuptools import setup

dependencies = [
    "vncdotool",
    "pymaging",
    "pymaging_png",
    "twisted",
    "zope",
]
package_dir={
    "": setuptools_dir,
    "vncdotool": os.path.join(os.path.dirname(__file__), "vncdotool"),
    "jvncdotool": os.path.join(os.path.dirname(__file__), "jvncdotool"),
    "pymaging": os.path.join(os.path.dirname(__file__), "externals", "pymaging", "pymaging"),
    "pymaging_png": os.path.join(os.path.dirname(__file__), "externals", "pymaging-png", "pymaging_png"),
    "twisted": os.path.join(os.path.dirname(__file__), "externals", "twisted", "twisted"),
    "zope": os.path.join(os.path.dirname(__file__), "externals", "zope.interface", "src", "zope"),
}

for root, dirs, files in os.walk(package_dir["twisted"]):
    #print root, files
    if "__init__.py" in files:
        package = "twisted"+root.replace(package_dir["twisted"], "").replace(os.sep, ".")
        dependencies.append(package)
        package_dir[package] = root

for root, dirs, files in os.walk(package_dir["zope"]):
    #print root, files
    if "__init__.py" in files:
        package = "zope"+root.replace(package_dir["zope"], "").replace(os.sep, ".")
        dependencies.append(package)
        package_dir[package] = root

#print dependencies
#print package_dir

setup(
    name='jvncdotool',
    version='0.0.1.dev0',
    description='Command line VNC client for Jython',
    install_requires=[],
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
    packages=['jvncdotool']+dependencies,
    package_dir=package_dir,
    py_modules=["pkg_resources"],
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
          'Programming Language :: Jython :: 2.7',
          'Topic :: Multimedia :: Graphics :: Viewers',
          'Topic :: Software Development :: Testing',
    ],

    long_description=README,
)

