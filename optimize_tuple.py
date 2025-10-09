import os
import re

def find_matching_paren(s, start):
    """Find the matching closing parenthesis"""
    count = 1
    i = start + 1
    while i < len(s) and count > 0:
        if s[i] == '(':
            count += 1
        elif s[i] == ')':
            count -= 1
        i += 1
    return i - 1 if count == 0 else -1

def optimize_tuple(content):
    """
    Optimize tuple(iterable) to (*iterable,)

    Safe patterns:
    - tuple(map(...)) -> (*map(...),)
    - tuple(sorted(...)) -> (*sorted(...),)
    - tuple(zip(...)) -> (*zip(...),)
    - tuple(filter(...)) -> (*filter(...),)

    NOT safe:
    - tuple(generator) -> (*generator,) - syntax error in some contexts
    - tuple with comprehension - might be longer
    """

    result = []
    i = 0

    while i < len(content):
        # Look for 'tuple(' pattern
        if i < len(content) - 6 and content[i:i+6] == 'tuple(':
            # Check if it's not preceded by alphanumeric or underscore
            if i == 0 or (not content[i-1].isalnum() and content[i-1] != '_'):
                # Find the matching closing paren
                close_pos = find_matching_paren(content, i + 5)
                if close_pos != -1:
                    # Extract the argument
                    arg = content[i+6:close_pos]

                    # Check if it starts with known safe functions
                    safe_functions = ['map(', 'sorted(', 'zip(', 'filter(', 'range(', 'reversed(']
                    is_safe = any(arg.startswith(func) for func in safe_functions)

                    # Also check for simple slicing like a[:]
                    if not is_safe and re.match(r'^[a-zA-Z_]\w*\[', arg):
                        is_safe = True

                    # Do NOT replace if it contains 'for' (generator/comprehension)
                    # tuple(x for ...) cannot be safely replaced with (*x for ...,)
                    if 'for' in arg or 'for\t' in arg or 'for\n' in arg:
                        is_safe = False

                    if is_safe:
                        # Replace tuple(arg) with (*arg,)
                        result.append('(*')
                        result.append(arg)
                        result.append(',)')
                        i = close_pos + 1
                        continue

        result.append(content[i])
        i += 1

    return ''.join(result)

# Process all task files
changed_files = []
total_saved = 0

for task_num in range(1, 401):
    task = f'task{task_num:03d}'
    src_file = f'Best_Decompressed/{task}.py'
    dst_file = f'Private-Uncompressed/{task}.py'

    if not os.path.exists(src_file):
        continue

    with open(src_file, 'r') as f:
        content = f.read()

    original_len = len(content)
    new_content = optimize_tuple(content)
    new_len = len(new_content)
    saved = original_len - new_len

    if new_content != content:
        with open(dst_file, 'w') as f:
            f.write(new_content)
        changed_files.append(task)
        total_saved += saved
        if saved > 0:
            print(f"+ {task}.py - Saved {saved} bytes")
        else:
            print(f"+ {task}.py - Changed (no size change)")

print(f"\nTotal files changed: {len(changed_files)}")
print(f"Total bytes saved: {total_saved}")
if changed_files:
    print(f"\nChanged files: {', '.join(changed_files)}")
