# Overview #

In this summer of code the following features will be implemented:

  * Implement color trails
  * Implement car control API
  * Implement sensors to car API
  * Implement event tracking
  * Implement level creation format
  * Create driving tests
  * Add script editor
  * Add packaging

## Details ##

### Color trails ###

Basically have a colored line drawn whereever the car goes
in the screen, this line is not to be percibed by sensors,
it should be posible to turn on and off the drawing of
this line

### Car control API ###

Implement a simple and easy API to control the car, this
API should give the user access to all movement functions
of the car and sensors.

This API should be well documented.

### Sensor API ###

Implement a module for capturing pixel information on a given
position at user request, this position will be relative to
the car position. It will provide a simple and easy API
to access sensor data within the car API.

This API should be well documented.

### Event tracking ###

Implement event tracking, this will include car movement,
position, collision, etc.

### Level creation format ###

Implement a file format to describe all entities that
the car may interact with as well passing conditions
for that level.

This format should be well documented.

### Create driving test ###

Create a set of driving tests which demostrate the
level creation format and will introduce the user
to many features of the language.

### Add script editor ###

Add a simple editor in order to script the environment
or the car inside carcode.

### Add packaging ###

Package carcode in common packaging formats, such as
deb and rpm.


# Plans and Implementation #

### Color trails ###

To implement this feature I will be using an additional
surface exclusive for car trail.

Each time the car changes position a line will be drawn
between the initial position and the end position.

I could have also implemented this as dots, however,
tests shows that the trail is incomplete with this
method, as the movement of the car may be of more than
1 pixel, thus lines are more appropiate here.

### Car control API ###

I will add script execution support via python exec function
and pass a custom environment with relevant objects and
variables for the script to use.

We will need to create and proxy class to the main car
object, this is to avoid the user having direct access
with car internal data.

### Sensor API ###

I will implement a class for capturing pixel data, by
using the Surface function get\_at

### Event tracking ###

Pending

### Level creation format ###

The level format will be valid python files, which
will be executed with an special environment of
functions and proxy classes to setup the level
and conditions.

### Create driving test ###


### Add script editor ###

Using PGU

### Add packaging ###

Using existing python tools, such as distutils, I will
create an script to install carcode and
create packages in most common formats.


# Current Status #

Subversion revision [r56](https://code.google.com/p/carcode/source/detail?r=56)

### Color trails ###

There is already some basic code to do this in my subversion
branch.

### Car control API ###

On development

### Sensor API ###

On development

### Event tracking ###

On development

### Level creation format ###

There is already code to load the level, but we need
a complete API.

### Create driving test ###

On development

### Add script editor ###

On development

### Add packaging ###

There is already complete support for creating RPM, DEB
and Installer in my subversion branch.