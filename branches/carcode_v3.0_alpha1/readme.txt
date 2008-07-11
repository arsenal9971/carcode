                             README
                    Carcode v3.0 Alpha1
=====================================================================

This is our first release, is an alpha release "As is" 
from our current development code, it is not fully featured 
but is functional, you may want to try it and experiment with it.

Please report any issues to our issue tracker (see link below), 
add the tag/label "Milestone-Alpha1" to separate it from 
other releases.

Home Page
    http://code.google.com/p/carcode/
    
Issue Tracker
    http://code.google.com/p/carcode/issues/list


Software Requirements
--------------------------------------------------

 * Python 2.4 or later
 * Pygame 1.6 or later
 * PyOpenGL 2.0 or later (2.0 highly recomended),
   you do not need 3D acceleration.
 * Python supported OS:
   - Linux
   - Windows
   - *BSD


Running Carcode
--------------------------------------------------

Run the carcode script file, from the shell this can be done with
the following command:

 python carcode.py
 
Carcode GUI gives you dialogs to load levels and scripts, but
we also offer command line options to do just that too.
 
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


Demo Levels
--------------------------------------------------

We have included a few levels demostrating current capabilities 
and scripting facilities of carcode, feel free of testing them out 
and doing your own car scripts to accomplish these levels.

Look for the files in the demos directory, check your package 
and platform notes to find out where it is.


Creating car scripts
--------------------------------------------------

Create a regular python file with your favorite text editor, with a function
named main that accepts one parameter, the car object, here is an
example from demos/level2_logic.py

# main function
def main(car):
    # Obtain the car sensors (left, right)
    lsensor = car.sensors["fl_sensor"]
    rsensor = car.sensors["fr_sensor"]

    # Check if the left sensor detected that we
    # are offroad and steer right
    if lsensor.pixel and not rsensor.pixel:
        car.steer_right()
        
    # Check if the right sensor detected that we
    # are offroad and steer left
    if not lsensor.pixel and rsensor.pixel:
        car.steer_left()
    
    # Check if both sensors detect we are offroad
    # try to steer right until we find the road back
    if lsensor.pixel and rsensor.pixel:
        car.steer_right()
        
    # Accelerate constantly
    if not car.moving() or car.speed < 2:
        car.accelerate()
        
Now save this file and load it from carcode, the main function 
will be executed everytime the car is updated.

To know about the available sensors and level characteristics 
consult the level file first, you may want to try the level without 
car script first to see what needs to be done and how.

Carscripts are specific for a level, each level has different 
characteristics such as available sensors, if the script tries to 
obtain a sensor that the car does not have it will crash carcode.


LINUX, *BSD NOTES
=====================================================================

RPM
--------------------------------------------------

Demos directory is installed in the following route:

/usr/share/doc/carcode/demos

Our setup.py script has support for building RPM files, to use
it you will need rpm building packages such as rpmbuild, run the 
script from the shell with the following arguments:

 python setup.py bdist_rpm


DEB
--------------------------------------------------

Demos are located in the following directory:

/usr/share/doc/carcode/examples

Our setup.py script has support for building DEB files for Debian or
Ubuntu, you will need to have deb building tools installed such as
debuild, run the script from the shell with the following arguments:

 python setup.py bdist_deb


Generic Instructions
--------------------------------------------------

You can install carcode in your system with our setup.py script
by running it as root with the following arguments:

 python setup.py install

If you do not want to install it system wide you can choose other
directory:

 python setup.py install --prefix /path/to/directory


WINDOWS NOTES
=====================================================================

pyOpenGL
--------------------------------------------------

Current version of pyOpenGL (3.0) depends on setuptools and is 
incompatible with py2exe, we recomended to use v2.0 which is
easier to get working, faster and compatible with py2exe.

For Python 2.5 you can download a custom pyOpenGL 2.0 package:

http://thorbrian.com/pyopengl/builds.php


GLUT
--------------------------------------------------

Installing pyOpenGL 2.0 sometimes misses a few DLLS, if carcode is
giving you an error about missing GLUT32.DLL download it from:

http://www.xmission.com/~nate/glut.html

Copy the glut32.dll to your system32 folder or to the carcode folder.


Py2exe
--------------------------------------------------

Our setup.py script has support for creating self contained
executables with py2exe, to use it run the script from the
command line with the argument py2exe as shown:

 python setup.py py2exe

This will generate a directory with the py2exe bundle, for
further information check the py2exe options:

 python setup.py py2exe --help


Windows Installer
--------------------------------------------------

Our setup.py script can create windows installer for carcode,
you can use it by running from the command line the setup.py
script with the following arguments:

 python setup.py bdis_wininst

This will create a windows installer, however, it DOES NOT
INCLUDE DEPENDENCIES, such as python itself, pygame or pyOpenGL.
