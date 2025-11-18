from typing import TypedDict
import json
from typing import List
import re

BLACKLIST_PATH = "data/blacklist.json"

"""Rule structure
- name: Name of the rule
- expression: Regular expression to match the window title
- enabled: If the rule is applied
"""

class Rule(TypedDict):
    name: str
    expression: str
    enabled: bool

def load_rules() -> List[Rule]:
    """Load all rules inside the blacklist file
    
    Returns
    -------
    List[Rule]
        List of rules
    """
    with open(f"{BLACKLIST_PATH}", "r") as f:
        return json.load(f)

def save_rules(rules: List[Rule]) -> None:
    """Save all rules inside the blacklist file

    Parameters
    ----------
    rules : List[Rule]
        List of rules to save
    """

    with open(f"{BLACKLIST_PATH}", "w") as f:
        json.dump(rules, f, indent=2)

def create_rule(name: str, expression: str, enabled: bool) -> None:
    """Creates the new rule if it doesn't exists

    Parameters
    ----------
    name : str
        Name of the rule
    expression : str
        Regular expression to match the window title
    """
    rules = load_rules()

    if any(rule["name"] == name for rule in rules):
        raise ValueError(f"Rule '{name}' already exists.")

    rules.append({"name": name, "expression": expression, "enabled": enabled})

    save_rules(rules)

def edit_rule(name: str, expression: str, enabled: bool) -> bool:
    """Edits an existing rule
    
    Parameters
    ----------
    name : str
        Name of the rule
    expression : str
        New regular expression to match the window title

    Returns
    -------
    bool
        True if the rule was edited, False if the rule was not found
    """
    rules = load_rules()
    for rule in rules:
        if rule["name"] == name:
            rule["expression"] = expression
            rule["enabled"] = enabled
            save_rules(rules)
            return True
    return False

def check_rules(window_title: str, rules: List[Rule]) -> bool:
    """Checks if the window title matches any enabled rule
    
    Parameters
    ----------
    window_title : str
        Title of the window
    rules : List[Rule]
        List of rules to check against
    
    Returns
    -------
    bool
        True if the window title matches any rule, False otherwise
    """
    for rule in rules:
        if re.search(rule["expression"], window_title) and rule["enabled"]:
            return True
    return False

def delete_rule(rule_name) -> bool:
    """Deletes a rule
    
    Parameters
    ----------
    rule_name : str
        Name of the rule to delete
    Returns
    -------
    bool
        True if the rule was deleted, False if the rule was not found
    """

    rules = load_rules()
    for rule in rules:
        if rule["name"] == rule_name:
            rules.remove(rule)
            save_rules(rules)
            return True
    return False

