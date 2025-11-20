from dataclasses import dataclass, field
import re

@dataclass
class Rule:
    """The Rule main dataclass"""
    name: str
    expression: str
    enabled: bool = True

    def matches(self, text: str) -> bool:
        return self.enabled and re.search(self.expression, text) is not None

def validate_rule(rule: Rule):
    """Validates the rule attributes"""
    if not rule.name.strip():
        raise ValueError("Rule name cannot be empty")

    if not rule.expression.strip():
        raise ValueError("Rule expression cannot be empty")
