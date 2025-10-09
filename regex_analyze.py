import json
import os

fixed_width_tasks = []
variable_width_tasks = []
same_size_tasks = []
single_color_change_tasks = []

def get_colors_used(grid):
    """Get set of colors used in grid"""
    colors = set()
    for row in grid:
        for cell in row:
            colors.add(cell)
    return colors

def has_single_color_change(inp, out):
    """Check if output differs from input by adding or removing exactly one color"""
    inp_colors = get_colors_used(inp)
    out_colors = get_colors_used(out)

    # Check if exactly one color was added or removed
    added = out_colors - inp_colors
    removed = inp_colors - out_colors

    return (len(added) == 1 and len(removed) == 0) or (len(added) == 0 and len(removed) == 1)

for task_num in range(1, 401):
    task_file = f'Examples/task{task_num:03d}.json'

    if not os.path.exists(task_file):
        continue

    try:
        with open(task_file) as f:
            data = json.load(f)

        # Collect all input widths and heights from train, test, and arc_gen
        widths = set()
        all_examples = []

        for example in data.get('train', []):
            if example['input']:
                widths.add(len(example['input'][0]))
                all_examples.append(example)

        for example in data.get('test', []):
            if example['input']:
                widths.add(len(example['input'][0]))
                all_examples.append(example)

        for example in data.get('arc_gen', []):
            if example['input']:
                widths.add(len(example['input'][0]))
                all_examples.append(example)

        # Check if all widths are the same
        if len(widths) == 1:
            fixed_width_tasks.append(task_num)

            # Check if all examples have same-sized input/output
            all_same_size = True
            for example in all_examples:
                inp = example['input']
                out = example['output']
                if len(inp) != len(out) or len(inp[0]) != len(out[0]):
                    all_same_size = False
                    break

            if all_same_size:
                same_size_tasks.append(task_num)

                # Check if all examples have single color change
                all_single_color_change = True
                for example in all_examples:
                    inp = example['input']
                    out = example['output']
                    if not has_single_color_change(inp, out):
                        all_single_color_change = False
                        break

                if all_single_color_change:
                    single_color_change_tasks.append(task_num)
        else:
            variable_width_tasks.append(task_num)

    except Exception as e:
        print(f"Error processing task {task_num}: {e}")

# Write results
with open('fixed_width.txt', 'w') as f:
    f.write(f"Fixed Width Tasks: {len(fixed_width_tasks)}\n")
    f.write(f"Variable Width Tasks: {len(variable_width_tasks)}\n")
    f.write(f"Same Size (input=output size): {len(same_size_tasks)}\n")
    f.write(f"Single Color Change: {len(single_color_change_tasks)}\n\n")

    f.write(f"Fixed width task numbers:\n")
    for task_num in fixed_width_tasks:
        f.write(f"{task_num}\n")

    f.write(f"\nSame size task numbers:\n")
    for task_num in same_size_tasks:
        f.write(f"{task_num}\n")

    f.write(f"\nSingle color change task numbers:\n")
    for task_num in single_color_change_tasks:
        f.write(f"{task_num}\n")

print(f"Analysis complete:")
print(f"Fixed width tasks: {len(fixed_width_tasks)}")
print(f"Variable width tasks: {len(variable_width_tasks)}")
print(f"Same size tasks: {len(same_size_tasks)}")
print(f"Single color change tasks: {len(single_color_change_tasks)}")
