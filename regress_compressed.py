import os
import re

def is_compressed(content):
    """Check if a file uses zlib compression."""
    # Only consider files that import zlib
    if 'zlib' in content:
        return True
    return False

def get_file_size(filepath):
    """Get file size in bytes."""
    try:
        return os.path.getsize(filepath)
    except:
        return None

# Collect data
data = []
compressed_tasks = []

# Get all task files from Public-Compressed
public_compressed_files = [f for f in os.listdir('Public-Compressed') if f.endswith('.py') and f.startswith('task')]

for filename in public_compressed_files:
    task_num = filename[4:7]  # Extract task number

    # Read Public-Compressed file
    compressed_path = os.path.join('Public-Compressed', filename)
    try:
        with open(compressed_path, 'r', encoding='utf-8', errors='ignore') as f:
            compressed_content = f.read()
    except Exception as e:
        continue

    # Check if it's actually compressed
    if not is_compressed(compressed_content):
        continue

    compressed_tasks.append(task_num)
    compressed_size = get_file_size(compressed_path)

    # Get uncompressed size from Public-Uncompressed
    uncompressed_path = os.path.join('Public-Uncompressed', filename)
    uncompressed_size = get_file_size(uncompressed_path)

    if compressed_size and uncompressed_size:
        data.append({
            'task': task_num,
            'compressed': compressed_size,
            'uncompressed': uncompressed_size
        })

print(f"Found {len(compressed_tasks)} zlib-compressed files in Public-Compressed")
print(f"Compressed tasks: {', '.join(sorted(compressed_tasks))}")

if len(data) < 2:
    print("\nInsufficient data for regression analysis.")
    print("Data collected:")
    for d in data:
        print(f"  Task {d['task']}: Compressed={d['compressed']} bytes, Uncompressed={d['uncompressed']} bytes")
else:
    # Calculate linear regression
    n = len(data)
    sum_x = sum(d['uncompressed'] for d in data)
    sum_y = sum(d['compressed'] for d in data)
    sum_x2 = sum(d['uncompressed']**2 for d in data)
    sum_xy = sum(d['uncompressed'] * d['compressed'] for d in data)

    # Calculate slope (m) and intercept (b) for y = mx + b
    # where y = compressed size, x = uncompressed size
    denominator = n * sum_x2 - sum_x**2
    if denominator != 0:
        m = (n * sum_xy - sum_x * sum_y) / denominator
        b = (sum_y - m * sum_x) / n

        # Calculate correlation coefficient
        mean_x = sum_x / n
        mean_y = sum_y / n

        numerator = sum((d['uncompressed'] - mean_x) * (d['compressed'] - mean_y) for d in data)
        denom_x = sum((d['uncompressed'] - mean_x)**2 for d in data)**0.5
        denom_y = sum((d['compressed'] - mean_y)**2 for d in data)**0.5

        if denom_x * denom_y != 0:
            r = numerator / (denom_x * denom_y)
        else:
            r = 0

        print("\n" + "="*60)
        print("LINEAR REGRESSION ANALYSIS")
        print("="*60)
        print(f"Number of data points: {n}")
        print(f"\nRegression equation:")
        print(f"  Compressed Size = {m:.4f} * Uncompressed Size + {b:.2f}")
        print(f"\nCorrelation coefficient (r): {r:.4f}")
        print(f"R-squared: {r**2:.4f}")

        print("\n" + "-"*60)
        print("Data points:")
        print("-"*60)
        print(f"{'Task':<8} {'Uncompressed':<15} {'Compressed':<15} {'Ratio':<10}")
        print("-"*60)
        for d in sorted(data, key=lambda x: x['uncompressed']):
            ratio = d['compressed'] / d['uncompressed'] if d['uncompressed'] > 0 else 0
            print(f"task{d['task']:<4} {d['uncompressed']:<15} {d['compressed']:<15} {ratio:.2%}")

        # Statistics
        print("\n" + "-"*60)
        print("Summary Statistics:")
        print("-"*60)
        avg_uncompressed = sum_x / n
        avg_compressed = sum_y / n
        avg_ratio = avg_compressed / avg_uncompressed if avg_uncompressed > 0 else 0

        print(f"Average uncompressed size: {avg_uncompressed:.0f} bytes")
        print(f"Average compressed size: {avg_compressed:.0f} bytes")
        print(f"Average compression ratio: {avg_ratio:.2%}")

    else:
        print("Error: Unable to calculate regression (denominator is zero)")