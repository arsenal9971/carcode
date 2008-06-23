#!/usr/bin/python
from libcarcode import CarcodeApp, Car
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-l', '--level', dest='level',
    help='load an specific level file')
parser.add_option('-m', '--monkey', action='store_true', 
    dest='monkey', default=False,
    help='record and replay, monkey see monkey do.')
parser.add_option('-s', '--script', dest='script',
    help='load an specific script file')

(opts, args) = parser.parse_args()

def setup_level(app):
    # Check if we have environment script
    if opts.level:
        # Run level script
        car = Car()
        app.arena.set_car(car)
        app.run_script(opts.level)
    else:
        # Setup default environment
        car = Car()
        app.arena.set_car(car)
    if opts.script:
        car.set_script(opts.script)

def main():
    app = CarcodeApp(800, 600)
    
    setup_level(app)
    app.main_loop()
    if opts.monkey:
        setup_level(app)
        app.rerun()

if __name__ == '__main__':
    main()
