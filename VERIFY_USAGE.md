# Code Golf Verification Tool Usage

## Basic Usage

```bash
# Verify task.py for a specific task number
python verify.py <task_number>

# Verify a specific solution file
python verify.py <task_number> <solution_file>
```

## Examples

```bash
# Verify task.py for task 1
python verify.py 1

# Verify a specific solution file for task 1
python verify.py 1 solutions/task001.py

# Verify task 0 (built-in example)
python verify.py 0
```

## Output Format

The tool outputs JSON with the following structure:

```json
{
  "success": true/false,
  "character_count": 123,
  "arc_agi_pass": 10,
  "arc_agi_fail": 0,
  "arc_gen_pass": 5,
  "arc_gen_fail": 0,
  "error": null,
  "task_number": 1
}
```

## Exit Codes

- **0**: Solution verified successfully (all tests pass)
- **1**: Verification failed (tests failed or error occurred)

## Claude Code Usage

Claude Code can easily use this tool to verify solutions:

```bash
python verify.py 1
```

Then parse the JSON output to get:
- Success/failure status
- Character count for successful solutions
- Detailed test results
- Any error messages