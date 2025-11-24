from typing import List, Type, TypedDict
from textual.screen import Screen

class ScreenItem(TypedDict):
    id: str
    prompt: str
    screen_class: Type[Screen] | None

SCREEN_LIST: List[ScreenItem] = [
    {
        "id": "home_screen",
        "prompt": "Home Screen",
        "screen_class": None
    },
    {
        "id": "window_title_display",
        "prompt": "Window Title Display",
        "screen_class": None
    },
]
