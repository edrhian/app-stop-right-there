"""App Main Screen"""
import logging
import os.path
from typing import Tuple
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual import work
from textual.reactive import reactive
from core.window_manager import watch_screen_title
from core.rule_manager import manager
from core.rule import Rule

from navigation.navigation_screen import NavigationScreen
from navigation.screen_list import SCREEN_LIST
from screens.rule_screen import RuleScreen
from screens.warning_screen import WarningScreen
from screens.confirmation_screen import ConfirmationScreen
from screens.window_title_display import WindowTitleDisplay

# Set screen classes, prevents circular import
for screen in SCREEN_LIST:
    if screen["id"] == "window_title_display":
        screen["screen_class"] = WindowTitleDisplay

class StopRightThereApp(App):
    """Entrypoint of the app, displays a table with the rules"""

    TITLE = "Stop Right There!"
    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        ("t", "show_screen_nav", "Navigation Menu"),
        ("a", "add_rule", "Add New Rule"),
        ("e", "edit_rule", "Edit Rule"),
        ("r", "remove_rule", "Remove Rule"),
        ("d", "switch_enable", "Enable/Disable Rule"),
    ]

    show_screen_nav = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(zebra_stripes=True,cursor_type="row",id="rule_list")
        yield Footer()

    def on_mount(self) -> None:
        """Display data after mounting components and start window watcher"""
        self.refresh_table()
        self.start_window_watch()

    def action_show_screen_nav(self) -> None:
        """Toggle the sidebar visibility."""
        self.push_screen(NavigationScreen(disabled_screen_id="home_screen", screen_list=SCREEN_LIST))

    def refresh_table(self, cursor_row=0):
        """Clears table data and displays it again
        Args:
            cursor_row: Row index of the current cursor position
            """
        table = self.query_one(DataTable)
        table.clear(columns=True)

        rules = sorted(manager.get_rules(), key=lambda rule: (rule.name, rule.expression))

        table.add_columns("name", "expression", "enabled")
        table.add_rows([(rule.name, rule.expression, rule.enabled) for rule in rules])

        table.move_cursor(row=cursor_row)

    def get_table_row_values(self) -> Tuple:
        """Returns the values of the table row at the cursor position"""
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        name, expression, enabled = table.get_row(row_key)
        cursor_row = table.cursor_row
        return name, expression, enabled, cursor_row

    @work
    async def action_add_rule(self) -> None:
        """Pushes Rule Screen in add mode"""
        rule_name, rule_expression, rule_enabled = await self.push_screen_wait(RuleScreen("add"))
        cursor_row = self.get_table_row_values()[-1]
        new_rule = Rule(rule_name, rule_expression, rule_enabled)

        await manager.create_rule(new_rule)
        self.refresh_table(cursor_row)

    @work
    async def action_edit_rule(self) -> None:
        """Pushes Rule Screen in edit mode"""
        old_name, old_expression, old_enabled, _ = self.get_table_row_values()
        cursor_row = self.get_table_row_values()[-1]
        _, new_expression, new_enabled = await self.push_screen_wait(RuleScreen(old_name,
                                                                                old_expression,
                                                                                old_enabled, "edit")
                                                                    )

        await manager.edit_rule(old_name, new_expression, new_enabled)

        self.refresh_table(cursor_row)

    @work
    async def start_window_watch(self):
        """Starts the window watcher, assigns get_rules and blacklisted callback function"""
        await watch_screen_title(manager.get_rules,on_blacklisted=self.handle_blacklisted_window)

    def handle_blacklisted_window(self, broken_rule: str):
        """Pushes Warning Screen, prevents WarningScreen mass stacking"""
        if isinstance(self.screen, WarningScreen):
            self.pop_screen()
        self.push_screen(WarningScreen(broken_rule))

    @work
    async def action_remove_rule(self) -> None:
        """Pushes ConfirmationScreen dialog and deletes rule if confirmed"""
        rule_name = self.get_table_row_values()[0]
        cursor_row = self.get_table_row_values()[-1]
        confirm = await self.push_screen_wait(ConfirmationScreen(rule_name))
        if not confirm:
            return

        await manager.delete_rule(rule_name)
        self.refresh_table(cursor_row)

    @work
    async def action_switch_enable(self) -> None:
        """Switches the enabled attribute of the rule at the current table row of the cursor"""
        rule_name, expression, enabled, _ = self.get_table_row_values()
        cursor_row = self.get_table_row_values()[-1]
        new_enabled = not enabled

        await manager.edit_rule(rule_name, expression, new_enabled)

        self.refresh_table(cursor_row)

if __name__ == "__main__":
    logging.basicConfig(
        filename="logs/app.log",
        encoding="UTF-8",
        filemode="a",
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        level=logging.INFO,
    )

    if not os.path.isfile("data/blacklist.json"):
        with open("data/blacklist.json", "w", encoding="UTF-8") as f:
            f.write("[]")

    app = StopRightThereApp()
    app.run()
