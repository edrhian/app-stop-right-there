from textual.app import ComposeResult
from textual.widgets import Footer, Header, Button, Input, Label
from textual.reactive import reactive
from textual import on
from textual.screen import ModalScreen    
from textual.containers import Vertical

class RuleScreen(ModalScreen[list]):

    CSS_PATH = "../styles/rule_screen.tcss"

    def __init__(self, rule_name = "",rule_expression = "", mode = "add"):
        super().__init__()
        self.mode = mode
        self.rule_name = rule_name
        self.rule_expression = rule_expression

    BINDINGS = [
        ("escape","app.pop_screen","Cancel"),
    ]

    rule_name = reactive("")
    rule_expression = reactive("")

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="form_container"):
            yield Label(content="Add New Rule" if self.mode=="add" else "Modify Rule", id="title")
            yield Input(
                placeholder="Rule Name", 
                id="input_rule_name", 
                disabled=(self.mode=="edit"), 
                value="" if self.mode=="add" else self.rule_name,
                classes="rule_screen_title"
            )
            yield Input(
                placeholder="Rule Expression", 
                id="input_rule_expression", 
                value="" if self.mode=="add" else self.rule_expression,
                classes="rule_screen_title"
            )
            yield Button(variant="success", label="Submit")
            
        yield Footer()

    @on(Button.Pressed)
    def action_confirm_add_rule(self):
        self.dismiss([self.rule_name, self.rule_expression])

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        input_widget = event.input

        if input_widget.id == "input_rule_name":
            self.rule_name = input_widget.value

        elif input_widget.id == "input_rule_expression":
            self.rule_expression = input_widget.value
