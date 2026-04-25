#!/usr/bin/env python3
"""Main entry point for CodeDojo."""

import sys
from pathlib import Path

from dojo import run_problem, load_problem, run_solution


def create_solution_stub(problem_id: str, solutions_dir: str = "solutions") -> None:
    """Create a stub solution file for the given problem ID."""
    problem = load_problem(problem_id)
    solution_path = Path(solutions_dir) / f"{problem_id}.py"

    if solution_path.exists():
        print(f"Solution file already exists: {solution_path}")
        return

    solution_path.parent.mkdir(parents=True, exist_ok=True)

    if problem.parameters:
        signature = ", ".join(problem.parameters)
    else:
        signature = "input_data"

    stub = f"def {problem.function_name}({signature}):\n"
    stub += f"    \"\"\"TODO: Implement solution for {problem.title}.\"\"\"\n"
    stub += f"    raise NotImplementedError(\"Implement the solution for {problem_id}\")\n"

    solution_path.write_text(stub, encoding="utf-8")
    print(f"Created stub solution: {solution_path}")


def main():
    """Run a problem's solution."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run.py <problem_id>")
        print("  python run.py make_stub <problem_id>")
        print("  python run.py <problem_id> <solution_file>")
        print()
        print("Examples:")
        print("  python run.py example")
        print("  python run.py make_stub example")
        print("  python run.py sum_of_two_numbers solutions/custom.py")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "make_stub":
        if len(sys.argv) != 3:
            print("Usage: python run.py make_stub <problem_id>")
            sys.exit(1)

        problem_id = sys.argv[2]
        try:
            create_solution_stub(problem_id)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)
        except (KeyError, ValueError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        return

    problem_id = command
    
    # If only problem_id is provided, use the new run_problem function
    if len(sys.argv) == 2:
        run_problem(problem_id)
        return
    
    # Legacy mode: problem_id + explicit solution_file
    solution_file = sys.argv[2]
    
    # Load the problem
    try:
        problem = load_problem(problem_id)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error loading problem: {e}")
        sys.exit(1)
    
    # Load the solution code
    try:
        with open(solution_file, 'r') as f:
            solution_code = f.read()
    except FileNotFoundError:
        print(f"Error: Solution file not found: {solution_file}")
        sys.exit(1)
    
    # Run the solution
    try:
        results = run_solution(solution_code, problem)
    except Exception as e:
        print(f"Error running solution: {e}")
        sys.exit(1)
    
    # Print results
    print(f"\nProblem: {problem.title}")
    print(f"ID: {problem.id}")
    print(f"Difficulty: {problem.difficulty}")
    print("Description:")
    for line in problem.description:
        print(line)
    print()
    print(f"Results: {results['passed']} passed, {results['failed']} failed\n")
    
    for result in results["test_results"]:
        status = "✓" if result["passed"] else "✗"
        print(f"{status} Test {result['test_number']}")
        if not result["passed"]:
            print(f"  Input: {result['input']}")
            print(f"  Expected: {result['expected']}")
            print(f"  Got: {result['actual']}")
            if "error" in result:
                print(f"  Error: {result['error']}")
    
    print()


if __name__ == "__main__":
    main()
