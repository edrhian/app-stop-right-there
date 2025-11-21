"""Delete Rule confirmation dialog"""
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Label
from textual.screen import ModalScreen
from textual.containers import Vertical

class ConfirmationScreen(ModalScreen):
    """Screen that displays a confirmation dialog"""

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
        """Cancels deletion and returns to the last screens"""
        self.dismiss(False)

    def action_confirm_deletion(self) -> None:
        """Confirms the deletion and returns to the last screens"""
        self.dismiss(True)
