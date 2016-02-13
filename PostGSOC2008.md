# Introduction #

This document outlines some of the future work that will be done for the current code base which was created as part of the GSoC 2008, this is a place for discussion too.


# Levels #

There is still a lot of work to do with levels, basically Beta 1 only has 3 levels, there is the need to make more, there is already a list of planned levels I should keep working with that while finding new ideas for more levels.

# Engine #

## Physics ##

Currently 2D physics engine is flaky, has many corner cases and needs to be revamped, probably by swaping it for a solid preexisting library, like Box2D, there is work done on a basic 2D physics engine for pygame from this GSoC too, I will check it out to see of we could use that or adapt it.

## Timers ##

My plan is to implement a global scheduler to coordinate rendering, input processing and timers, this will enable us to do many things a lot easier (such animations).

The basic idea is to have a class with a list of Tasks or Timers, each task has a previously specified amount of time which it should wait before runing. The scheduler will just iterate trough this list and run tasks that are due, this however, does not imply multithreading.

## Layering ##

Rendering should be divided by layers, the ground layer, the car layer and the top layer, this is important as the layers are drawn in order, pixel sensors will only see the ground layer.

# Optimizations #

## GUI ##

The small OpenGL based GUI toolkit for carcode is very unoptimized, we could make use of vertex buffers (glDrawElements) and compiled lists to make it faster (by reducing the calls to glBegin, glColor, glVertex and friends).

Text editor is very inefficient, I should clean the event code to make it faster, make use of compiled lists for font rendering.

Images are very heavy, they are basically an array of vectors of with colors in a compiled list, this wastes a lot of video memory as it stores vector coordinates (x, y) and color components (r, g, b and posibly alpha), which could take as much as 16 bytes per pixel in a 32 bit machine using 32 bit floats for vertex position and a byte per color, there are other ways to do it. Altough most video cards are very efficient at pushing pixels, even some IGPs.