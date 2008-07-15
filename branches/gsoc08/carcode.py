#!/usr/bin/python
from libcarcode import CarcodeApp, Car
import sys
from optparse import OptionParser

VERSION = "3.0a1"

parser = OptionParser()
parser.add_option('-l', '--level', dest='level',
    help='load an specific level file')
parser.add_option('-v', '--version', action='store_true', 
    dest='version', default=False,
    help='display carcode version and exit.')
parser.add_option('-s', '--script', dest='script',
    help='load an specific script file')

(opts, args) = parser.parse_args()

def setup_level(app):
    # Check if we have environment script
    if opts.level:
        # Run level script
        app.load_level(opts.level)
    if opts.script:
        app.load_script(opts.script)

def main():
    if opts.version:
        print "carcode",  VERSION
        sys.exit(0)
        
    app = CarcodeApp(800, 600)
    
    setup_level(app)
    app.main_loop()

if __name__ == '__main__':
    main()
