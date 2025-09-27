# Final comparison between Public-Compressed, Private-Compressed, and Public-2
import os
import shutil

print("=" * 60)
print("FINAL COMPARISON: Public vs Private vs Public-2")
print("=" * 60)

# Create Best directory
os.makedirs("Best", exist_ok=True)

private_better = 0
public_better = 0
public2_better = 0
equal = 0
private_only = 0
public_only = 0
public2_only = 0

for f in range(1, 401):
    task_name = f"task{str(f).zfill(3)}.py"
    public_path = f"Public-Compressed/{task_name}"
    private_path = f"Private-Compressed/{task_name}"
    public2_path = f"Public-2/{task_name}"
    best_path = f"Best/{task_name}"

    public_exists = os.path.exists(public_path)
    private_exists = os.path.exists(private_path)
    public2_exists = os.path.exists(public2_path)

    if not public_exists and not private_exists and not public2_exists:
        continue

    # Get sizes and paths for existing files
    candidates = []
    if public_exists:
        public_size = len(open(public_path, "rb").read())
        candidates.append((public_size, public_path, "Public"))
    if private_exists:
        private_size = len(open(private_path, "rb").read())
        candidates.append((private_size, private_path, "Private"))
    if public2_exists:
        public2_size = len(open(public2_path, "rb").read())
        candidates.append((public2_size, public2_path, "Public-2"))

    # Find the best (smallest) solution
    best_size, best_source_path, best_source_name = min(candidates, key=lambda x: x[0])

    # Count how many files have the same best size
    best_count = sum(1 for size, _, _ in candidates if size == best_size)

    if len(candidates) == 1:
        # Only one source exists
        source_name = candidates[0][2]
        if source_name == "Private":
            private_only += 1
        elif source_name == "Public":
            public_only += 1
        else:  # Public-2
            public2_only += 1
        print(f"Task {f:3d}: {source_name:8} ONLY   ({best_size} bytes)")
    elif best_count > 1:
        # Multiple sources have the same best size
        equal += 1
        sources = [name for size, _, name in candidates if size == best_size]
        print(f"Task {f:3d}: Equal size      ({best_size} bytes) - {', '.join(sources)}")
    else:
        # One source is clearly better
        if best_source_name == "Private":
            private_better += 1
        elif best_source_name == "Public":
            public_better += 1
        else:  # Public-2
            public2_better += 1

        # Show comparison with other sources
        other_sizes = [f"{name}:{size}" for size, _, name in candidates if name != best_source_name]
        print(f"Task {f:3d}: {best_source_name:8} BETTER ({best_size} bytes) vs {', '.join(other_sizes)}")

    # Copy the best solution to Best directory
    shutil.copy2(best_source_path, best_path)

print("\n" + "=" * 60)
print("SUMMARY:")
print(f"Private better:   {private_better}")
print(f"Public better:    {public_better}")
print(f"Public-2 better:  {public2_better}")
print(f"Equal size:       {equal}")
print(f"Private only:     {private_only}")
print(f"Public only:      {public_only}")
print(f"Public-2 only:    {public2_only}")
print(f"Total tasks:      {private_better + public_better + public2_better + equal + private_only + public_only + public2_only}")
print("=" * 60)
print(f"Best solutions copied to 'Best/' directory")