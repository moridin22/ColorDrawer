# ColorDrawer
A ColorDrawer allows the user to draw on top of a webcam feed using a 'wand'.

## Getting Started

### Prerequisites
The modules numpy and opencv must be installed for python 3; the easiest way to install these modules is to download the anaconda distribution of python, available [here](https://www.continuum.io/downloads).
For best results, a wand with a sizable spherical tip and distinct color
should be used. http://imgur.com/xLqXhjE provides a good example.

### Usage
Simply run `colordrawer.py`. For best results, a wand with a sizable spherical tip and distinct color should be used. http://imgur.com/xLqXhjE provides a good example.

### Hotkeys:
c -> Clears the screen.

d -> Segments the drawing. Pressing 'd' toggles the drawing.

e -> Erases one segment of the drawing.

h -> Recalibrates the hsv values to the mean of the calibration rectangle.

q -> Quits the program.

r -> Toggles the calibration rectangle.

s -> Cycles through the colors.
