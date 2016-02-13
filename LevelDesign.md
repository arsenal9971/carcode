# Introduction #

In this document I outline the designs and goals of carcode base levels, feel free to modify, comment or add specifications, this is a page to discuss the level design itself, it will be constantly updated with new additions and changes, it is not the final design (yet).


# Levels #

## Level 1: Entry ##

**Goal:** Let the user get familiar with car controls and basic car scripting.

**Level Objects**
  * Straight road, 800 units long, 50 units wide.
  * Finish line, placed at the end of the road

**Level Objectives**
  * Reach to the finish line
  * Don't get out of road.

**Notes:** The user will solve this one by simply accelerating the car constantly, he will just need to know how to call the acceleration functions and check the car speed.

## Level 2: Simple Paths ##

**Goal:** Let the user get familiar with sensor API and steering controls.

**Level Objects**
  * Looped road, something simple
  * Finish line or start line, for practical purposes is the same.

**Level Objectives**
  * Run the whole track.
  * Don't let the car go outside the road.

**Sensors:**
  * Two sensors in the front right and left of the car which should detect pixel color black (not the track color).

**Notes:** The user will need to keep check on car speed and accelerate when appropriate, he will need to use car sensors to know when the car is getting out of the track and to steer to recover correct curse.

## Level 3: Follow the line ##

**Goal:** Let the user practice the use of the sensor API and steering controls by making the car follow a thin line, this will prepare the user for next levels which will make use of color lines to guide the car.

**Level Objects**
  * Guide line, a thin line (a few pixels wide) that goes straight, with curves and other irregular shapes.
  * Finish point, an area at the end of the guide line where the car must reach.

**Level Objectives**
  * Follow the line
  * The car should always touch the line.

**Sensors**
  * Undecided

**Notes:** The user will have to create a script that lets the car steer following the line in many different situations.

## Level 4: Park the car ##

**Goal:** The user will use the past experiences to successfully lead the car to the parking area, this includes sensors, steering and engine/gears controls.

**Level Objects**
  * Parking objects, which are parking areas denoted by the usual white lines.
  * Guide line, a color line to help the user guide the car to the target parking area.

**Level Objectives**
  * Move the car to the red parking zone.
  * Have the car in horizontal position.
  * Shut down the engine to park.

**Sensors**
  * Undecided

**Notes:** The user could solve the problem following the guide line, detecting when has reached the parking area and park the car in the correct position.

## More coming soon ##