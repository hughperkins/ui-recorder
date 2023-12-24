from dataclasses import dataclass
from typing import List, Tuple, cast


@dataclass
class Event:
    class_type: str

    def __init__(self):
        # print('event init', self.__class__.__name__)
        self.class_type = self.__class__.__name__


@dataclass
class MouseMove(Event):
    pos: Tuple[float, float]
    duration_secs: float

    def __init__(self, pos: Tuple[float, float] | List[float], duration_secs: float) -> None:
        super().__init__()
        self.pos = cast(Tuple[float, float], tuple(pos))
        self.duration_secs = duration_secs

    def __str__(self) -> str:
        return f'MouseMove(pos={self.pos})'


@dataclass
class Pause(Event):
    duration_secs: float

    def __init__(self, duration_secs: float) -> None:
        super().__init__()
        self.duration_secs = duration_secs

    def __str__(self) -> str:
        return 'Pause()'


@dataclass
class Typing(Event):
    text: str

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return f'Typing(text={self.text})'


@dataclass
class MouseClick(Event):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return 'MouseClick()'


@dataclass
class MouseScroll(Event):
    dy: int
    duration_secs: float

    def __init__(self, dy: int, duration_secs: float) -> None:
        super().__init__()
        self.dy = dy
        self.duration_secs = duration_secs

    def __str__(self) -> str:
        return f'MouseScroll(dy={self.dy})'
