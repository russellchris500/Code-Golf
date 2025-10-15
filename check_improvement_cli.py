#!/usr/bin/env python3
import sys
from pathlib import Path
from check_for_improvement import process_task

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_improvement_cli.py <task_number>")
        sys.exit(1)

    task_num = int(sys.argv[1])
    info = process_task(task_num)

    print(f"\n{'='*60}")
    print(f"Task {task_num:03d} Compression Results")
    print(f"{'='*60}")
    print(f"Original:    {info['original_len']:4d} bytes")
    print(f"Optimized:   {info['optimized_len']:4d} bytes")
    print(f"Compressed:  {info['compressed_len']:4d} bytes")
    print(f"Chosen:      {info['chosen_len']:4d} bytes")
    print(f"{'='*60}")

    # Private-Compressed status
    pc_prev = info['pc_previous_len']
    pc_prev_text = "NEW" if pc_prev is None else f"{pc_prev}B"
    pc_status = "UPDATED" if info['pc_written'] else "KEPT"
    print(f"Private-Compressed: {pc_prev_text} → {pc_status}")

    # Best status with validation
    best_prev = info['best_previous_len']
    best_prev_text = "NEW" if best_prev is None else f"{best_prev}B"
    best_status = "UPDATED" if info['best_written'] else "KEPT"

    if info['best_previous_len'] is None or info['chosen_len'] < info['best_previous_len']:
        if info['validation_passed']:
            validation_status = "✓ VALIDATED"
        elif info['validation_error']:
            validation_status = f"✗ FAILED: {info['validation_error']}"
            best_status = "VALIDATION FAILED"
        else:
            validation_status = "✗ FAILED"
            best_status = "VALIDATION FAILED"
    else:
        validation_status = "Not tested (not shorter)"

    print(f"Best:               {best_prev_text} → {best_status}")
    print(f"Validation:         {validation_status}")
    print(f"Best_Decompressed:  {'UPDATED' if info['best_decompressed_written'] else 'KEPT'}")
    print(f"{'='*60}\n")
