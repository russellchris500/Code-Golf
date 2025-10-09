import json
import os

def count_nonzero(grid):
    """Count non-zero cells in a grid"""
    return sum(1 for row in grid for cell in row if cell != 0)

def get_dimensions(grid):
    """Get dimensions of a grid"""
    if not grid:
        return (0, 0)
    return (len(grid), len(grid[0]) if grid else 0)

def analyze_task_details(task_num):
    """Get detailed analysis of a task for regex suitability"""
    filepath = f"Examples/task{task_num:03d}.json"

    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        return None

    all_input_dims = []
    all_output_dims = []
    examples_data = []

    # Check all categories
    for category in ['train', 'test', 'arc-gen']:
        if category not in data:
            continue

        examples = data[category]
        for example in examples:
            if 'input' in example and 'output' in example:
                input_grid = example['input']
                output_grid = example['output']

                input_dims = get_dimensions(input_grid)
                output_dims = get_dimensions(output_grid)

                all_input_dims.append(input_dims)
                all_output_dims.append(output_dims)

                input_nonzero = count_nonzero(input_grid)
                output_nonzero = count_nonzero(output_grid)

                examples_data.append({
                    'input': input_nonzero,
                    'output': output_nonzero,
                    'input_dims': input_dims,
                    'output_dims': output_dims,
                    'input_grid': input_grid,
                    'output_grid': output_grid
                })

    if not all_input_dims:
        return None

    # Check if all dimensions are the same
    unique_input_dims = set(all_input_dims)
    unique_output_dims = set(all_output_dims)
    same_io_dims = all_input_dims == all_output_dims

    if len(unique_input_dims) == 1 and len(unique_output_dims) == 1 and same_io_dims:
        dims = list(unique_input_dims)[0]
        max_dim = max(dims)

        if max_dim <= 10:  # Focus on very small grids
            avg_input = sum(e['input'] for e in examples_data) / len(examples_data)
            avg_output = sum(e['output'] for e in examples_data) / len(examples_data)

            # Calculate how many cells change on average
            total_changes = 0
            for e in examples_data:
                changes = 0
                for i in range(len(e['input_grid'])):
                    for j in range(len(e['input_grid'][i])):
                        if e['input_grid'][i][j] != e['output_grid'][i][j]:
                            changes += 1
                total_changes += changes
            avg_changes = total_changes / len(examples_data)

            return {
                'task': task_num,
                'dims': dims,
                'total_cells': dims[0] * dims[1],
                'avg_input_cells': avg_input,
                'avg_output_cells': avg_output,
                'avg_changes': avg_changes,
                'num_examples': len(examples_data)
            }

    return None

def main():
    print("Analyzing tasks for BEST regex candidates (grids <=10x10)...\n")

    candidates = []

    for task_num in range(1, 401):
        result = analyze_task_details(task_num)
        if result:
            candidates.append(result)

    # Sort by grid size, then by number of changes
    candidates.sort(key=lambda x: (x['total_cells'], x['avg_changes']))

    print(f"Found {len(candidates)} tasks with fixed dimensions <=10x10\n")
    print("="*90)
    print("BEST REGEX CANDIDATES (sorted by grid size, then cell changes)")
    print("="*90)
    print()

    for c in candidates:
        cell_diff = c['avg_output_cells'] - c['avg_input_cells']
        diff_str = f"+{cell_diff:.1f}" if cell_diff >= 0 else f"{cell_diff:.1f}"

        print(f"task{c['task']:03d}: {c['dims'][0]:2d}x{c['dims'][1]:2d} "
              f"({c['total_cells']:3d} cells) | "
              f"Input: {c['avg_input_cells']:5.1f} -> Output: {c['avg_output_cells']:5.1f} ({diff_str:6s}) | "
              f"Avg {c['avg_changes']:5.1f} cells change")

    # Highlight the top candidates
    print("\n" + "="*90)
    print("TOP 20 CANDIDATES (smallest grids with fewest changes)")
    print("="*90)
    print()

    # Focus on tasks where output is similar to input (small modifications)
    simple_transforms = [c for c in candidates if abs(c['avg_changes']) < c['total_cells'] * 0.5]
    simple_transforms.sort(key=lambda x: (x['total_cells'], x['avg_changes']))

    for i, c in enumerate(simple_transforms[:20], 1):
        print(f"{i:2d}. task{c['task']:03d}: {c['dims'][0]}x{c['dims'][1]} "
              f"- avg {c['avg_changes']:.1f} cells change "
              f"({c['avg_input_cells']:.0f}->{c['avg_output_cells']:.0f} filled)")

if __name__ == "__main__":
    main()
