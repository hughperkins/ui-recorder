"""
This version is designed for use on menus, where we want to smooth over the various hesitations and up/down scrolls,
whilst I'm trying to find the right options...

Things we want:
- if user was scrolling, and now clicks, then log the scroll and the click
- if user was scrolling, and now moves mouse, then log the scroll, and track the move
- if user moved the mouse, and now scrolls, then log the move, and track the scroll
- if user was moving mouse, and now clicks, then log the move, and the click
- user can use up and down keys to scroll
- scrolling with mouse scroll is not supported
- user can scroll right down to bottom, using 's', to ensure the scroll bar is in a known position,
  and then scroll up using up/down keys, to get to a known position

We also want to record keyboard stuff, but there are some specificities:
- ignore alt-tab, because I need to change between instructions and the app
- normal ascii keys, a-z, 0-9, I want
- not sure other stuff...
- simply filtering out alt-tab probably pretty good
- need to also filter out s though. hmmm
- should make it something else like eg ctrl-s or something. maybe ctrl-down?
- I also want a faster scroll. maybe add shift-up, shift-down?

Todo:
- add mouse drag
"""
import argparse
import json
import os
import sys
from typing import List, Optional, Set, Tuple, Type
from pynput import mouse, keyboard
import numpy as np
import time
import math
import chili

from ui_recorder import smooth_step, ui_events
from ui_recorder.speak import say


class Recorder:
    def __init__(self) -> None:
        self.events: List[ui_events.Event] = []

        # self.last_scroll_dir: Optional[int] = None
        self.total_scroll_dy = 0
        self.last_mouse_pos: Optional[Tuple[int, int]] = None
        self.typing_so_far = ""

        self.mouse_c = mouse.Controller()
        self.keyboard_c = keyboard.Controller()

        self.done = False
        self.abort = False

        self.keys: Set[keyboard.Key | keyboard.KeyCode] = set()

    def on_move(self, x, y):
        pass

    def record_event(self, evt: ui_events.Event) -> None:
        self.events.append(evt)
        print(evt)

    def finish_any_started_events(self, exclude_type: Optional[Type[ui_events.Event]]) -> None:
        # print('finish_any_started_events', exclude_type, ui_events.MouseScroll,
        # type(exclude_type), type(ui_events.MouseScroll))
        did_action = False
        if (
            self.last_mouse_pos is not None and
            self.last_mouse_pos != self.mouse_c.position and
            exclude_type != ui_events.MouseMove
        ):
            print('adding move from unfinished')
            self.record_move()
            self.last_mouse_pos = self.mouse_c.position
            did_action = True
        if self.total_scroll_dy is not None and self.total_scroll_dy != 0 and exclude_type != ui_events.MouseScroll:
            evt: ui_events.Event = ui_events.MouseScroll(dy=self.total_scroll_dy, duration_secs=1)
            print('from unfinished', evt)
            self.events.append(evt)
            self.total_scroll_dy = 0
            did_action = True
        if self.typing_so_far != "" and exclude_type != ui_events.Typing:
            evt = ui_events.Typing(text=self.typing_so_far)
            print('from unfinished', evt)
            self.events.append(evt)
            self.typing_so_far = ""
            did_action = True
        if did_action:
            self.finish_any_started_events(exclude_type=None)

    def on_click(self, x, y, button, pressed):
        if pressed:
            print('mouse click')
            self.finish_any_started_events(exclude_type=ui_events.MouseClick)
            # if self.total_scroll_dy != 0:
            #     evt = ui_events.MouseScroll(dy=self.total_scroll_dy, duration_secs=1)
            #     print(evt)
            #     self.events.append(evt)
            #     self.total_scroll_dy = 0
            # self.record_event(ui_events.MouseMove(self.mouse_c.position, 1))
            self.record_event(ui_events.MouseClick())

    def record_move(self):
        evt = ui_events.MouseMove(self.mouse_c.position, 1)
        print(evt)
        self.events.append(evt)

    def record_scroll(self):
        self.record_event(ui_events.MouseScroll(self.total_scroll_dy, 1))
        self.total_scroll_dy = 0

    def on_scroll(self, x, y, dx, dy):
        return
        # say('You moved the mouse wheel. aborting')
        # self.abort = True
        # sys.exit(0)
        sys.exit(0)
        sys.exit(0)
        if self.last_mouse_pos is None or self.last_mouse_pos != self.mouse_c.position:
            self.record_move()
            self.last_mouse_pos = self.mouse_c.position
        if dy == 0:
            return
        self.total_scroll_dy += dy

    def do_scroll(self, dy):
        if dy == 0:
            return
        self.finish_any_started_events(exclude_type=ui_events.MouseScroll)
        # if self.last_mouse_pos is None or self.last_mouse_pos != self.mouse_c.position:
        #     # if self.total_scroll_dy != 0:
        #     self.record_move()
        #     self.last_mouse_pos = self.mouse_c.position
        self.total_scroll_dy += dy
        self.mouse_c.scroll(0, dy)

    def immediate_large_scroll_down(self):
        self.finish_any_started_events(exclude_type=ui_events.MouseScroll)
        # if self.last_mouse_pos is None or self.last_mouse_pos != self.mouse_c.position:
        #     self.record_move()
        #     self.last_mouse_pos = self.mouse_c.position
        if self.total_scroll_dy is None:
            self.total_scroll_dy = -1000
        else:
            self.total_scroll_dy -= 1000
        self.mouse_c.scroll(0, -1000)
        self.record_scroll()

    def on_press(self, key):
        self.keys.add(key)
        # if (
        #     keyboard.Key.ctrl_l in self.keys and
        #     keyboard.Key.shift_l in self.keys and
        #     len(self.keys) == 3
        # ):
        # print('key down', key)
        if isinstance(key, keyboard.KeyCode):
            ...
            # if key.char == 's':
        elif isinstance(key, keyboard.Key):
            if key == keyboard.Key.up:
                if keyboard.Key.shift_l in self.keys:
                    # print('up with shift')
                    self.do_scroll(5)
                else:
                    self.do_scroll(1)
            elif key == keyboard.Key.down:
                # print('keys', self.keys)
                if keyboard.Key.cmd_l in self.keys:
                    # print('down with cmd')
                    self.immediate_large_scroll_down()
                elif keyboard.Key.shift_l in self.keys:
                    # print('down with shift')
                    self.do_scroll(-5)
                else:
                    self.do_scroll(-1)

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.finish_any_started_events(exclude_type=None)
            self.done = True
        if key != keyboard.Key.tab:
            if isinstance(key, keyboard.KeyCode):
                self.finish_any_started_events(exclude_type=ui_events.Typing)
                c = key.char
                if c is not None:
                    self.typing_so_far += c
        self.keys.discard(key)

    def smooth_move_to(self, new_pos, duration: float = 1, ease: bool = True):
        start = time.time()
        start_pos = np.array(self.mouse_c.position)
        dt = (time.time() - start) / duration
        while dt < duration:
            dt_smooth = smooth_step.smoothstep_f(0, 1, dt)
            self.mouse_c.position = new_pos * dt_smooth + (1 - dt_smooth) * start_pos
            dt = (time.time() - start) / duration
        self.mouse_c.position = new_pos

    def record(self, filepath: str) -> None:
        self.done = False
        self.mouse_l = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)

        self.keyboard_l = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

        self.mouse_l.start()
        time.sleep(0.1)
        self.keyboard_l.start()
        self.last_mouse_pos = self.mouse_c.position
        print('started')
        say('started')

        while not self.done and not self.abort:
            time.sleep(0.1)

        self.mouse_l.stop()

        if self.abort:
            self.keyboard_l.stop()
            print('aborted')
            sys.exit(-1)

        print('finished recording')
        say('finished recording')

        # encoder = chili.Encoder[Event]()
        for evt in self.events:
            print('chili.encode', chili.encode(evt))

        events_dicts = [chili.encode(evt) for evt in self.events]
        print(events_dicts)
        with open(filepath, 'w') as f:
            # f.write(json.dumps(events_dicts, indent=2))
            f.write("[\n")
            for evt_dict in events_dicts:
                f.write(json.dumps(evt_dict) + "\n")
            f.write("}\n")

        os.system(f"cat {filepath}")

        # self.done = False
        # while not self.done:
        #     time.sleep(0.1)

    def replay(self, filepath: str) -> None:
        with open(filepath) as f:
            evt_dicts = json.load(f)
        evt_objs = [chili.decode(evt_dict, getattr(ui_events, evt_dict['class_type'])) for evt_dict in evt_dicts]
        print('evt_objs', evt_objs)
        self.events = evt_objs

        self.keyboard_l = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.keyboard_l.start()
        while not self.done:
            time.sleep(0.1)
        self.keyboard_l.stop()

        self.playback()

    def playback(self) -> None:
        say('replaying')
        done = False

        for evt in self.events:
            if done:
                say('exiting')
                sys.exit(-1)
            if isinstance(evt, ui_events.MouseMove):
                print('start move')
                # say('move')
                self.smooth_move_to(np.array(evt.pos), duration=1)
                print('end move')
                time.sleep(0.5)
            elif isinstance(evt, ui_events.MouseClick):
                print('start click')
                # say('click')
                self.mouse_c.click(mouse.Button.left)
                print('after click')
                time.sleep(0.1)
            elif isinstance(evt, ui_events.MouseScroll):
                print('scroll', evt.dy)
                # say('scroll')
                length = int(math.fabs(evt.dy))
                direction = 1 if evt.dy > 0 else -1
                print('length', length, 'direction', direction)
                for n in range(length):
                    self.mouse_c.scroll(0, direction)
                    time.sleep(1.0 / length)
                print('after scroll')
                time.sleep(0.5)
            elif isinstance(evt, ui_events.Typing):
                print('text', evt.text)
                for c in evt.text:
                    self.keyboard_c.press(c)
                    time.sleep(0.1)
            elif isinstance(evt, ui_events.Pause):
                print('pause')
                time.sleep(evt.duration_secs)
            else:
                say(f"Unknown event {evt.class_type}")
                raise Exception(f"Unknown event {evt.class_type}")

        say('replay finished')

    # def run(self) -> None:
    #     self.record()
    #     self.playback()


def run(args: argparse.Namespace) -> None:
    recorder = Recorder()
    if args.first_replay is not None:
        for filepath in args.first_replay:
            print(filepath)
            recorder.replay(filepath=filepath)
    recorder.record(filepath=args.filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--first-replay', nargs='+', type=str, help='list of json files to reply first')
    parser.add_argument("--filepath", type=str, required=True)
    args = parser.parse_args()
    run(args)
