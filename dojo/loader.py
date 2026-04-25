"""Loader for CodeDojo problems."""

import json
from pathlib import Path
from typing import Dict

from .types import Example, ProblemSpec, TestCase


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
    
    description_data = data["description"]
    if isinstance(description_data, str):
        description_lines = [description_data]
    elif isinstance(description_data, list) and all(isinstance(item, str) for item in description_data):
        description_lines = description_data
    else:
        raise ValueError("description must be either a string or a list of strings")

    def _validate_string_list(value, field_name):
        if value is None:
            return None
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field_name} must be a list of strings")
        return value

    def _parse_examples(examples_data):
        if examples_data is None:
            return None
        if not isinstance(examples_data, list):
            raise ValueError("examples must be a list")

        examples = []
        for i, item in enumerate(examples_data):
            if not isinstance(item, dict):
                raise ValueError(f"Example {i} must be a dictionary")
            if "input" not in item:
                raise ValueError(f"Example {i} is missing 'input' field")
            if "explanation" not in item:
                raise ValueError(f"Example {i} is missing 'explanation' field")
            if not isinstance(item["input"], dict):
                raise ValueError(f"Example {i}: 'input' must be a dictionary")
            if not isinstance(item["explanation"], str):
                raise ValueError(f"Example {i}: 'explanation' must be a string")

            examples.append(Example(input=item["input"], explanation=item["explanation"]))

        return examples

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
    
    examples = _parse_examples(data.get("examples"))
    edge_cases = _validate_string_list(data.get("edge_cases"), "edge_cases")
    notes = _validate_string_list(data.get("notes"), "notes")
    tags = _validate_string_list(data.get("tags"), "tags")
    patterns = _validate_string_list(data.get("patterns"), "patterns")

    return ProblemSpec(
        id=data["id"],
        title=data["title"],
        difficulty=data["difficulty"],
        description=description_lines,
        function_name=data["function_name"],
        constraints=data["constraints"],
        test_cases=test_cases,
        parameters=data.get("parameters"),  # Optional parameter names
        tags=tags,
        patterns=patterns,
        examples=examples,
        edge_cases=edge_cases,
        notes=notes
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
