#!/usr/bin/python
from libcarcode import CarcodeApp, Car
import sys
    
def main():
    app = CarcodeApp(800, 600)

    # Check if we have environment script
    if len(sys.argv) > 1:
        # Run level script
        app.run_script(sys.argv[1])
    else:
        # Setup default environment
        car = Car(app.screen)
        app.arena.set_car(car)
    app.main_loop()

if __name__ == '__main__':
    main()
