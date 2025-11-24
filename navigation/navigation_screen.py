import logging
import os.path
from typing import List, Sequence, Tuple, TypedDict
from textual.app import App, ComposeResult
import textual
from textual.widgets import Footer, Header, DataTable, OptionList, Label
from textual import work, on
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets.option_list import Option
from textual.containers import Vertical
from core.window_manager import watch_screen_title
from core.rule_manager import manager
from core.rule import Rule
from navigation.screen_list import ScreenItem

class NavigationScreen(ModalScreen):
    
    DEFAULT_CSS = """
        OptionList {
            align: center middle;
        }
        Label.header1 {
            margin: 1;
            text-style: bold;
        }
        Vertical.nav_container {
            width: 60%;
            height: 70%;
        }
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
        ("s", "app.pop_screen", "Cancel")
    ]

    def __init__(self, disabled_screen_id: str, screen_list: Sequence[ScreenItem]) -> None:
        super().__init__()
        self.disabled_screen = disabled_screen_id

        self.screen_list = screen_list

        self.options = []

        for screen in self.screen_list:
            self.options.append(Option(prompt=screen['prompt'], id=screen['id']))

        for option in self.options:
            if option.id == disabled_screen_id:
                option.disabled = True
                return

    def compose(self):
        with Vertical(classes="nav_container"):
            yield Label("Screen Navigator",classes="header1")
            option_list = OptionList()
            option_list.add_options(self.options)
            yield option_list

    def on_option_list_option_selected(self, message: OptionList.OptionSelected):
        target_screen = message.option.id

        for screen in self.screen_list:
            if screen["id"] == target_screen:
                screen_class = screen["screen_class"]

                if screen_class is None:
                    while len(self.app.screen_stack) > 1:
                        self.app.pop_screen()
                    return
                
                self.app.push_screen(screen_class())
                return

        self.dismiss()
