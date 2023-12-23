import argparse

from ui_recorder import record


def run(args: argparse.Namespace) -> None:
    recorder = record.Recorder()
    recorder.replay(filepath=args.filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", type=str, required=True)
    args = parser.parse_args()
    run(args)
