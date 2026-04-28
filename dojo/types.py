"""Type definitions for CodeDojo."""

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class TestCase:
    """Represents a test case for a problem."""
    input: dict
    output: Any


@dataclass
class Example:
    """Represents a documented example for a problem."""
    input: dict
    explanation: List[str]


@dataclass
class ProblemSpec:
    """Represents a problem specification."""
    id: str
    title: str
    difficulty: str
    description: List[str]
    function_name: str
    constraints: List[str]
    test_cases: List[TestCase]
    parameters: Optional[List[str]] = None  # Parameter names for function signature
    tags: Optional[List[str]] = None
    patterns: Optional[List[str]] = None
    examples: Optional[List[Example]] = None
    edge_cases: Optional[List[str]] = None
    notes: Optional[List[str]] = None


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
