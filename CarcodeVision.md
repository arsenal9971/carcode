carcode is intended as a tool for helping beginners learn to program in Python. It simulates a two-dimensional robotic car that you must write programs to control and do simple tasks, such as parking.

It can be thought of as an extension of turtle graphics, similar in some ways to [Squeak](http://www.squeak.org/) or Java's [Robocode](http://robocode.sourceforge.net/). However, both of those projects are relatively complex, and have a relatively steep learning curve.

Currently a basic user-driven version has been created allowing the user to drive the car around the screen.

The next features to implement include:

  * Add different kinds of PixelColorSensors. These can be used by the car to help steer it automatically, to find yellow lines, etc. [Squeak](http://www.squeak.org/) provides something similar (indeed, [Squeak](http://www.squeak.org/) could be a good source of ideas for other features to add).

  * Simple crash modeling would fun, i.e. when two solid objects come into contact at least one should be dented or crumple.

  * Create a GUI that makes it easy to select different kinds of backgrounds, customize the details of the car, etc.

  * Create a super simple, easy to understand API that can be used by beginners to write cool and interesting programs. It should let the programmer access all the basic car features. Clear and complete documentation is important here.

  * Demo programs and tutorials --- suitable for beginners --- need to be written. A nice idea for this is to create a series of challenge that for a drivers test, culminating in programmers earning their carcode driver's license.

  * Graphical extensions, such as more car details (customization?), environmental details such as traffic lights, puddles, pedestrians, lamp posts, other cars, etc. Indeed, many features that you see in other car games or the like could be added, but, ideally, they should all be things that a beginning programmer can easily understand and interact with via the car they are controlling.

  * 2D is nice, but 2.5D (e.g. like [Roller Coaster Tycoon](http://www.atari.com/rollercoastertycoon/)) might be an appealing improvement. Possibly full-blown 3D might also be used, but the problem with 3D is that simply navigating and moving around could get in the way and make it less useful as an educational tool. Perhaps [pyglet](http://www.pyglet.org/) or [PySoy](http://www.pysoy.org/) could be used for this?

  * Make the downloading and installation of carcode as simple, pleasant, and anguish-free as possible. Nothing frustrates beginners more than software that is difficult to even get running.

NextSteps suggests a slightly more detailed list of things to do.