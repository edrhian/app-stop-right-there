from textual.app import ComposeResult
from textual.widgets import Footer, Header, Button, Label, Digits
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Vertical, Horizontal, Center
from textual.reactive import reactive

class ConfirmationScreen(ModalScreen):

    def __init__(self, rule_name):
        super().__init__()
        self.rule_name = rule_name

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("r", "confirm_deletion", "Confirm Deletion"),
    ]

    CSS_PATH = "../styles/confirmation_screen.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="dialog_box"):
            yield Label(f"Delete {self.rule_name} rule?",classes="confirmation_title")
            yield Label("> Press 'escape' to cancel",classes="confirmation_text")
            yield Label("> Press 'r' again to confirm",classes="confirmation_text")
        yield Footer()

    def action_cancel(self) -> None:
        self.dismiss(False)

    def action_confirm_deletion(self) -> None:
        self.dismiss(True)
        
