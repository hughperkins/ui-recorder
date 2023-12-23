# ui-recorder
Record ui to json file, playback from it. Ignores your random pauses and stuff, whilst you read the instructions.

This app fuses consecutive actions of the same type (except mouse clicks) together, into single actions.

You can edit the recording, before playing it back.

By default, fused actions are fused into actions of 1 second, for mouse scrolls, and mouse moves.

Typing is played back at 10 characters per second. (about 120 wpm)

*Note: only support Mac OS X*.
- tested on Sonoma, using a MacBook Air M2 (but I imagine it should run on any recent-ish Mac?)

## Currently supported actions

Actions supported:
- typing (fused into a single Typing event, with the entire string)
    - currently only supports lowercase a-z an 0-9
- mouse move
- mouse click, with left button
- mouse scroll, BUT, do NOT use the scroll wheel, it will lead to inconsistencies
    - to scroll a bit, use up and down arrows
    - to scroll up or down faster, use shift + up/down arrows
    - to scroll massively, to ensure you start at a known scroll position, use command + down

## Installation:

- clone this repo, and cd into the root of this repo
- if you have poetry, run `poetry install`
- otherwise, use pip: `pip install .`, or `pip install -e .`, as you prefer

## To record:
- from the root of this cloned repo, run:
```
python prot/record.py --filepath [filepath where your output will be recorded as json]
```
- alt-tab over to your application
- press 'escape'
    - you should hear 'recording started'
- start doing stuff :)
- when you're finished, hit escape again
    - you should hear 'recording finished'

Note that alt-tab is ignored, so you can freely switch backwards and forwards between your instructions, and the application you are recording.

## To playback

- from the root of this cloned repo, run:
```
python prot/replay.py --filepath [filepath to recorded json]
```
- alt-tab over to your application
- press 'escape'
    - you should hear 'replay started'
- once finished, you should hear 'replay finished'
