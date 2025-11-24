from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Header, Footer, Label, Input

from navigation.navigation_screen import NavigationScreen
from navigation.screen_list import SCREEN_LIST

class ConfigurationScreen(ModalScreen):

    BINDINGS = [
        ("t", "show_screen_nav", "Navigation Menu")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Label("Timer Settings", classes="title")
            yield Input(
                    placeholder="5",
                    id="input",
                    value=""
                )
        yield Footer()

    def action_show_screen_nav(self) -> None:
        """Toggle the sidebar visibility."""
        self.app.push_screen(NavigationScreen(disabled_screen_id="configuration_screen", screen_list=SCREEN_LIST))

    def on_input_changed(self, event: Input.Changed) -> None:
        """Changes values when modifying rule attributes from input components"""
        input_widget = event.input

        if input_widget.id == "input":
            self.input_var = input_widget.value
