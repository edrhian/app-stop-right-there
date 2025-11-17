from textual.app import ComposeResult
from textual.widgets import Footer, Header, Button, Label, Digits
from textual import on
from textual.screen import Screen
from textual.containers import Vertical
from textual.reactive import reactive

class WarningScreen(Screen):
    
    CSS_PATH = "../styles/warning_screen.tcss"
    time_left = reactive(5)
    
    BINDINGS = [
        ("a", "noop", None),
        ("e", "noop", None),
        ("r", "noop", None),
    ]

    # Cancel binding inheritance from app.py
    def action_noop(self) -> None:
        pass

    def on_mount(self) -> None:
        self.dismiss_button = self.query_one(Button)
        self.dismiss_button.add_class("hidden")
        self.set_focus(self.dismiss_button)
        self.tick_timer = self.set_interval(1, self.tick)
        
    def tick(self) -> None:
        self.time_left -= 1
        if not self.time_left:
            self.tick_timer.stop()
            self.show_button()

    def watch_time_left(self, time_left: int) -> None:
        time, seconds = divmod(time_left, 60)
        hours, minutes = divmod(time, 60)
        self.query_one(Digits).update(f"{hours:02}:{minutes:02}:{seconds:02}")

    def show_button(self) -> None:
        self.dismiss_button.remove_class("hidden")

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="warning_container"):
            yield Label("Stop Right There!",classes="warning_text")
            yield Label(f"Wait",classes="warning_text")
            yield Digits()
            yield Label(f"Before continue",classes="warning_text")
            yield Button("Dismiss", id="dismiss_button", variant="error" )
        yield Footer()

    @on(Button.Pressed)
    def action_dismiss_message(self):
        self.dismiss()
