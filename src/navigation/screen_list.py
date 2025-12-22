"""Screen List"""
from typing import List, Type, TypedDict
from textual.screen import Screen

class ScreenItem(TypedDict):
    """Data structure required to display and navigate between screens in NavigationScreen"""
    id: str
    prompt: str
    screen_class: Type[Screen] | None

SCREEN_LIST: List[ScreenItem] = [
    {
        "id": "home_screen",
        "prompt": "Home",
        "screen_class": None
    },
    {
        "id": "window_title_display",
        "prompt": "Window Title Display",
        "screen_class": None
    },
    {
        "id": "configuration_screen",
        "prompt": "Configuration",
        "screen_class": None
    },
    {
        "id": "documentation",
        "prompt": "App Documentation",
        "screen_class": None
    },
]
