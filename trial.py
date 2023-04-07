"""
This file contains the functions necessary for
creating and running a single trial start-to-finish,
including eyetracker triggers.
To run the 'null-cue gaze bias' experiment, see main.py.

made by Anna van Harmelen, 2023
"""

from psychopy import visual
from psychopy.core import wait
from time import time, sleep
from response import get_response
from stimuli import (
    create_fixation_cross,
    create_capture_cue_frame,
    create_stimuli_frame,
)
import random

# experiment flow:
# 1. fixatiekruis
# 2. fixatiekruis + twee blokkies ernaast
# 3. fixatiekruis
# 4. fixatiekruis + vierkantje om het kruis
# 5. fixatiekruis
# 6. probecue
# 7. dials voor respons van proefpersoon

COLOURS = ["#ff99ac", "#f5e2a3", "#a8f0d1", "#99ceff"]


def generate_stimuli_characteristics(condition, target_bar):
    neutral_colour, *stimuli_colours = random.sample(COLOURS, 3)

    orientations = [
        random.choice([-1, 1]) * random.randint(5, 85),
        random.choice([-1, 1]) * random.randint(5, 85),
    ]

    if target_bar == "left":
        target_colour, distractor_colour = stimuli_colours
        target_orientation = orientations[0]
    else:
        distractor_colour, target_colour = stimuli_colours
        target_orientation = orientations[1]

    if condition == "congruent":
        capture_colour = target_colour
    elif condition == "incongruent":
        capture_colour = distractor_colour
    elif condition == "neutral":
        capture_colour = neutral_colour

    return {
        "stimuli_colours": stimuli_colours,
        "capture_colour": capture_colour,
        "trial_condition": condition,
        "left_orientation": orientations[0],
        "right_orientation": orientations[1],
        "target_bar": target_bar,
        "target_colour": target_colour,
        "target_orientation": target_orientation,
    }


def do_while_showing(waiting_time, something_to_do, window):
    """
    Show whatever is drawn to the screen for exactly `waiting_time` period,
    while doing `something_to_do` in the mean time.
    """
    window.flip()
    start = time()
    something_to_do()
    wait(waiting_time - (time() - start))


def single_trial(
    left_orientation,
    right_orientation,
    target_bar,
    target_colour,
    target_orientation,
    stimuli_colours,
    capture_colour,
    trial_condition,
    settings,
    testing,
    eyetracker=None,
):
    screens = [
        (0, lambda: 0 / 0, None),  # initial one to make life easier
        (0.1, lambda: create_fixation_cross(settings), None),
        (
            0.25,
            lambda: create_stimuli_frame(
                left_orientation, right_orientation, stimuli_colours, settings
            ),
            "stimuli_onset",
        ),
        (0.75, lambda: create_fixation_cross(settings), None),
        (
            0.25,
            lambda: create_capture_cue_frame(capture_colour, settings),
            "capture_cue_onset",
        ),
        (1.75, lambda: create_fixation_cross(settings), None),
        (
            None,
            lambda: create_fixation_cross(settings, target_colour),
            "probe_cue_onset",
        ),
    ]

    # !!! The timing you pass to do_while_showing is the timing for the previously drawn screen.

    for index, (duration, _, frame) in enumerate(screens[:-1]):
        # Send trigger if not testing
        if not testing and frame:
            trigger = get_trigger(frame, trial_condition, target_bar)
            eyetracker.tracker.send_message(f"trig{trigger}")

        # Draw the next screen while showing the current one
        do_while_showing(duration, screens[index + 1][1], settings["window"])

        if not testing and frame:
            eyetracker.tracker.send_message("trigOFF")

    if not testing:
        trigger = get_trigger("response_onset", trial_condition, target_bar)
        eyetracker.tracker.send_message(f"trig{trigger}")

    response = get_response(target_orientation, target_colour, settings)

    if not testing:
        trigger = get_trigger("response_offset", trial_condition, target_bar)
        eyetracker.tracker.send_message(f"trig{trigger}")

    # Show performance
    create_fixation_cross(settings)
    show_text(
        f"{response['performance']}", settings["window"], (0, settings["deg2pix"](0.5))
    )

    if not testing:
        trigger = get_trigger("feedback_onset", trial_condition, target_bar)
        eyetracker.tracker.send_message(f"trig{trigger}")
    settings["window"].flip()
    sleep(0.8)

    return response


def get_trigger(frame, condition, target_position):
    condition_marker = {
        "congruent": 1,
        "incongruent": 3,
        "neutral": 5
    }[condition]

    if target_position == "right":
        condition_marker += 1

    return {
        "stimuli_onset": "",
        "capture_cue_onset": "1",
        "probe_cue_onset": "2",
        "response_onset": "3",
        "response_offset": "4",
        "feedback_onset": "5",
    }[frame] + str(condition_marker)


def show_text(input, window, pos=(0, 0), colour="#ffffff"):
    textstim = visual.TextStim(
        win=window, font="Courier New", text=input, color=colour, pos=pos, height=24
    )

    textstim.draw()
