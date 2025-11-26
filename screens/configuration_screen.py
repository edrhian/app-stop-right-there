import sys
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.widgets import Header, Footer, Label, Input, Button, OptionList
from textual.widgets.option_list import Option
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
        """Sets the inputs values to the current configuration"""
        popup_index = ['console','html']
        self.config = load_config(path="config/config.yaml")
        self.duration = self.config['timer']['duration_seconds']
        self.popup_mode = self.config['popup']['mode']

        duration_input = self.query_one("#duration_input", Input)
        duration_input.value = str(self.duration)

        popup_mode_option_list = self.query_one("#popup_mode_option_list", OptionList)
        popup_mode_option_list.highlighted = popup_index.index(self.popup_mode)

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
            yield Label("Popup Window",classes="title")
            yield Label("Mode",classes="body_text")
            yield Label("(the way that the app warns you when breaking a rule)",
                        classes="subtitle")
            yield OptionList(
                Option("Terminal", id="console_option"),
                Option("HTML Page", id="html_option"),
                classes="configuration_option_list",
                id="popup_mode_option_list"
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
            
            self.restart_in_new_terminal()

    def change_config_values(self) -> None:
        duration_input = self.query_one("#duration_input", Input)
        self.config['timer']['duration_seconds'] = int(duration_input.value)

        popup_mode_option_list = self.query_one("#popup_mode_option_list", OptionList)
        selected_popup_mode_option = popup_mode_option_list.highlighted_option

        if selected_popup_mode_option is not None:
            if selected_popup_mode_option.id == "console_option":
                self.config['popup']['mode'] = "console"
            else:
                self.config['popup']['mode'] = "html"

    def restart_in_new_terminal(self):
        sys.exit(99)
