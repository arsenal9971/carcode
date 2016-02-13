Things to do for carcode, approximately in the order they ought to be done:

  * Add an optional colored "trail" to the car (as in turtle graphics) so we can see the path the car has followed. Use different colors for forwards and backwards (assuming that looks good on screen).

  * Create an API for controlling the car that is **simple enough for beginning programmers to understand and use**. It should give access to all the features of the car.

  * Create pixel color sensors for the car. These return the color of the pixel they are above, and there should probably be at least four: two at the front of the car, and two at the back.

  * Track statistics such as: total time spent on a task; total distance traveled forward/backward; total distance turned left/right; number of forward/reverse gear switches; number of times break/accelerator was used; number of times the horn was honked; total time spent with the engine running (e.g. important for gas consumption!); number of yellow lines/obstacles run over.

  * Statistics and tasks should be tracked over time. For now, we assume there is only a single user, and will store all their result and statistics via pickling.

  * Create a series of "driving test" challenges, each corresponding to a small programming task suitable for a beginner. The first few should not be hard at all, but should be designed to give users experience using the API. Gradually, the tasks can get more challenging, culminating in the user earning their "carcode license". Indeed, as with a real driving test, the final test could combine all the previous tests into one big final test.

  * Automatically recognize when a task is performed. For example, suppose the task is to back into a parking spot. The location where the car should end up could be colored green (or whatever color looks good on the screen), and the system automatically knows both when the car is on the green spot, and facing the correct direction. Then it checks that other rules have been met, e.g. perhaps there is a limit of 3 forward/reverse gear switches.

  * Add a "replay" feature that re-runs a particular carcode session so users can watch it again. This is also very useful for creating demos to show people what carcode is like.

  * Improve the graphics. This could be done in many different ways, for example:

  * Using pygame, make the car look more like a car, and the road more like a road. Realism is not necessarily important, but a fun, good-looking style is (e.g. cartoon cars are fun).

  * Using pygame, allow for maps bigger than the screen using scrolling.

  * Re-do the entire graphics front end in 2.5/3D, perhaps using [pyglet](http://www.pyglet.org/) or [PySoy](http://www.pysoy.org/).