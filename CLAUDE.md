# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google Code Golf 2025 competition project focused on solving ARC-AGI style puzzles. The codebase consists of:
- A Tkinter-based viewer application for visualizing task examples
- Utilities for loading and verifying solutions
- JSON task files containing puzzle input/output pairs

## Architecture

### Main Components

1. **viewer.py**: Tkinter GUI application for visualizing code golf tasks
   - Displays input/output grids with colored cells
   - Supports navigation through train/test/arc-gen examples
   - Uses the code_golf_utils module for color definitions

2. **Examples/code_golf_utils/code_golf_utils.py**: Core utilities module
   - `load_examples(task_num)`: Loads task data from JSON files
   - `verify_program(task_num, examples)`: Validates solutions against test cases
   - `show_examples()`: Matplotlib-based visualization
   - Color palette definition (10 colors mapped to values 0-9)
   - Expects solutions to be in `/kaggle/working/task.py` with a function `p()`

3. **Task Files**: `Examples/task*.json` (task001.json through task400.json)
   - Each contains "train", "test", and "arc-gen" sections
   - Each section has input/output grid pairs

## Common Development Tasks

### Running the Viewer
```bash
python viewer.py
```
Enter task number (0 for built-in example, 1-400 for task files) to visualize puzzle examples.

### Solution Structure
Solutions should define a function `p(input_grid)` that transforms the input grid to produce the output grid. The function must return a list of lists matching the expected output format.

## Key Implementation Notes

- The code_golf_utils module expects to run in a Kaggle environment (`/kaggle/input/google-code-golf-2025/`)
- Solutions are verified by deep copying inputs and comparing numpy array outputs
- Valid outputs must contain only numeric values (0-9) in list format
- The viewer uses a fixed color palette where each number 0-9 maps to a specific RGB color