EyeSpy!
=======
by David Su (http://usdivad.com/)

### About
This feature extractor, adapted from Shantnu Tiwari's "Webcam-Face-Detect" code (https://github.com/shantnu/Webcam-Face-Detect), uses the OpenCV library to detect the presence of eyes. It then performs some calculations to extract the following features:

    1. Number of eyes detected
    2. Average area of eyes
    3. Distance between left and right eye
    4. Left eye x-coordinate
    5. Left eye y-coordinate
    6. Right eye x-coordinate
    7. Right eye y-coordinate

If only one eye is detected, features 3, 6, and 7 will be 0. If no eyes are detected, features 3-7 will be 0. If more than two eyes are detected, the two left-most eyes (i.e. lowest x-coordinates) will be used as the left and right eye, although all eye areas will be used for calculating feature 2.

Messages are sent via the pyOSC library, connecting to IP address `127.0.0.1` and port `6448` (the port that Wekinator listens to by default).

For "Machine Learning for Musicians and Artists", offered by Goldsmiths University of London + Kadenze.

The GitHub repo for this project can be found at: https://github.com/usdivad/EyeSpy


### Usage
`python eyespy.py`

^ By default this uses the stump-based 20x20 frontal eye detection Haar classifier, included with OpenCV. To use a custom cascade classifier, enter `python eyespy.py <classifier_path>`. Some other classifiers can be found in the **cascades** directory.

**EyeSpyTest** includes a Wekinator project that is already (somewhat) trained; you can use it to test the feature extractor straight out of the box!


### Possible use cases:
- We can detect how many people are present in the scene using feature 1. This in turn can be used for implementing social aspects of an artwork, e.g. only triggering certain events when more than one person is present.
- Features 2 and 3 can in combination be used to estimate the proximity of the user(s). This can be used for continuous control over, for example, an audio filter that changes with respect to proximity.
- Features 3-7 can be used for positional detection, from which velocity and acceleration can then be calculated. These can be then be used for a variety of classification tasks, much like the WhichFace example input program



### Installation
This feature extractor depends on:
- Python
- pyOSC
- OpenCV

To install Python, follow the instructions for your OS at: https://www.python.org/downloads/

To install pyOSC, simply enter `pip install pyosc` (or `pip install pyosc --pre` for Python 2.x). 

For OpenCV, I was able to just follow the instructions on this site (http://www.jeffreythompson.org/blog/2013/08/22/update-installing-opencv-on-mac-mountain-lion/). The commands amount to:

    brew tap homebrew/science
    brew install --with-tbb opencv
    

However, some dependencies might be missing; I found this site (http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/) to be helpful on that front, although you'll want to use version 2.4.x instead of 3.0.0. Step 6 lists the Homebrew commands for installing the required packages and developer tools.

If none of these work for you, head over to the OpenCV downloads page (http://opencv.org/downloads.html) and see if that helps. Make sure to select the correct operating system!