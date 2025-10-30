# Comparison between Best-Updated and Public-8 (by file size only)
import os
import shutil

print("=" * 60)
print("COMPARISON: Best-Updated vs Public-8 (file size only)")
print("=" * 60)

# Create Best directory
os.makedirs("Best-Updated-2", exist_ok=True)

best_better = 0
public8_better = 0
equal = 0
best_only = 0
public8_only = 0

for f in range(1, 401):
    task_name = f"task{str(f).zfill(3)}.py"
    best_path_src = f"Best-Updated/{task_name}"
    public8_path = f"Public-8/{task_name}"
    best_path = f"Best-Updated-2/{task_name}"

    best_exists = os.path.exists(best_path_src)
    public8_exists = os.path.exists(public8_path)

    if not best_exists and not public8_exists:
        continue

    # Get sizes and paths for existing files
    candidates = []
    if best_exists:
        best_size = len(open(best_path_src, "rb").read())
        candidates.append((best_size, best_path_src, "Best-Updated"))
    if public8_exists:
        public8_size = len(open(public8_path, "rb").read())
        candidates.append((public8_size, public8_path, "Public-8"))

    # Find the best (smallest) solution
    best_size, best_source_path, best_source_name = min(candidates, key=lambda x: x[0])

    # Count how many files have the same best size
    best_count = sum(1 for size, _, _ in candidates if size == best_size)

    if len(candidates) == 1:
        # Only one source exists
        source_name = candidates[0][2]
        if source_name == "Best-Updated":
            best_only += 1
        else:  # Public-8
            public8_only += 1
        print(f"Task {f:3d}: {source_name:12} ONLY   ({best_size} bytes)")
    elif best_count > 1:
        # Multiple sources have the same best size
        equal += 1
        sources = [name for size, _, name in candidates if size == best_size]
        print(f"Task {f:3d}: Equal size       ({best_size} bytes) - {', '.join(sources)}")
    else:
        # One source is clearly better
        if best_source_name == "Best-Updated":
            best_better += 1
        else:  # Public-8
            public8_better += 1

        # Show comparison with other sources
        other_sizes = [f"{name}:{size}" for size, _, name in candidates if name != best_source_name]
        print(f"Task {f:3d}: {best_source_name:12} BETTER ({best_size} bytes) vs {', '.join(other_sizes)}")

    # Copy the best solution to Best directory
    shutil.copy2(best_source_path, best_path)

print("\n" + "=" * 60)
print("SUMMARY:")
print(f"Best-Updated better: {best_better}")
print(f"Public-8 better:     {public8_better}")
print(f"Equal size:          {equal}")
print(f"Best-Updated only:   {best_only}")
print(f"Public-8 only:       {public8_only}")
print(f"Total tasks:         {best_better + public8_better + equal + best_only + public8_only}")
print("=" * 60)
print(f"Best solutions copied to 'Best-Updated-2/' directory")