"""
This script is used to test random aspects
of the 'placeholder' experiment.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from math import atan2, degrees

import time
import random


def deg2pix(deg):
    dpix = degrees(atan2(0.5 * 17.5, 50)) / (0.5 * 1080)
    return int(deg / dpix)
# bovenstaande waardes geven een dpix waarde van 0.018381...
# en dat is een logische waarde voor aantal visual degrees per pixel op het scherm
# Dat is ook logisch als je zegt dat de stimulus 1 visual degree moet zijn (see below)
# want dan bereken je nu het aantal pixels dat daarmee overeenkomt.


window = visual.Window(color=[0, 0.6, 1], size=[1920, 1080], units="pix", fullscr=True)

fixation_size = {
    "size": deg2pix(0.2),
    "line": deg2pix(0.2),
    "basecol": (0.2, 0.2, 0.2),
    "probecol": (0.9, 0.9, 0.9),
}

fixation_cross = visual.ShapeStim(
    win=window,
    vertices=(
        (0, -fixation_size["size"]),
        (0, fixation_size["size"]),
        (0, 0),
        (-fixation_size["size"], 0),
        (fixation_size["size"], 0),
    ),
    lineColor=[0, 0, 0],
    lineWidth=fixation_size["line"],
    closeShape=False,
    units="pix",
)

bar_stimulus_right = visual.Rect(
    win=window,
    units="pix",
    width=deg2pix(0.4),
    height=deg2pix(3),
    pos=[deg2pix(6), 0],
    fillColor="black",
    ori=random.randint(0,360),
)

bar_stimulus_left = visual.Rect(
    win=window,
    units="pix",
    width=deg2pix(0.4),
    height=deg2pix(3),
    pos=[-deg2pix(6), 0],
    fillColor="black",
    ori=random.randint(0,360),
)

fixation_cross.draw()
bar_stimulus_right.draw()
bar_stimulus_left.draw()
window.flip()
time.sleep(1)


fixation_cross.draw()

capture_cue = visual.Rect(
    win=window,
    units='pix',
    width=deg2pix(2),
    height=deg2pix(2),
    pos=(0,0),
    lineColor = 'red',
    lineWidth = deg2pix(0.1),
    fillColor = None,
)

capture_cue.draw()
window.flip()
time.sleep(2)
