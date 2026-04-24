"""CodeDojo - A local coding dojo for practicing Python."""

__version__ = "0.1.0"

from .loader import load_problem
from .runner import load_solution, run_solution, run_problem
from .types import TestCase, ProblemSpec, Problem, Solution

__all__ = ["load_problem", "load_solution", "run_solution", "run_problem", "TestCase", "ProblemSpec", "Problem", "Solution"]
