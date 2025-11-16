from textual.app import ComposeResult
from textual.widgets import Footer, Header, Button, Label
from textual import on
from textual.screen import Screen

class WarningScreen(Screen):
    
    CSS_PATH = "../styles/warning_screen.tcss"

    def on_mount(self) -> None:
        self.dismiss_button = self.query_one(Button)
        self.dismiss_button.add_class("hidden")
        self.set_focus(self.dismiss_button)
        self.set_timer(3, self.show_button)
        
    def show_button(self) -> None:
        self.dismiss_button.remove_class("hidden")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("This is a warning screen!")
        yield Button("Dismiss", id="dismiss_button", variant="error" )
        yield Footer()

    @on(Button.Pressed)
    def action_dismiss_message(self):
        self.dismiss()
