import asyncio
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Label
from textual import work
from textual.screen import Screen
from textual.containers import Vertical, ScrollableContainer
from textual.reactive import reactive

from core.window_manager import get_window_title

DESCRIPTION = """This screen lets you know what is the exact title that the app reads"""

class WindowTitleDisplay(Screen):

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("s", "start_scan", "Start Scanning"),
        ("a", "noop", None),
        ("e", "noop", None),
        ("r", "noop", None),
    ]

    # Cancel binding inheritance from app.py
    def action_noop(self) -> None:
        pass

    CSS_PATH = "../styles/window_title_display.tcss"

    is_scanning = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="window_title_display_container"):
            yield Label(DESCRIPTION, classes="window_title_display_title")
            yield Label("> Press 's' to start/stop scanning every 1 second", classes="window_title_display_description")

            self.scan_list = ScrollableContainer(id="scan_list")  
            yield self.scan_list

        yield Footer()

    def action_cancel(self) -> None:
        self.dismiss()

    @work
    async def action_start_scan(self):
        """Append a new line to the scan list every second."""
        self.is_scanning = not self.is_scanning

        if not self.is_scanning:
            return

        while self.is_scanning:
            title = await asyncio.to_thread(get_window_title) or ""

            new_label = Label(f"Active Window: {title}", classes="scan_item")
            self.scan_list.mount(new_label)
            new_label.scroll_visible()

            await asyncio.sleep(1)
