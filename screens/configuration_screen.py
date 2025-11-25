from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Header, Footer, Label, Input, Button
from textual.reactive import reactive
from textual.validation import Number

from config.config import load_config, save_config
from navigation.navigation_screen import NavigationScreen
from navigation.screen_list import SCREEN_LIST

class ConfigurationScreen(ModalScreen):

    AUTO_FOCUS = "Label"

    BINDINGS = [
        ("t", "show_screen_nav", "Navigation Menu")
    ]

    def on_mount(self):
        self.config = load_config(path="config/config.yaml")
        self.duration = self.config['timer']['duration_seconds']

        duration_input = self.query_one("#duration_input", Input)
        duration_input.value = str(self.duration)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Label("Timer Settings", classes="title")
            yield Label("Duration",classes="body_text")
            yield Label("(how much time you have to wait before the dismiss button appears when breaking a rule)",
                        classes="subtitle")
            yield Input(
                    placeholder=f"Duration",
                    id="duration_input",
                    value="",
                    type="integer",
                    validators=[
                        Number(minimum=1)
                    ]
                )
            yield Button(variant="success", label="Save Changes",id="save_config_button")
        yield Footer()

    def action_show_screen_nav(self) -> None:
        """Toggle the sidebar visibility."""
        self.app.push_screen(NavigationScreen(disabled_screen_id="configuration_screen", screen_list=SCREEN_LIST))

    def on_input_changed(self, event: Input.Changed) -> None:
        """Changes values when modifying rule attributes from input components"""

        validation_result = event.validation_result

        save_config_button = self.query_one("#save_config_button", Button)

        if validation_result is None or not validation_result.is_valid:
            save_config_button.disabled = True

        else:
            save_config_button.disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        
        if button_id == "save_config_button":
            self.change_config_values()
            save_config(path="config/config.yaml", config=self.config)
            self.app.pop_screen()

    def change_config_values(self) -> None:
        duration_input = self.query_one("#duration_input", Input)
        self.config['timer']['duration_seconds'] = int(duration_input.value)
