# Final comparison between Best, Public-3, and Public-4
import os
import shutil

print("=" * 60)
print("FINAL COMPARISON: Best vs Public-3 vs Public-4")
print("=" * 60)

# Create Best directory
os.makedirs("Best", exist_ok=True)

best_better = 0
public3_better = 0
public4_better = 0
equal = 0
best_only = 0
public3_only = 0
public4_only = 0

for f in range(1, 401):
    task_name = f"task{str(f).zfill(3)}.py"
    best_path_src = f"Best/{task_name}"
    public3_path = f"Public-3/{task_name}"
    public4_path = f"Public-4/{task_name}"
    best_path = f"Best_Updated/{task_name}"

    best_exists = os.path.exists(best_path_src)
    public3_exists = os.path.exists(public3_path)
    public4_exists = os.path.exists(public4_path)

    if not best_exists and not public3_exists and not public4_exists:
        continue

    # Get sizes and paths for existing files
    candidates = []
    if best_exists:
        best_size = len(open(best_path_src, "rb").read())
        candidates.append((best_size, best_path_src, "Best"))
    if public3_exists:
        public3_size = len(open(public3_path, "rb").read())
        candidates.append((public3_size, public3_path, "Public-3"))
    if public4_exists:
        public4_size = len(open(public4_path, "rb").read())
        candidates.append((public4_size, public4_path, "Public-4"))

    # Find the best (smallest) solution
    best_size, best_source_path, best_source_name = min(candidates, key=lambda x: x[0])

    # Count how many files have the same best size
    best_count = sum(1 for size, _, _ in candidates if size == best_size)

    if len(candidates) == 1:
        # Only one source exists
        source_name = candidates[0][2]
        if source_name == "Best":
            best_only += 1
        elif source_name == "Public-3":
            public3_only += 1
        else:  # Public-4
            public4_only += 1
        print(f"Task {f:3d}: {source_name:9} ONLY   ({best_size} bytes)")
    elif best_count > 1:
        # Multiple sources have the same best size
        equal += 1
        sources = [name for size, _, name in candidates if size == best_size]
        print(f"Task {f:3d}: Equal size       ({best_size} bytes) - {', '.join(sources)}")
    else:
        # One source is clearly better
        if best_source_name == "Best":
            best_better += 1
        elif best_source_name == "Public-3":
            public3_better += 1
        else:  # Public-4
            public4_better += 1

        # Show comparison with other sources
        other_sizes = [f"{name}:{size}" for size, _, name in candidates if name != best_source_name]
        print(f"Task {f:3d}: {best_source_name:9} BETTER ({best_size} bytes) vs {', '.join(other_sizes)}")

    # Copy the best solution to Best directory
    shutil.copy2(best_source_path, best_path)

print("\n" + "=" * 60)
print("SUMMARY:")
print(f"Best better:      {best_better}")
print(f"Public-3 better:  {public3_better}")
print(f"Public-4 better:  {public4_better}")
print(f"Equal size:       {equal}")
print(f"Best only:        {best_only}")
print(f"Public-3 only:    {public3_only}")
print(f"Public-4 only:    {public4_only}")
print(f"Total tasks:      {best_better + public3_better + public4_better + equal + best_only + public3_only + public4_only}")
print("=" * 60)
print(f"Best solutions copied to 'Best_Updated/' directory")