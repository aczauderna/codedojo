"""Type definitions for CodeDojo."""

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class TestCase:
    """Represents a test case for a problem."""
    input: dict
    output: Any


@dataclass
class ProblemSpec:
    """Represents a problem specification."""
    id: str
    title: str
    difficulty: str
    description: str
    function_name: str
    constraints: List[str]
    test_cases: List[TestCase]
    parameters: Optional[List[str]] = None  # Parameter names for function signature


@dataclass
class Problem:
    """Represents a coding problem."""
    name: str
    description: str
    test_cases: List[TestCase]


@dataclass
class Solution:
    """Represents a solution to a problem."""
    problem_name: str
    code: str
    results: Optional[dict] = None
