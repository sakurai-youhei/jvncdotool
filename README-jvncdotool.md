# Requirement

Only **Jython 2.7-b1** is tested.

# How to build and run jvncdo  
At first, please do `git submodule update --init` to retrieve all submodules under externals directory.

Then, nothing special. Run setup-jython.py with **clean** and **bdist_egg** command by Jython, set JYTHONPATH to built egg file and then run "import jvncdotool;jvncdotool.command.vncdo()" somehow.

## On Windows  

```
SET JYTHONPATH=
java.exe -jar jython-standalone-2.7-b1.jar -C UTF-8 setup-jython.py clean bdist_egg
SET JYTHONPATH=dist\jvncdotool-0.0.1.dev0-py2.7.egg
java.exe -jar jython-standalone-2.7-b1.jar -C UTF-8 -c "import jvncdotool.command;jvncdotool.command.vncdo()" --help
```

## On Linux  

```
env JYTHONPATH="" java -jar jython-standalone-2.7-b1.jar -C UTF-8 setup-jython.py clean bdist_egg
env JYTHONPATH=dist/jvncdotool-0.0.1.dev0-py2.7.egg java -jar jython-standalone-2.7-b1.jar -C UTF-8 -c "import jvncdotool.command;jvncdotool.command.vncdo()" --help
```
