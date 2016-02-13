Pixel color sensors are a simple way for a car to get feedback from the environment. They sense the colors of pixels on the background.

By putting sensors around the edges of a car, you can write code that will automatically steer it. For example, two sensors put at the front left and front right (like bug antennae) can be used to make the car follow a colored path.

The basic color sensor returns True if the background pixel that it is currently above matches one of the colors it senses, and False otherwise.

A more advanced radar-type color sensor works as follows. The sensor is aimed in a particular direction, and it returns the distance --- in pixels --- of the nearest pixel of a color that it senses. That is, it returns the length of the line drawn from the pixel sensor to the nearest pixel of the color it matches. If there is no matching color, then False is returned.

The sensors should allow for various kinds of configuration, such as limiting their range, or giving noisy feedback (to simulate real-world sensors).