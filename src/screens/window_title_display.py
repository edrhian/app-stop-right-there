"""Window Scanner Screen"""
import asyncio
from textual.app import ComposeResult
from textual.widgets import Footer, Header, Label
from textual import work
from textual.screen import ModalScreen
from textual.containers import Vertical, ScrollableContainer
from textual.reactive import reactive

from core.paths import resource_path
from core.window_manager import get_window_title
from navigation.navigation_screen import NavigationScreen
from navigation.screen_list import SCREEN_LIST

DESCRIPTION = """This screen lets you know what is the exact title that the app reads"""

class WindowTitleDisplay(ModalScreen):
    """Screen that let's the user display the exact title of the active window"""

    def __init__(self) -> None:
        super().__init__()
        self.scan_list: ScrollableContainer

    BINDINGS = [
        ("t", "show_screen_nav", "Navigation Menu"),
        ("s", "scan_switch", "Start/Stop Scanning"),
        ("c", "clear_list", "Clear Scan List"),
    ]

    CSS_PATH = resource_path("styles/window_title_display.tcss")

    is_scanning = reactive(False)
    scan_state_label: Label | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="window_title_display_container"):
            yield Label(DESCRIPTION, classes="title")
            yield Label("> Press 's' to start/stop scanning every 1 second", classes="subtitle")
            self.scan_state_label = Label(f"Scanning: {self.is_scanning}",
                                          id="scan_state",
                                          classes="subtitle")
            yield self.scan_state_label

            self.scan_list = ScrollableContainer(id="scan_list")
            yield self.scan_list

        yield Footer()

    def action_show_screen_nav(self) -> None:
        """Toggle the sidebar visibility."""
        self.app.push_screen(NavigationScreen(disabled_screen_id="window_title_display", screen_list=SCREEN_LIST))

    def action_cancel(self) -> None:
        """Returns to the last Screen without sending data"""
        self.dismiss()

    def watch_is_scanning(self) -> None:
        """Watches is_scanning reactive variable"""
        if self.scan_state_label:
            self.scan_state_label.update(f"Scanning: {self.is_scanning}")

    @work
    async def action_scan_switch(self):
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

    def action_clear_list(self):
        """Clears the scan_list labels"""
        self.scan_list.remove_children()
