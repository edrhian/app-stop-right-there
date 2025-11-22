import logging
import os.path
from typing import Tuple
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

from screens.rule_screen import RuleScreen
from screens.warning_screen import WarningScreen
from screens.confirmation_screen import ConfirmationScreen
from screens.window_title_display import WindowTitleDisplay

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

    def __init__(self, disabled_screen_id) -> None:
        super().__init__()
        self.disabled_screen = disabled_screen_id

        self.options = [
            Option(prompt="Home",id="home_screen"),
            Option(prompt="Window Title Display",id="window_title_display_screen"),
            Option(prompt="Configuration",id="configuration_screen")
        ]

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
        if target_screen == "home_screen":
            self.app.pop_screen()

        if target_screen == "window_title_display_screen":
            self.app.pop_screen()
            self.app.push_screen(WindowTitleDisplay())

        else:
            self.dismiss()
