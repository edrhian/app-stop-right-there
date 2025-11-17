from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable
from textual import on, work
from core.window_manager import read_screen_title
import core.rule as rule
import logging

from screens.rule_screen import RuleScreen
from screens.warning_screen import WarningScreen
from screens.confirmation_screen import ConfirmationScreen

class StopRightThereApp(App):

    TITLE = "Stop Right There!"
    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        ("a", "add_rule", "Add New Rule"),
        ("e", "edit_rule", "Edit Rule"),
        ("r", "remove_rule", "Remove Rule")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.rules = rule.load_rules()
        self.refresh_table()
        self.start_window_watch()

    def refresh_table(self):
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.clear(columns=True)

        rules = rule.load_rules()
        table.add_columns("name", "expression")
        table.add_rows([(r["name"], r["expression"]) for r in rules])

    @work
    async def action_add_rule(self) -> None:
        rule_name, rule_expression = await self.push_screen_wait(RuleScreen("add"))
        rule.create_rule(rule_name,rule_expression)
        self.rules = rule.load_rules()
        self.refresh_table()

    @work
    async def action_edit_rule(self) -> None:
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        rule_name, rule_expression = table.get_row(row_key)
        rule_name, rule_expression = await self.push_screen_wait(RuleScreen(rule_name, rule_expression, "edit"))
        rule.edit_rule(rule_name, rule_expression)
        self.rules = rule.load_rules()
        self.refresh_table()
        
    @work
    async def start_window_watch(self):
        await read_screen_title(lambda: self.rules, on_blacklisted=self.handle_blacklisted_window)

    def handle_blacklisted_window(self, window_title: str):
        if isinstance(self.screen, WarningScreen):
            self.pop_screen()
        self.push_screen(WarningScreen())

    @work
    async def action_remove_rule(self) -> None:
        user_confirm = await self.push_screen_wait(ConfirmationScreen())
        if user_confirm:
            table = self.query_one(DataTable)
            row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
            rule.delete_rule(table.get_row(row_key)[0])
            self.rules = rule.load_rules()
            self.refresh_table()

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
    app = StopRightThereApp()
    app.run()
