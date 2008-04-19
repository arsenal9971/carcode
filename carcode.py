#!/usr/bin/python
from libcarcode import CarcodeApp, Car

def main():
    app = CarcodeApp(800, 600)
    car = Car(app.screen)
    app.arena.set_car(car)
    app.main_loop()

if __name__ == '__main__':
    main()
