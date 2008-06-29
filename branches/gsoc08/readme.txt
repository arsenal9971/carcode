                             README
                    Carcode GSOC Development branch
=====================================================================

Software Requirements

 * Python 2.4 or later
 * Pygame 1.6 or later
 * PyOpenGL 2.0 or later (2.0 highly recomended),
   you do not need 3D acceleration.
 * Python supported OS:
   - Linux
   - Windows
   - *BSD


Running Carcode

You can tell carcode to load a give level file with the option -l,
as shown in the example we load a file under the demo directory:

 python carcode.py -l demos/level1.py

You can set a script to handle the car logic with the option -s,
as show in the example:

 python carcode.py -s mylogic.py

A full example of loading a level and logic:

 python carcode.py -l demos/level1.py -s mylogic.py

Lengthy car scripts or with tight loops can degrade overall
performance.


LINUX, *BSD NOTES
=====================================================================

RPM

Our setup.py script has support for building RPM files, to use
it you will need rpm building packages such as rpmbuild, run the 
script from the shell with the following arguments:

 python setup.py bdist_rpm


DEB

Our setup.py script has support for building DEB files for Debian or
Ubuntu, you will need to have deb building tools installed such as
debuild, run the script from the shell with the following arguments:

 python setup.py bdist_deb


Generic instructions

You can install carcode in your system with our setup.py script
by running it as root with the following arguments:

 python setup.py install

If you do not want to install it system wide you can choose other
directory:

 python setup.py install --prefix /path/to/directory


WINDOWS NOTES
=====================================================================

GLUT

Installing pyOpenGL 2.0 sometimes misses a few DLLS, if carcode is
giving you an error about missing GLUT32.DLL download it from:

http://www.xmission.com/~nate/glut.html

Copy the glut32.dll to your system32 folder or to the carcode folder.

Py2exe

Our setup.py script has support for creating self contained
executables with py2exe, to use it run the script from the
command line with the argument py2exe as shown:

 python setup.py py2exe

This will generate a directory with the py2exe bundle, for
further information check the py2exe options:

 python setup.py py2exe --help


Windows Installer

Our setup.py script can create windows installer for carcode,
you can use it by running from the command line the setup.py
script with the following arguments:

 python setup.py bdis_wininst

This will create a windows installer, however, it DOES NOT
INCLUDE DEPENDENCIES, such as python itself, pygame or pyOpenGL.