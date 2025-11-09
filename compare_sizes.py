import os
from pathlib import Path

private_dir = Path("Work")
best_dir = Path("Best-Updated-2")

# Get all task files from Work
private_files = sorted(private_dir.glob("task*.py"))

improvements = []
all_comparisons = []

for private_file in private_files:
    best_file = best_dir / private_file.name

    if best_file.exists():
        private_size = private_file.stat().st_size
        best_size = best_file.stat().st_size

        all_comparisons.append({
            'task': private_file.name,
            'private': private_size,
            'best': best_size,
            'diff': private_size - best_size
        })

        if private_size < best_size:
            improvements.append({
                'task': private_file.name,
                'private': private_size,
                'best': best_size,
                'savings': best_size - private_size
            })

print(f"Tasks where Work is SMALLER than Best-Updated-2:\n")
if improvements:
    for imp in improvements:
        print(f"{imp['task']:15} Work: {imp['private']:4} bytes  Best: {imp['best']:4} bytes  Savings: {imp['savings']:4} bytes")
    print(f"\n{'='*80}")
    print(f"\nTotal: {len(improvements)} tasks with potential savings of {sum(imp['savings'] for imp in improvements)} bytes")
else:
    print("No improvements found - Best-Updated-2 is smaller or equal for all tasks.")
