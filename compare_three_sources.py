# Final comparison between Best, Public-3, and Public-4
import os
import shutil
import json
import copy

def test_solution(solution_function, input_grid, expected_output):
    """Test the solution function and return whether it passes"""
    try:
        # Create a deep copy of input to avoid modifying original
        input_copy = copy.deepcopy(input_grid)
        result = solution_function(input_copy)

        # Convert result to list format if it's not already
        if isinstance(result, tuple):
            result = [list(row) if isinstance(row, tuple) else row for row in result]
        elif isinstance(result, list):
            result = [list(row) if isinstance(row, tuple) else row for row in result]
        else:
            return False

        # Check if result matches expected output
        return result == expected_output
    except Exception:
        return False

def test_all_examples(solution_function, task_num):
    """Test the solution against all examples. Returns True if all pass."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'Examples', f"task{task_num:03d}.json")
        if not os.path.exists(file_path):
            return False

        with open(file_path, 'r') as f:
            example_data = json.load(f)

        # Test all categories
        for category in ['train', 'test', 'arc-gen']:
            if category in example_data:
                for example in example_data[category]:
                    if not test_solution(solution_function, example['input'], example['output']):
                        return False

        return True
    except Exception:
        return False

def load_solution(solution_path):
    """Load the solution function from a file. Returns function or None."""
    try:
        with open(solution_path, 'rb') as f:
            file_content = f.read()

        namespace = {}
        try:
            exec(file_content, namespace)
        except Exception as exec_error:
            try:
                text_content = file_content.decode('utf-8')
                exec(text_content, namespace)
            except Exception:
                raise exec_error

        if 'p' in namespace:
            return namespace['p']
        else:
            return None
    except Exception:
        return None

print("=" * 60)
print("FINAL COMPARISON: Best vs Public-6 vs Public-7")
print("=" * 60)

# Create Best directory
os.makedirs("Best-Updated", exist_ok=True)

best_better = 0
public3_better = 0
public4_better = 0
equal = 0
best_only = 0
public3_only = 0
public4_only = 0

for f in range(1, 401):
    task_name = f"task{str(f).zfill(3)}.py"
    best_path_src = f"Best/{task_name}"
    public3_path = f"Public-6/{task_name}"
    public4_path = f"Public-7/{task_name}"
    best_path = f"Best-Updated/{task_name}"

    best_exists = os.path.exists(best_path_src)
    public3_exists = os.path.exists(public3_path)
    public4_exists = os.path.exists(public4_path)

    if not best_exists and not public3_exists and not public4_exists:
        continue

    # Get sizes, paths, and test results for existing files
    candidates = []
    if best_exists:
        best_size = len(open(best_path_src, "rb").read())
        best_func = load_solution(best_path_src)
        best_passes = test_all_examples(best_func, f) if best_func else False
        candidates.append((best_size, best_path_src, "Best", best_passes))
    if public3_exists:
        public3_size = len(open(public3_path, "rb").read())
        public3_func = load_solution(public3_path)
        public3_passes = test_all_examples(public3_func, f) if public3_func else False
        candidates.append((public3_size, public3_path, "Public-6", public3_passes))
    if public4_exists:
        public4_size = len(open(public4_path, "rb").read())
        public4_func = load_solution(public4_path)
        public4_passes = test_all_examples(public4_func, f) if public4_func else False
        candidates.append((public4_size, public4_path, "Public-7", public4_passes))

    # Filter to only passing solutions
    passing_candidates = [c for c in candidates if c[3]]

    if not passing_candidates:
        print(f"Task {f:3d}: NO PASSING SOLUTIONS - skipping")
        continue

    # Find the best (smallest) passing solution
    best_size, best_source_path, best_source_name, _ = min(passing_candidates, key=lambda x: x[0])

    # Count how many passing files have the same best size
    best_count = sum(1 for size, _, _, _ in passing_candidates if size == best_size)

    if len(passing_candidates) == 1:
        # Only one source exists and passes
        source_name = passing_candidates[0][2]
        if source_name == "Best":
            best_only += 1
        elif source_name == "Public-6":
            public3_only += 1
        else:  # Public-7
            public4_only += 1
        print(f"Task {f:3d}: {source_name:9} ONLY   ({best_size} bytes)")
    elif best_count > 1:
        # Multiple sources have the same best size and pass
        equal += 1
        sources = [name for size, _, name, _ in passing_candidates if size == best_size]
        print(f"Task {f:3d}: Equal size       ({best_size} bytes) - {', '.join(sources)}")
    else:
        # One source is clearly better
        if best_source_name == "Best":
            best_better += 1
        elif best_source_name == "Public-6":
            public3_better += 1
        else:  # Public-7
            public4_better += 1

        # Show comparison with other passing sources
        other_sizes = [f"{name}:{size}" for size, _, name, _ in passing_candidates if name != best_source_name]
        print(f"Task {f:3d}: {best_source_name:9} BETTER ({best_size} bytes) vs {', '.join(other_sizes)}")

    # Copy the best solution to Best directory
    shutil.copy2(best_source_path, best_path)

print("\n" + "=" * 60)
print("SUMMARY:")
print(f"Best better:      {best_better}")
print(f"Public-6 better:  {public3_better}")
print(f"Public-7 better:  {public4_better}")
print(f"Equal size:       {equal}")
print(f"Best only:        {best_only}")
print(f"Public-6 only:    {public3_only}")
print(f"Public-7 only:    {public4_only}")
print(f"Total tasks:      {best_better + public3_better + public4_better + equal + best_only + public3_only + public4_only}")
print("=" * 60)
print(f"Best solutions copied to 'Best-Updated/' directory")