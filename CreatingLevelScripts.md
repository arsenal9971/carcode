# Introduction #

This is a guide with the essentials to build you own level scripts for carcode, from basic objects and sensors to collision detection, events, goals and objectives.

This is a guide by examples, for additional information refer to the API documents.

This documentation is based on latest code from subversion some interfaces may not be the same in previous releases but that will be signaled.

## How level scripts work ##

Carcode level scripts are plain python files, this means that you use standard python language features to define objects and its interactions with the environment and car.

The level script is loaded by carcode as if it where a normal python module (think of math module for example), then it will look for a class named LevelScript and proceed to create and instance of it.

On the main loop, carcode will call for the update function of this LevelScript instance.

So far design requirements are two, there must be a class named LevelScript which should contain a function named update (even if it does nothing).

Level setup (objects, goals, scoring) should be done within the constructor/initialization function of the LevelScript class (init), this function will be called without arguments as the environment supplies required objects.

The LevelScript may check environment state each frame in its update function, this function is called without arguments in the main loop if the game is running.

## Script environment ##

Carcode will provide the level script with a environment with all needed objects to manipulate the game world and add entities (objects) to it.

There is two main objects used to interact with the environment, Arena and Carcode, these are instances not classes and should be used directly, Arena manages the game entity list while Carcode manages events, goals and scoring.

### Base entities ###

Carcode provides a small set of common entities to construct levels, these include the Box class (to draw rectangles).

### Sensors ###

Carcode provides two basic sensors, the base Sensor class which will read the pixel color and return a tuple with the rgb components and the ColorSensor which will look for a specific color and will return a boolean depending if it detected the specified color.

### Custom entities ###

The level script can create custom entities by subclassing ccEntity (refer to libcarcode.physics API documentation).

Because carcode uses OpenGL internally to draw it will provide to the level script with all base OpenGL functions, refer to pyOpenGL API docs:

http://pyopengl.sourceforge.net/documentation/manual/reference-GL.html

# Simple objects #

```
class LevelScript:
  def __init__(self):
    box = Box(pos=(10, 10), size=(800, 50))
    Arena.add_entity(box)
  
  def update(self):
    pass
```

This is a simple script which only adds an object to carcode, there is the LevelScript class, the constructor instances Box which is an entity with a rectangular shape, we set the position for this entity (pos=(x,y)) and the size (size=(width, height)), finally we add this entity to the Arena object with the function add\_entity.

We add an empty update function as required, however we don't use it at the moment.


# Collision detection #

Carcore physics engine will test for collisions only between entities whose member collisionable is set to True, by default it set to False.

Physics engine does not keep track of collisions, when detecting one it will trigger an event, all entities contain the member evt\_collision, which is the event handler for collisions, you may add a function to it which will be called when the event collision is triggered for that object.

```
class LevelScript:
  def __init__(self):
    box = Box(pos=(500, 10), size=(50, 50))
    box.collisionable = True
    box.evt_collision.subscribe(self.onCollision)
    Arena.add_entity(box)
    self.boxcollision = False
  
  def onCollision(self, entity, colTest):
    print 'Object collided!'
    self.boxcollision = True
  
  def update(self):
    pass
```

This code creates a box entity and sets the collisionable flag to True, which means that we want carcode to test collision for that object. We subscribe the function onCollision from our class to box.evt\_collision, this function will receive 2 parameters, the first is the entity which triggered this event (box in this case), then a tuple of two booleans describing the results of collision test, the first boolean is whatever there was a collision (always true as the event is generated only when positive tests), and the second boolean is whatever the the object is completely contained in entity (for example the car inside a box).

As carcode physics engine does not keep track of collision results you may want to keep track of it inside a variable in your LevelScript, this will be useful later when using Goals and Scores.

# Sensors #

Providing sensors is essential for the user, thus the type and position of the sensors should be chosen carefully according the level design.

```
class LevelScript:
  def __init__(self):
    box = Box(pos=(500, 10), size=(50, 50))
    Arena.add_entity(box)
    sens = Sensor(24, 0)
    car = Arena.get_car()
    car.add_sensor("frontsensor", sens)
  def update(self):
    pass
```

This script creates an entity (Box) and a sensor which will be placed 24 units right of the car center and 0 pixels below the center, we get the car object from the Arena object and add the sensor to it, adding a sensor to a car needs two arguments, the name of the sensor and the sensor object, later on the user can lookup for an specific sensor by its name, be sure to use descriptive names.