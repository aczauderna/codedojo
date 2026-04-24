"""Runner for CodeDojo solutions."""

import importlib.util
import time
from pathlib import Path

from .loader import load_problem
from .types import ProblemSpec


def run_solution(solution_code: str, problem: ProblemSpec) -> dict:
    """
    Run a solution against a problem's test cases.
    
    Args:
        solution_code: The solution code as a string.
        problem: The ProblemSpec instance to test against.
        
    Returns:
        A dictionary with results for each test case.
    """
    # Create a namespace to execute the solution code
    namespace = {}
    exec(solution_code, namespace)
    
    # Assume the solution function is named 'solve'
    solve_func = namespace.get('solve')
    
    if not solve_func:
        raise ValueError("Solution must define a 'solve' function")
    
    results = {
        "passed": 0,
        "failed": 0,
        "test_results": []
    }
    
    for i, test_case in enumerate(problem.test_cases):
        try:
            output = solve_func(test_case.input)
            passed = output == test_case.output
            
            results["test_results"].append({
                "test_number": i + 1,
                "passed": passed,
                "input": test_case.input,
                "expected": test_case.output,
                "actual": output
            })
            
            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1
                
        except Exception as e:
            results["test_results"].append({
                "test_number": i + 1,
                "passed": False,
                "input": test_case.input,
                "expected": test_case.output,
                "actual": None,
                "error": str(e)
            })
            results["failed"] += 1
    
    return results


def load_solution(problem_id: str, solutions_dir: str = "solutions"):
    """
    Dynamically load a solution module from a Python file.
    
    Args:
        problem_id: The problem identifier (filename without extension).
        solutions_dir: Directory containing solution Python files.
        
    Returns:
        The imported solution module.
        
    Raises:
        FileNotFoundError: If the solution file does not exist.
        ImportError: If the module cannot be loaded.
    """
    solution_path = Path(solutions_dir) / f"{problem_id}.py"
    
    if not solution_path.exists():
        raise FileNotFoundError(f"Solution file not found: {solution_path}")
    
    spec = importlib.util.spec_from_file_location(f"solution_{problem_id}", solution_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to create import spec for {solution_path}")
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_problem(problem_id: str, problems_dir: str = "problems", solutions_dir: str = "solutions") -> None:
    """
    Load a problem, import its solution, run all test cases, and print results with timing.
    
    Args:
        problem_id: The problem identifier (filename without extension).
        problems_dir: Directory containing problem JSON files. Defaults to "problems".
        solutions_dir: Directory containing solution Python files. Defaults to "solutions".
        
    Raises:
        FileNotFoundError: If problem or solution file not found.
        AttributeError: If solution module doesn't contain the required function.
        Exception: For other runtime errors.
    """
    # Load the problem specification
    try:
        problem = load_problem(problem_id, problems_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except (KeyError, ValueError) as e:
        print(f"Error loading problem: {e}")
        return
    
    # Dynamically import the solution module
    try:
        solution_module = load_solution(problem_id, solutions_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error loading solution module: {e}")
        return
    
    # Get the function from the solution module
    function_name = problem.function_name
    
    if not hasattr(solution_module, function_name):
        print(f"Error: Solution module does not define function '{function_name}'")
        return
    
    solve_func = getattr(solution_module, function_name)
    
    if not callable(solve_func):
        print(f"Error: '{function_name}' is not callable")
        return
    
    # Print problem header
    print(f"\n{'=' * 70}")
    print(f"Problem: {problem.title}")
    print(f"ID: {problem.id}")
    print(f"Difficulty: {problem.difficulty}")
    print(f"Description: {problem.description}")
    print(f"{'=' * 70}\n")
    
    # Run test cases
    passed_count = 0
    failed_count = 0
    total_time = 0.0
    
    for i, test_case in enumerate(problem.test_cases, 1):
        try:
            # Measure execution time
            start_time = time.time()
            
            # Call function with appropriate arguments
            if problem.parameters:
                # Unpack input dict as keyword arguments
                actual_output = solve_func(**test_case.input)
            else:
                # Pass entire input dict as single argument
                actual_output = solve_func(test_case.input)
                
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            
            # Check if output matches expected
            is_passed = actual_output == test_case.output
            
            if is_passed:
                status = "✓ OK"
                passed_count += 1
            else:
                status = "✗ FAIL"
                failed_count += 1
            
            # Print result with timing
            print(f"Test {i}: {status} ({elapsed_time*1000:.2f}ms)")
            
            # On failure, print details
            if not is_passed:
                print(f"  Input:    {test_case.input}")
                print(f"  Expected: {test_case.output}")
                print(f"  Actual:   {actual_output}")
            
        except Exception as e:
            failed_count += 1
            print(f"Test {i}: ✗ ERROR")
            print(f"  Input:    {test_case.input}")
            print(f"  Expected: {test_case.output}")
            print(f"  Error:    {str(e)}")
    
    # Print summary
    print(f"\n{'-' * 70}")
    print(f"Results: {passed_count} passed, {failed_count} failed")
    print(f"Total time: {total_time*1000:.2f}ms")
    print(f"{'=' * 70}\n")
