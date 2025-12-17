"""Navigation Screen"""
from typing import Sequence
import webbrowser
from textual.widgets import OptionList, Label
from textual.screen import ModalScreen
from textual.widgets.option_list import Option
from textual.containers import Vertical
from navigation.screen_list import ScreenItem

class NavigationScreen(ModalScreen):
    """Screen that lets the user navigate between screens"""
    DEFAULT_CSS = """
        #navigation_option_list {
            align: center middle;
        }
        Label.header1 {
            margin: 1;
            text-style: bold;
        }
        Vertical.nav_container {
            width: 60%;
            height: 70%;
        }
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
        ("t", "app.pop_screen", "Cancel")
    ]

    def __init__(self, disabled_screen_id: str, screen_list: Sequence[ScreenItem]) -> None:
        super().__init__()
        self.disabled_screen = disabled_screen_id

        self.screen_list = screen_list

        self.options = []

        for screen in self.screen_list:
            self.options.append(Option(prompt=screen['prompt'], id=screen['id']))

        # Prevents stacking the same screen
        for option in self.options:
            if option.id == disabled_screen_id:
                option.disabled = True
                return

    def compose(self):
        with Vertical(classes="nav_container"):
            yield Label("Screen Navigator",classes="header1")
            option_list = OptionList(id="navigation_option_list")
            option_list.add_options(self.options)
            yield option_list

    def on_option_list_option_selected(self, message: OptionList.OptionSelected):
        """Switch to the selected screen"""
        target_screen = message.option.id

        for screen in self.screen_list:
            if target_screen == "documentation":
                webbrowser.open("https://github.com/edrhian/app-stop-right-there/tree/main", 2)
                self.app.pop_screen()
                return
        
            if screen["id"] == target_screen:
                screen_class = screen["screen_class"]

                # Pop all screens before stack another
                while len(self.app.screen_stack) > 1:
                    self.app.pop_screen()

                # Only Home Screen (the app entrypoint) has no class
                if screen_class is None:    
                    return

                self.app.push_screen(screen_class())
                return
            

        self.dismiss()
