"""Configuration Screen"""
import sys
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import VerticalScroll, HorizontalGroup
from textual.widgets import Header, Footer, Label, Input, Button, RadioSet, RadioButton, Rule
from textual.validation import Number

from config.config import load_config, save_config
from core.paths import resource_path
from navigation.navigation_screen import NavigationScreen
from navigation.screen_list import SCREEN_LIST

class ConfigurationScreen(ModalScreen):
    """
    Screen that allows the user to modify the configuration of the App
    """

    AUTO_FOCUS = "Label"

    BINDINGS = [
        ("t", "show_screen_nav", "Navigation Menu")
    ]

    def on_mount(self):
        """Sets the inputs values to the current configuration"""
        self.config = load_config(path=resource_path("config/config.yaml"))
        self.duration = self.config['timer']['duration_seconds']
        self.popup_mode = self.config['popup']['mode']

        duration_input = self.query_one("#duration_input", Input)
        duration_input.value = str(self.duration)

        popup_mode_radio_set = self.query_one("#popup_mode_radio_set", RadioSet)
        radio_button = popup_mode_radio_set.query_one(f"#{self.popup_mode}", RadioButton)
        radio_button.value = True

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll():
            yield Label("Timer Settings", classes="title")
            yield Label("Duration",classes="body_text")
            yield Label("(how much time you have to wait before the dismiss button appears when breaking a rule)",
                        classes="subtitle")
            yield Input(
                    placeholder="Duration",
                    id="duration_input",
                    value="",
                    type="integer",
                    validators=[
                        Number(minimum=1)
                    ]
                )
            yield Rule(line_style="double")
            yield Label("Popup Window",classes="disabled_feature")
            yield Label("Mode",classes="disabled_feature")
            yield Label("(the way that the app warns you when breaking a rule)",
                        classes="disabled_feature")
            yield Label("The html mode is currently disabled due having window managing problems",
                        classes="important_text")
            with RadioSet(id="popup_mode_radio_set",classes="configuration_radio_set"):
                yield RadioButton("Terminal", id="console")
                yield RadioButton("HTML Page", id="html",disabled=True)
            yield Rule(line_style="double")
            yield Label("The app will exit after applying the changes, you must rerun the app manually",
                        classes="important_text")
            with HorizontalGroup():
                yield Button(variant="error", label="Cancel Changes",id="cancel_config_button")
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
        # Save teh configuration and restart the app
        if button_id == "save_config_button":
            self.change_config_values()
            save_config(path=resource_path("config/config.yaml"), configuration=self.config)
            self.restart_in_new_terminal()
        if button_id == "cancel_config_button":
            self.app.pop_screen()

    def change_config_values(self) -> None:
        """Get all input values and modify the configuration"""
        duration_input = self.query_one("#duration_input", Input)
        self.config['timer']['duration_seconds'] = int(duration_input.value)

        popup_mode_radio_set = self.query_one("#popup_mode_radio_set", RadioSet)
        selected_popup_mode_option = popup_mode_radio_set.pressed_button

        if selected_popup_mode_option is not None:
            self.config['popup']['mode'] = selected_popup_mode_option.id

    # NOTE: Restart behavior doesn't work for now, user must open the app manually after it saves the configuration
    def restart_in_new_terminal(self):
        """Exit the program with code 99"""
        sys.exit(99)
