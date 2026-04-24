"""Loader for CodeDojo problems."""

import json
from pathlib import Path
from typing import Dict

from .types import ProblemSpec, TestCase


def load_problem(problem_id: str, problems_dir: str = "problems") -> ProblemSpec:
    """
    Load a problem specification from a JSON file.
    
    Args:
        problem_id: The problem identifier (filename without .json).
        problems_dir: Directory containing problem JSON files. Defaults to "problems".
        
    Returns:
        A ProblemSpec instance.
        
    Raises:
        FileNotFoundError: If the problem file does not exist.
        KeyError: If required fields are missing from the problem specification.
        ValueError: If test cases are malformed.
    """
    problem_path = Path(problems_dir) / f"{problem_id}.json"
    
    if not problem_path.exists():
        raise FileNotFoundError(f"Problem file not found: {problem_path}")
    
    try:
        with open(problem_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in problem file {problem_path}: {e}")
    
    # Validate required fields
    required_fields = ["id", "title", "difficulty", "description", "function_name", "constraints", "test_cases"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise KeyError(f"Missing required fields in {problem_path}: {missing_fields}")
    
    # Parse test cases
    test_cases = []
    test_cases_data = data.get("test_cases", [])
    
    if not isinstance(test_cases_data, list):
        raise ValueError("test_cases must be a list")
    
    for i, tc in enumerate(test_cases_data):
        if not isinstance(tc, dict):
            raise ValueError(f"Test case {i} must be a dictionary")
        
        if "input" not in tc:
            raise ValueError(f"Test case {i} is missing 'input' field")
        
        if "output" not in tc:
            raise ValueError(f"Test case {i} is missing 'output' field")
        
        if not isinstance(tc["input"], dict):
            raise ValueError(f"Test case {i}: 'input' must be a dictionary")
        
        test_cases.append(TestCase(input=tc["input"], output=tc["output"]))
    
    return ProblemSpec(
        id=data["id"],
        title=data["title"],
        difficulty=data["difficulty"],
        description=data["description"],
        function_name=data["function_name"],
        constraints=data["constraints"],
        test_cases=test_cases,
        parameters=data.get("parameters")  # Optional parameter names
    )


def load_all_problems(problems_dir: str = "problems") -> Dict[str, ProblemSpec]:
    """
    Load all problems from a directory.
    
    Args:
        problems_dir: Directory containing problem JSON files.
        
    Returns:
        A dictionary mapping problem IDs to ProblemSpec instances.
    """
    problems = {}
    path = Path(problems_dir)
    
    for problem_file in path.glob("*.json"):
        problem_id = problem_file.stem  # Get filename without extension
        try:
            problem = load_problem(problem_id, problems_dir)
            problems[problem.id] = problem
        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f"Warning: Failed to load problem from {problem_file}: {e}")
    
    return problems
