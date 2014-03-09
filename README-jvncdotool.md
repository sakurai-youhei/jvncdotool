# How to build and run jvncdo  
Nothing special. Run setup-jython.py with clean and bdist_egg command by Jython, set JYTHONPATH tp built egg file and then run "import jvncdotool;jvncdotool.command.vncdo()" somehow.

## On Windows  

```
C:\jython2.7b1\jython.bat setup-jython.py clean bdist_egg
cd dist
SET JYTHONPATH=jvncdotool-0.0.1.dev0-py2.7.egg
C:\jython2.7b1\jython.bat -C UTF-8 -c "import jvncdotool.command;jvncdotool.command.vncdo()" --help
```

## On Linux (Not checked, yet)  

```
jython.sh setup-jython.py clean bdist_egg
cd dist
env JYTHONPATH=jvncdotool-0.0.1.dev0-py2.7.egg jython.sh -C UTF-8 -c "import jvncdotool.command;jvncdotool.command.vncdo()" --help
```
