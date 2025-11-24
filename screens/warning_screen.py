"""Warning Popup Screen"""
from textual.app import ComposeResult
from textual.widgets import Footer, Button, Label, Digits
from textual import on
from textual.screen import ModalScreen
from textual.containers import Vertical
from textual.reactive import reactive
from textual.timer import Timer

class WarningScreen(ModalScreen):
    """Screen that appears when accessing a blacklisted window"""
    dismiss_button: Button
    tick_timer: Timer

    def __init__(self, broken_rule=""):
        super().__init__()
        self.broken_rule = broken_rule


    CSS_PATH = "../styles/warning_screen.tcss"
    time_left = reactive(5)

    def on_mount(self) -> None:
        """On mount WarningScreen"""
        self.dismiss_button = self.query_one(Button)
        self.dismiss_button.add_class("hidden")
        self.set_focus(self.dismiss_button)
        self.tick_timer = self.set_interval(1, self.tick)

    def tick(self) -> None:
        """Timer callback function, decrements time, 
        stops timer at zero and shows the button when time runs out"""
        self.time_left -= 1
        if not self.time_left:
            self.tick_timer.stop()
            self.show_button()

    def watch_time_left(self, time_left: int) -> None:
        """Gets the time left and displays it in the Digits component"""
        time, seconds = divmod(time_left, 60)
        hours, minutes = divmod(time, 60)
        self.query_one(Digits).update(f"{hours:02}:{minutes:02}:{seconds:02}")

    def show_button(self) -> None:
        """Changes button class to show it"""
        self.dismiss_button.remove_class("hidden")

    def compose(self) -> ComposeResult:
        with Vertical(id="warning_container", classes="dialog_box"):
            yield Label("Stop Right There!",classes="warning_text")
            yield Label(f"You just broke the {self.broken_rule} rule!",classes="warning_text")
            yield Label("Wait",classes="warning_text")
            yield Digits()
            yield Label("Before continue",classes="warning_text")
            yield Button("Dismiss", id="dismiss_button", variant="error" )
        yield Footer()

    @on(Button.Pressed)
    def action_dismiss_message(self):
        """Returns to the last screen"""
        self.dismiss()
