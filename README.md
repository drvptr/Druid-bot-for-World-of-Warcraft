The idea is this.
The addon transmits the player’s coordinates using color. It displays two colored cubes on the screen, and the HEX color values of those cubes represent the coordinates. The script listener.py captures the window, reads the color from these cubes, and outputs the coordinates.

This is necessary in order to build a program based on a PID-controller concept, which would regulate the error and prevent the character from getting stuck on obstacles. There are also some experiments related to computer vision here: a neural network was trained to detect leystones in Legion zones.
