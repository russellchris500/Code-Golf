# -*- coding: utf-8 -*-
"""
Debug tool to view failing test cases for Code Golf tasks.
Usage: python debug_failures.py <task_number> [folder]
"""
import json
import os
import sys
import importlib.util
import copy

sys.path.append(os.path.join(os.path.dirname(__file__), 'Examples', 'code_golf_utils'))
from code_golf_utils import colors

def load_solution(task_num, folder="Work"):
    """Load the solution function from the specified folder"""
    solution_path = os.path.join(os.path.dirname(__file__), folder, f'task{task_num:03d}.py')

    if not os.path.exists(solution_path):
        print(f"Error: Solution file task{task_num:03d}.py not found in {folder} folder")
        return None

    try:
        spec = importlib.util.spec_from_file_location(f"task{task_num:03d}", solution_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'p'):
            return module.p
        else:
            print(f"Error: Solution file task{task_num:03d}.py does not contain function 'p'")
            return None

    except Exception as e:
        print(f"Error loading solution: {str(e)}")
        return None

def test_solution(solution_func, input_grid, expected_output):
    """Test the solution function and return the result"""
    if not solution_func:
        return None, "No solution loaded"

    try:
        # Create a deep copy of input to avoid modifying original
        input_copy = copy.deepcopy(input_grid)
        result = solution_func(input_copy)

        # Convert result to list format if it's not already
        if isinstance(result, tuple):
            result = [list(row) if isinstance(row, tuple) else row for row in result]
        elif isinstance(result, list):
            # Also convert any tuple rows within a list result
            result = [list(row) if isinstance(row, tuple) else row for row in result]
        else:
            return None, f"Invalid output type: {type(result)}"

        # Check if result matches expected output
        if result == expected_output:
            return result, "PASS"
        else:
            return result, "FAIL"

    except Exception as e:
        return None, f"Error: {str(e)}"

def print_grid(grid, title="Grid"):
    """Print a grid in a readable format"""
    print(f"\n{title}:")
    if not grid:
        print("  (empty)")
        return

    print(f"  Size: {len(grid)}x{len(grid[0]) if grid else 0}")
    for i, row in enumerate(grid):
        row_str = ''.join(str(cell) for cell in row)
        print(f"  {i:2d}: {row_str}")

def find_failures(task_num, folder="Work", max_failures=5, show_details=True):
    """Find and display failing test cases"""
    print(f"=== Debug Failures for Task {task_num} ===")

    # Load solution
    solution_func = load_solution(task_num, folder)
    if not solution_func:
        return

    # Load task data
    file_path = os.path.join(os.path.dirname(__file__), 'Examples', f"task{task_num:03d}.json")
    if not os.path.exists(file_path):
        print(f"Error: File task{task_num:03d}.json not found")
        return

    with open(file_path, 'r') as f:
        example_data = json.load(f)

    failures = []
    total_tests = 0

    # Test all categories
    for category in ['train', 'test', 'arc-gen']:
        if category not in example_data:
            continue

        print(f"\n--- Testing {category} examples ---")
        category_failures = []

        for i, example in enumerate(example_data[category]):
            total_tests += 1
            result, status = test_solution(solution_func, example['input'], example['output'])

            if status != "PASS":
                category_failures.append({
                    'category': category,
                    'index': i,
                    'input': example['input'],
                    'expected': example['output'],
                    'actual': result,
                    'status': status
                })
                print(f"  {category} {i+1}: {status}")
            else:
                print(f"  {category} {i+1}: PASS")

        failures.extend(category_failures)

    # Summary
    print(f"\n=== SUMMARY ===")
    print(f"Total tests: {total_tests}")
    print(f"Failures: {len(failures)}")
    print(f"Success rate: {((total_tests - len(failures)) / total_tests * 100):.1f}%")

    if not failures:
        print("🎉 All tests passed!")
        return

    # Show detailed failure information
    if show_details:
        print(f"\n=== DETAILED FAILURE ANALYSIS ===")
        for i, failure in enumerate(failures[:max_failures]):
            print(f"\n--- FAILURE {i+1}: {failure['category']} example {failure['index']+1} ---")
            print(f"Status: {failure['status']}")

            print_grid(failure['input'], "Input")
            print_grid(failure['expected'], "Expected Output")

            if failure['actual'] is not None:
                print_grid(failure['actual'], "Actual Output")

                # Compare sizes
                exp_size = (len(failure['expected']), len(failure['expected'][0]) if failure['expected'] else 0)
                act_size = (len(failure['actual']), len(failure['actual'][0]) if failure['actual'] else 0)
                if exp_size != act_size:
                    print(f"  ⚠️  Size mismatch: expected {exp_size}, got {act_size}")

                # Show differences if same size
                if exp_size == act_size and failure['expected'] and failure['actual']:
                    print("\n  Differences:")
                    found_diff = False
                    for r in range(len(failure['expected'])):
                        for c in range(len(failure['expected'][0])):
                            if failure['expected'][r][c] != failure['actual'][r][c]:
                                print(f"    ({r},{c}): expected {failure['expected'][r][c]}, got {failure['actual'][r][c]}")
                                found_diff = True
                    if not found_diff:
                        print("    (No differences found - this shouldn't happen!)")
            else:
                print("  Actual Output: (error occurred)")

            print("-" * 60)

        if len(failures) > max_failures:
            print(f"\n... and {len(failures) - max_failures} more failures")

    return failures

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_failures.py <task_number> [folder] [max_failures]")
        print("  task_number: 1-400")
        print("  folder: Work (default) or Solutions")
        print("  max_failures: maximum number of detailed failures to show (default: 5)")
        return

    try:
        task_num = int(sys.argv[1])
        if not (1 <= task_num <= 400):
            print("Error: Task number must be between 1 and 400")
            return
    except ValueError:
        print("Error: Task number must be a valid integer")
        return

    folder = sys.argv[2] if len(sys.argv) > 2 else "Work"
    max_failures = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    find_failures(task_num, folder, max_failures)

if __name__ == "__main__":
    main()