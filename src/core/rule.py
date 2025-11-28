"""Defines the data structure of Rule dataclass"""
from dataclasses import dataclass
import re

@dataclass
class Rule:
    """The Rule main dataclass"""
    name: str
    expression: str
    enabled: bool = True

    def matches(self, text: str) -> bool:
        """Checks if the text provided matches with te regular expression of the Rule"""
        return self.enabled and re.search(self.expression, text) is not None

def validate_rule(rule: Rule):
    """Validates the rule attributes
    
    Args:
        rule: Rule object
    """
    if not rule.name.strip():
        raise ValueError("Rule name cannot be empty")

    if not rule.expression.strip():
        raise ValueError("Rule expression cannot be empty")
