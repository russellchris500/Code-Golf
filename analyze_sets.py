import os
import re
from pathlib import Path

def analyze_file(filepath):
    """Analyze a solution file for set operation opportunities."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()

    opportunities = []
    lines = content.split('\n')

    # Pattern: list comprehension with conditionals that could be set ops
    # [x for x in A if x not in B] -> list(set(A)-set(B))
    if re.search(r'\[.*for.*in.*if.*not in', content):
        opportunities.append("Set difference: [x for x in A if x not in B] -> list(set(A)-set(B)) or A-B if sets")

    # [x for x in A if x in B] -> list(set(A)&set(B))
    if re.search(r'\[.*for.*in.*if.*\sin\s', content):
        opportunities.append("Set intersection: [x for x in A if x in B] -> list(set(A)&set(B))")

    # Multiple 'in' checks could use set membership
    if content.count(' in ') > 3 or content.count(' not in ') > 2:
        opportunities.append("Multiple membership tests - consider converting to set for O(1) lookup")

    # Union patterns: A + [x for x in B if x not in A]
    if re.search(r'\+\s*\[.*if.*not in', content):
        opportunities.append("Union: A+[x for x in B if x not in A] -> list(set(A)|set(B))")

    # XOR/symmetric difference patterns
    if 'symmetric' in content.lower() or ('difference' in content.lower() and 'symmetric' in content.lower()):
        opportunities.append("Symmetric difference: set(A)^set(B) for elements in A or B but not both")

    # Detecting unique elements
    if re.search(r'list\(set\(.*\)\)', content) and 'len' not in content:
        opportunities.append("Converting to set and back - may optimize with set operations")

    # Remove duplicates while preserving order (could sometimes use sets)
    if re.search(r'(unique|distinct|duplicates?)', content.lower()):
        opportunities.append("Duplicate handling - verify if set operations can help")

    # Check for filtering patterns
    if re.search(r'filter\(', content):
        opportunities.append("filter() usage - may convert to set operations if doing membership tests")

    # Look for &, |, -, ^ already used (good!)
    set_ops_used = []
    if '&' in content and 'and' not in content:
        set_ops_used.append('& (intersection)')
    if '|' in content and 'or' not in content:
        set_ops_used.append('| (union)')
    if re.search(r'(?<!\w)-(?!\w)', content):
        set_ops_used.append('- (difference)')
    if '^' in content and '**' not in content:
        set_ops_used.append('^ (symmetric diff)')

    return opportunities, set_ops_used, len(content)

def main():
    solutions_dir = Path('Solutions')
    work_dir = Path('Work')
    private_dir = Path('Private-Uncompressed')

    all_dirs = [d for d in [solutions_dir, work_dir, private_dir] if d.exists()]

    results = []

    for directory in all_dirs:
        for filepath in sorted(directory.glob('task*.py')):
            opportunities, set_ops_used, char_count = analyze_file(filepath)

            if opportunities or set_ops_used:
                task_num = re.search(r'task(\d+)', filepath.name)
                task_num = task_num.group(1) if task_num else '???'

                results.append({
                    'file': str(filepath),
                    'task': task_num,
                    'opportunities': opportunities,
                    'set_ops_used': set_ops_used,
                    'chars': char_count
                })

    # Print report
    print("=" * 80)
    print("SET OPERATION OPTIMIZATION ANALYSIS")
    print("=" * 80)
    print()

    # Files already using set operations
    print("FILES ALREADY USING SET OPERATIONS:")
    print("-" * 80)
    using_sets = [r for r in results if r['set_ops_used']]
    for r in using_sets:
        print(f"Task {r['task']:>3} ({r['chars']:>4} chars): {', '.join(r['set_ops_used'])}")
        print(f"  File: {r['file']}")
        print()

    print()
    print("=" * 80)
    print("POTENTIAL OPTIMIZATION OPPORTUNITIES:")
    print("-" * 80)

    has_opportunities = [r for r in results if r['opportunities']]
    for r in has_opportunities:
        print(f"\nTask {r['task']:>3} ({r['chars']:>4} chars)")
        print(f"  File: {r['file']}")
        for opp in r['opportunities']:
            print(f"  - {opp}")

    print()
    print("=" * 80)
    print(f"SUMMARY: {len(using_sets)} files using set ops, {len(has_opportunities)} with potential optimizations")
    print("=" * 80)

if __name__ == '__main__':
    main()
