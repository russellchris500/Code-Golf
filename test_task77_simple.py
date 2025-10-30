import json
import sys

# Load the solution
with open('Work/task077.py', 'rb') as f:
    exec(f.read())

# Load the task data
with open('Examples/task077.json', 'r') as f:
    data = json.load(f)

# Test all examples
all_pass = True
total = 0
passed = 0

for category in ['train', 'test', 'arc-gen']:
    if category in data:
        for i, example in enumerate(data[category]):
            total += 1
            result = p(example['input'])
            if result == example['output']:
                passed += 1
                print(f"{category}[{i}]: PASS")
            else:
                all_pass = False
                print(f"{category}[{i}]: FAIL")

print(f"\n{passed}/{total} passed")

# Count characters
with open('Work/task077.py', 'rb') as f:
    char_count = len(f.read())
print(f"Character count: {char_count}")

sys.exit(0 if all_pass else 1)
