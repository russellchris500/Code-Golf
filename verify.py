#!/usr/bin/env python3
"""
Command-line tool for verifying Code Golf solutions.
Returns exit code 0 on success, 1 on failure.
Outputs JSON with success status and character count.
"""

import sys
import json
import os
import copy
import importlib.util
import traceback
import re
import numpy
import numpy as np
from pathlib import Path

# Add the Examples directory to the path so we can import code_golf_utils
sys.path.insert(0, str(Path(__file__).parent / "Examples" / "code_golf_utils"))

# Define colors locally to avoid matplotlib dependency for CLI tool
colors = [
    (0, 0, 0),
    (30, 147, 255),
    (250, 61, 49),
    (78, 204, 48),
    (255, 221, 0),
    (153, 153, 153),
    (229, 59, 163),
    (255, 133, 28),
    (136, 216, 241),
    (147, 17, 49),
]

task_zero = {
    "train": [{
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 5, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 1, 1, 1, 1, 1, 1, 0, 5, 5],
            [5, 5, 0, 0, 0, 0, 0, 0, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
    }],
    "test": [{
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 5, 5, 5],
            [5, 5, 4, 5, 5, 5, 4, 5, 5, 5],
            [5, 5, 4, 5, 5, 5, 4, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 0, 5],
            [5, 5, 5, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 5, 5, 5],
            [5, 5, 4, 0, 0, 0, 4, 0, 5, 5],
            [5, 5, 4, 0, 5, 5, 4, 0, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 0, 5, 5],
            [5, 5, 5, 0, 0, 0, 0, 0, 5, 5],
        ],
    }],
    "arc-gen": [{
        "input": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 5, 5, 5, 5, 2, 5, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
        "output": [
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 5, 5],
            [5, 5, 2, 0, 0, 0, 0, 2, 0, 5],
            [5, 5, 2, 0, 5, 5, 5, 2, 0, 5],
            [5, 5, 2, 0, 5, 5, 5, 2, 0, 5],
            [5, 5, 2, 0, 5, 5, 5, 2, 0, 5],
            [5, 5, 2, 2, 2, 2, 2, 2, 0, 5],
            [5, 5, 5, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ],
    }],
}


def load_examples(task_num):
    """Loads relevant data from ARC-AGI and ARC-GEN."""
    if not task_num:
        return task_zero

    # Try multiple possible locations for the task files
    possible_paths = [
        f"C:/Users/Chris/Code/Code Golf/Examples/task{task_num:03d}.json",
        f"Examples/task{task_num:03d}.json",
        f"./task{task_num:03d}.json",
        f"/kaggle/input/google-code-golf-2025/task{task_num:03d}.json"
    ]

    for path in possible_paths:
        if os.path.exists(path):
            with open(path) as f:
                examples = json.load(f)
            return examples

    raise FileNotFoundError(f"Could not find task{task_num:03d}.json in any expected location")


def verify_solution(task_num, task_path=None):
    """
    Verify a solution for a given task number.
    Returns a dict with success status, character count, and details.
    """
    result = {
        "success": False,
        "character_count": 0,
        "arc_agi_pass": 0,
        "arc_agi_fail": 0,
        "arc_gen_pass": 0,
        "arc_gen_fail": 0,
        "error": None,
        "task_number": task_num
    }

    # Default to task.py if no path specified
    if task_path is None:
        # Try multiple possible locations
        possible_paths = [
            "/kaggle/working/task.py",
            "task.py",
            f"./task{task_num:03d}.py",
            f"task{task_num:03d}.py"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                task_path = path
                break
        else:
            result["error"] = "Could not find task.py or task solution file"
            return result

    if not os.path.exists(task_path):
        result["error"] = f"File not found: {task_path}"
        return result

    # Load examples
    try:
        examples = load_examples(task_num)
    except FileNotFoundError as e:
        result["error"] = str(e)
        return result

    # Import the module
    task_name = "task_with_imports"
    spec = importlib.util.spec_from_file_location(task_name, task_path)
    if spec is None:
        result["error"] = f"Unable to import {task_path}"
        return result

    module = sys.modules[task_name] = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        result["error"] = f"Error importing module: {str(e)}"
        return result

    if not hasattr(module, "p"):
        result["error"] = "Unable to locate function p() in solution file"
        return result

    program = getattr(module, "p")
    if not callable(program):
        result["error"] = "Function p() in solution file is not callable"
        return result

    def verify(example_subset):
        right, wrong, error = 0, 0, ""
        for example in example_subset:
            example_copy = copy.deepcopy(example)
            try:
                output = program(example_copy["input"])
                output = json.dumps(output)
                output = output.replace("true", "1").replace("false", "0")
                unsafe_chars = re.compile(r"[^0-9,\[\]\s\.]")
                if unsafe_chars.search(output):
                    raise ValueError(f"Invalid output from user code: {output[:500]}")
                output = json.loads(output)
                user_output = np.array(output)
                label_output = np.array(example_copy["output"])
                if numpy.array_equal(user_output, label_output):
                    right += 1
                else:
                    wrong += 1
            except Exception as e:
                error = str(e)
                wrong += 1
        return right, wrong, error

    # Verify ARC-AGI examples
    arc_agi_right, arc_agi_wrong, arc_agi_error = verify(examples["train"] + examples["test"])
    result["arc_agi_pass"] = arc_agi_right
    result["arc_agi_fail"] = arc_agi_wrong

    # Verify ARC-GEN examples
    arc_gen_right, arc_gen_wrong, arc_gen_error = verify(examples["arc-gen"])
    result["arc_gen_pass"] = arc_gen_right
    result["arc_gen_fail"] = arc_gen_wrong

    # Combine errors if any
    if arc_agi_error or arc_gen_error:
        result["error"] = arc_agi_error or arc_gen_error

    # Check success
    if arc_agi_wrong + arc_gen_wrong == 0:
        result["success"] = True
        result["character_count"] = os.path.getsize(task_path)

    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python verify.py <task_number> [solution_file]"
        }))
        sys.exit(1)

    try:
        task_num = int(sys.argv[1])
    except ValueError:
        print(json.dumps({
            "success": False,
            "error": f"Invalid task number: {sys.argv[1]}"
        }))
        sys.exit(1)

    task_path = sys.argv[2] if len(sys.argv) > 2 else None

    result = verify_solution(task_num, task_path)

    # Output JSON result
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()