import asyncio
import json
from pathlib import Path
from typing import List
from core.rule import Rule, validate_rule

class RuleManager:
    """Manages CRUD operations of Rules"""

    def __init__(self, path: str = "data/blacklist.json"):
        self.path = Path(path)
        self._lock = asyncio.Lock()
        self.rules: List[Rule] = self.load()

    def load(self) -> List[Rule]:
        """Loads all rules from file in path"""
        if not self.path.exists():
            return []

        try:
            with open(self.path, "r") as f:
                data = json.load(f)

            return [Rule(name=rule["name"], expression=rule["expression"], enabled=rule["enabled"]) for rule in data]

        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON inside {self.path}")

    def _save(self) -> None:
        """Saves all rules to a json file from path"""
        data = [{"name": rule.name, "expression": rule.expression, "enabled": rule.enabled} for rule in self.rules]

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    async def create_rule(self, rule: Rule) -> None:
        """Creates a rule if is validated and adds to rules list, calls save"""
        async with self._lock:
            if any(r.name == rule.name for r in self.rules):
                raise ValueError(f"Rule '{rule.name}' already exists.")

            validate_rule(rule)
            self.rules.append(rule)
            self._save()

    async def edit_rule(self, name: str, expr: str, enabled: bool) -> bool:
        """Edits a rule if it's name exists"""
        async with self._lock:
            for rule in self.rules:
                if rule.name == name:
                    rule.expression = expr
                    rule.enabled = enabled
                    validate_rule(rule)
                    self._save()
                    return True
        return False

    async def delete_rule(self, name: str) -> bool:
        """Deletes a rule from rule list and saves the list"""
        async with self._lock:
            for rule in self.rules:
                if rule.name == name:
                    self.rules.remove(rule)
                    self._save()
                    return True
        return False

    def get_rules(self) -> List[Rule]:
        """Gets all rules"""
        return self.rules

manager = RuleManager()
