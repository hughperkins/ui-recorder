import chili

from prot import ui_events


def run():
    evts = []
    evts.append(ui_events.MouseScroll(123, 2.5))
    evts.append(ui_events.MouseClick())
    evts.append(ui_events.MouseMove([3, 20.5], 0.6))
    # encoder = chili.Encoder[Event]()
    # print(encoder.encode(e))
    for e in evts:
        print(chili.json_encode(e))
        print(chili.encode(e))


if __name__ == '__main__':
    run()
