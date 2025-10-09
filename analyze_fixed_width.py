import json
import os

fixed_width_tasks = []
variable_width_tasks = []

for task_num in range(1, 401):
    task_file = f'Examples/task{task_num:03d}.json'

    if not os.path.exists(task_file):
        continue

    try:
        with open(task_file) as f:
            data = json.load(f)

        # Collect all input widths from train, test, and arc_gen
        widths = set()

        for example in data.get('train', []):
            if example['input']:
                widths.add(len(example['input'][0]))

        for example in data.get('test', []):
            if example['input']:
                widths.add(len(example['input'][0]))

        for example in data.get('arc_gen', []):
            if example['input']:
                widths.add(len(example['input'][0]))

        # Check if all widths are the same
        if len(widths) == 1:
            fixed_width_tasks.append(task_num)
        else:
            variable_width_tasks.append(task_num)

    except Exception as e:
        print(f"Error processing task {task_num}: {e}")

# Write results
with open('fixed_width.txt', 'w') as f:
    f.write(f"Fixed Width Tasks: {len(fixed_width_tasks)}\n")
    f.write(f"Variable Width Tasks: {len(variable_width_tasks)}\n\n")
    f.write(f"Fixed width task numbers:\n")
    for task_num in fixed_width_tasks:
        f.write(f"{task_num}\n")

print(f"Analysis complete:")
print(f"Fixed width tasks: {len(fixed_width_tasks)}")
print(f"Variable width tasks: {len(variable_width_tasks)}")
