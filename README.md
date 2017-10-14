# readtime
Python 2.7 program to read analog time through image processing techniques using OpenCV 2.
This program works on the basis of the difference in HSV values of the clock hands and anything else in the frame. Hence the color of the hands of the clock need to be different from anything else in the image, and the colour of both clock hands must be the same.
Initial screen:
![Startup screen on running timeread.py](https://raw.github.com/anishmrao/readtime/master/timeread1.png)
On aligning the meeting point of the clock hands with the blue dot and keeping the vertical diagonal as the 12-6 line, press SPACE.
Click either of the clock hands to give the right color (HSV value) of the clock hands.
![Result window](/timeread2.png?raw=true)
The above window with the result will appear on click, if the input is valid.
