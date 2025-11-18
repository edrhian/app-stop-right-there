from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label
from textual import on, work
from core.window_manager import watch_screen_title
import core.rule as rule
import logging
import os.path

from screens.rule_screen import RuleScreen
from screens.warning_screen import WarningScreen
from screens.confirmation_screen import ConfirmationScreen
from screens.window_title_display import WindowTitleDisplay

class StopRightThereApp(App):

    TITLE = "Stop Right There!"
    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        ("a", "add_rule", "Add New Rule"),
        ("e", "edit_rule", "Edit Rule"),
        ("r", "remove_rule", "Remove Rule"),
        ("s", "find_window_title", "Window Title Finder"),
        ("d", "switch_enable", "Enable/Disable Rule")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(zebra_stripes=True,cursor_type="row",id="rule_list")
        yield Footer()

    def on_mount(self) -> None:
        self.rules = rule.load_rules()
        self.refresh_table()
        self.start_window_watch()

    def refresh_table(self):
        table = self.query_one(DataTable)
        table.clear(columns=True)

        rules = sorted(rule.load_rules(), key=lambda r: (r["name"], r["expression"]))

        table.add_columns("name", "expression","enabled")
        table.add_rows([(r["name"], r["expression"], r["enabled"]) for r in rules])

    @work
    async def action_add_rule(self) -> None:
        rule_name, rule_expression, rule_enabled = await self.push_screen_wait(RuleScreen("add"))
        rule.create_rule(rule_name,rule_expression, rule_enabled)
        self.rules = rule.load_rules()
        self.refresh_table()

    @work
    async def action_edit_rule(self) -> None:
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        rule_name, rule_expression, rule_enabled = table.get_row(row_key)
        rule_name, rule_expression, rule_enabled = await self.push_screen_wait(RuleScreen(rule_name, rule_expression, rule_enabled,"edit"))
        rule.edit_rule(rule_name, rule_expression, rule_enabled)
        self.rules = rule.load_rules()
        self.refresh_table()
        
    @work
    async def start_window_watch(self):
        await watch_screen_title(lambda: self.rules, on_blacklisted=self.handle_blacklisted_window)

    def handle_blacklisted_window(self, window_title: str):
        if isinstance(self.screen, WarningScreen):
            self.pop_screen()
        self.push_screen(WarningScreen())

    @work
    async def action_remove_rule(self) -> None:
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        rule_name = table.get_row(row_key)[0]
        
        user_confirm = await self.push_screen_wait(ConfirmationScreen(rule_name))
        if user_confirm:
            cursor_row = table.cursor_row    
            rule.delete_rule(rule_name)
            self.rules = rule.load_rules()
            self.refresh_table()
            table.move_cursor(row=cursor_row or 0)

    def action_find_window_title(self) -> None:
        self.push_screen(WindowTitleDisplay())

    def action_switch_enable(self) -> None:
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        rule_name, rule_expression, rule_enabled = table.get_row(row_key)
        rule_enabled = not rule_enabled
        rule.edit_rule(rule_name, rule_expression, rule_enabled)
        cursor_row = table.cursor_row
        self.rules = rule.load_rules()
        self.refresh_table()
        table.move_cursor(row=cursor_row or 0)

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
        with open("data/blacklist.json", "w") as f:
            f.write("[]")

    app = StopRightThereApp()
    app.run()
