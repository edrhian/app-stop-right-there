from textual.app import ComposeResult
from textual.widgets import Footer, Header, Button, Label, Digits
from textual import on
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center
from textual.reactive import reactive

class ConfirmationScreen(Screen):

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("r", "confirm_deletion", "Confirm Deletion"),
        ("a", "noop", None),
        ("e", "noop", None),
    ]

    # Cancel binding inheritance from app.py
    def action_noop(self) -> None:
        pass

    CSS_PATH = "../styles/confirmation_screen.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="confirm_v_container"):
            yield Label("Delete this rule?",classes="confirmation_title")
            yield Label("> Press 'escape' to cancel",classes="confirmation_text")
            yield Label("> Press 'r' again to confirm",classes="confirmation_text")
        yield Footer()

    def action_cancel(self) -> None:
        self.dismiss(False)

    def action_confirm_deletion(self) -> None:
        self.dismiss(True)
        
