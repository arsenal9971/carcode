from distutils.core import setup
import sys
import os

# If we want debian package, build it and exit
if 'bdist_deb' in sys.argv:
    print "Building debian package with debuild"
    os.system("debuild -us -uc")
    print "Finished bulding package"
    sys.exit(0)

# Setup base 'setup' arguments as a dictionary
setup_args = dict(
    name = "carcode",
    version = "0.1",
    description = "Learn Python programming using an animated car",
    long_description = """
    carcode is an experiment in programming education.
    The idea is to give beginning programmers carcode, 
    which provides an animated car they can drive around 
    the screen either using the keyboard, or 
    programmatically through a simple API.""",
    
    license = "GPLv2",
    keywords = "python pygame education carcode",
    url = "http://code.google.com/p/carcode/",
    
    packages = ['libcarcode', 'libcarcode.media', 'libcarcode.media.sound', 'libcarcode.media.images'],
    scripts = ['carcode.py'],
    package_data = {
        '': ['*.png', '*.wav']
    },
    install_requires = ['pygame']
    )


# If we want to use py2exe add the appropiate arguments
# to setup
if 'py2exe' in sys.argv:
    print "Building Windows Executable"
    setup_args['windows'] = ['carcode.py']
    import py2exe

# Run setup and unfold setup_args as arguments
setup(**setup_args)

