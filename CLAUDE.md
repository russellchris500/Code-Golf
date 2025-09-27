# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google Code Golf 2025 competition project focused on solving ARC-AGI style puzzles using minimal character count. The competition involves writing compact Python functions that transform input grids to output grids based on pattern recognition.

## Architecture

### Core Components

1. **viewer.py**: Interactive visualization tool for examining task examples
   - Displays input/output grid pairs with colored cells (10-color palette, values 0-9)
   - Navigates through train/test/arc-gen example categories
   - Task 0 displays built-in example, tasks 1-400 load from JSON files

2. **test.py**: Interactive testing interface for solutions
   - Real-time testing of solutions against all examples
   - Shows input, expected output, and actual output side-by-side
   - Color-coded PASS/FAIL status for each test case
   - Loads solutions from `Solutions/task*.py` files

3. **verify.py**: Command-line verification tool
   - JSON output with success status and character count
   - Exit code 0 on success, 1 on failure
   - Searches multiple paths for solution files

4. **zipit.py**: Creates submission.zip from Solutions folder
   - Packages all `task*.py` files for Kaggle submission
   - Strips directory structure (files at root of zip)

### Solution Structure

Solutions must be in `Solutions/task{num:03d}.py` and define:
```python
def p(i):
    # Transform input grid i to output grid
    return output_grid
```

Input/output format: List of lists containing integers 0-9

## Common Commands

```bash
# Visualize task examples
python viewer.py  # Enter task number in GUI

# Test a solution interactively
python test.py    # Enter task number in GUI

# Verify solution from command line
python verify.py <task_num>              # Verifies task.py
python verify.py <task_num> Solutions/task001.py  # Specific file

# Create submission zip
python zipit.py   # Creates submission.zip from Solutions folder
```

## Verification Output Format

```json
{
  "success": true,
  "character_count": 123,
  "arc_agi_pass": 10,
  "arc_agi_fail": 0,
  "arc_gen_pass": 5,
  "arc_gen_fail": 0,
  "task_number": 1
}
```

## Important Notes

- Solutions are tested on both ARC-AGI (train+test) and ARC-GEN examples
- Character count includes entire file (minimize whitespace and variable names)
- The code_golf_utils module adapts paths for both local and Kaggle environments
- Task files located in `Examples/task{num:03d}.json`
- Work folder contains in-progress solutions

## Working with Task Files

**WARNING**: The JSON files in Examples/ are very large (often >70,000 tokens) and will exceed token limits if read directly.

**DO NOT**: Attempt to read entire Examples/task*.json files using the Read tool.

**INSTEAD**:
- Rely on the user's description of the problem
- Use verify.py to test solutions - it automatically loads and tests against all examples
- If you must inspect examples, use Python to programmatically load specific parts:
  ```python
  import json
  with open('Examples/task001.json') as f:
      data = json.load(f)
      # Inspect specific examples programmatically
  ```
- Use Grep to search for specific patterns if needed

When solving a problem, the user will provide a description of the basics of solving the problem. Use the principles of python code golf to write a function p(g) that solves the problem. The function and other code should be in a file named task###.py. Place the file in the Work directory. Report success of failure and the number of bytes used by checking with the verify.py program. Debug if any failure occurs.
Don't use interactive testing with viewer and test.