# CodeDojo

A local coding dojo for practicing Python programming through problem-solving.

## Project Structure

```
CodeDojo/
├── dojo/                 # Core dojo module
│   ├── __init__.py
│   ├── loader.py        # Problem loader
│   ├── runner.py        # Solution runner
│   └── types.py         # Type definitions
├── problems/            # Problem definitions (JSON format)
│   └── example.json     # Example problem
├── solutions/           # Solution implementations
│   └── example.py       # Example solution
├── run.py              # Main entry point
└── README.md           # This file
```

## Getting Started

### Quick Start - Running a Problem

The simplest way to run a problem and its solution:

```bash
python3 run.py example
python3 run.py sum_of_two_numbers
```

This automatically loads the problem from `problems/<problem_id>.json`, imports the solution from `solutions/<problem_id>.py`, runs all test cases, and displays formatted results with timing information.

### Legacy Mode - Custom Solution File

If you want to run a custom solution file against a problem:

```bash
python3 run.py sum_of_two_numbers solutions/custom_solution.py
```

### Output Format

When running `python3 run.py <problem_id>`, you'll see:
- Problem title, ID, difficulty, and description
- ✓ OK or ✗ FAIL status for each test with execution time in milliseconds
- On failure: Input, expected output, and actual output
- On error: Input, expected output, and error message
- Summary with total passed/failed and total execution time

## Problem Format

Problems are defined in JSON format with structured metadata. Each problem file should have the following structure:

```json
{
  "id": "problem_identifier",
  "title": "Problem Title",
  "difficulty": "easy|medium|hard",
  "description": "Detailed description of what the problem asks.",
  "function_name": "solve",
  "constraints": [
    "Constraint 1",
    "Constraint 2"
  ],
  "test_cases": [
    {
      "input": {"key": "value"},
      "output": "expected_result"
    }
  ]
}
```

### Field Descriptions

- **id**: Unique identifier for the problem (used as filename)
- **title**: Human-readable problem name
- **difficulty**: Level of difficulty (easy, medium, hard)
- **description**: Full problem description
- **function_name**: Name of the function to implement (e.g., "solve")
- **constraints**: List of constraints or requirements
- **test_cases**: Array of test cases with input (dict) and expected output

### Example Problem

```json
{
  "id": "sum_of_two_numbers",
  "title": "Sum of Two Numbers",
  "difficulty": "easy",
  "description": "Write a function that returns the sum of two numbers.",
  "function_name": "solve",
  "constraints": [
    "The input will always be a dictionary",
    "Numbers can be positive, negative, or zero"
  ],
  "test_cases": [
    {
      "input": {"a": 1, "b": 2},
      "output": 3
    },
    {
      "input": {"a": 5, "b": 10},
      "output": 15
    }
  ]
}
```

## Solution Format

Solutions must define a function that matches the `function_name` specified in the problem (typically `solve`). The function receives the `input` dictionary and must return a value matching the expected `output`.

### Example Solution

```python
def solve(input_data):
    """Calculate the sum of two numbers."""
    return input_data["a"] + input_data["b"]
```

## Features

- **Load and run problems** from JSON files with full metadata
- **Dynamic solution import** - automatically finds and loads solution files
- **Execute solutions** and validate against all test cases  
- **Detailed test result reporting** with pass/fail status and execution timing
- **Clear error messages** for missing fields, malformed data, or runtime errors
- **Formatted output** with visual indicators (✓ OK, ✗ FAIL, ✗ ERROR)
- **Execution timing** for each test case in milliseconds
- **Expected vs actual output display** on test failures
- **Error stack traces** and messages when exceptions occur
- **Type hints** and dataclass-based clean architecture
- **Extensible structure** for adding new problems and solutions

## Error Handling

The loader provides clear error messages for common issues:

- **FileNotFoundError**: Problem file doesn't exist
- **KeyError**: Required fields missing from problem specification
- **ValueError**: JSON is invalid or test cases are malformed

