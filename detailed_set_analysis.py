import re
from pathlib import Path

def analyze_specific_patterns(filepath):
    """Deep analysis of specific code patterns that could use set operations."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()

    suggestions = []

    # Pattern 1: [x for x in A if x not in B]
    pattern1 = re.findall(r'\[([^]]+)\s+for\s+(\w+)\s+in\s+([^]]+)\s+if\s+\2\s+not\s+in\s+([^]]+)\]', content)
    for match in pattern1:
        expr, var, iter_obj, check_obj = match
        if expr.strip() == var:  # Simple case: [x for x in A if x not in B]
            current = f"[{var} for {var} in {iter_obj} if {var} not in {check_obj}]"
            improved = f"list(set({iter_obj})-set({check_obj}))"
            if len(improved) < len(current):
                savings = len(current) - len(improved)
                suggestions.append({
                    'type': 'Set Difference',
                    'current': current,
                    'improved': improved,
                    'savings': savings
                })

    # Pattern 2: [x for x in A if x in B]
    pattern2 = re.findall(r'\[([^]]+)\s+for\s+(\w+)\s+in\s+([^]]+)\s+if\s+\2\s+in\s+([^]]+)\]', content)
    for match in pattern2:
        expr, var, iter_obj, check_obj = match
        if expr.strip() == var:
            current = f"[{var} for {var} in {iter_obj} if {var} in {check_obj}]"
            improved = f"list(set({iter_obj})&set({check_obj}))"
            if len(improved) < len(current):
                savings = len(current) - len(improved)
                suggestions.append({
                    'type': 'Set Intersection',
                    'current': current,
                    'improved': improved,
                    'savings': savings
                })

    # Pattern 3: Multiple 'if x not in list' checks -> convert list to set
    not_in_checks = len(re.findall(r'if\s+\w+\s+not\s+in\s+\w+', content))
    in_checks = len(re.findall(r'if\s+\w+\s+in\s+\w+', content))

    if not_in_checks >= 2 or in_checks >= 3:
        suggestions.append({
            'type': 'Convert to Set for Membership',
            'current': f'{in_checks} "in" checks, {not_in_checks} "not in" checks',
            'improved': 'Convert checked collection to set at start for O(1) lookup',
            'savings': 'Performance + possibly chars if used in comprehension'
        })

    # Pattern 4: Finding unique elements in both lists
    # Pattern like: unique_to_A = [x for x in A if x not in B]
    #               unique_to_B = [x for x in B if x not in A]
    if content.count('if x not in') >= 2 or content.count('if y not in') >= 2:
        suggestions.append({
            'type': 'Symmetric Difference Candidate',
            'current': 'Finding elements unique to each list separately',
            'improved': 'Use set(A)^set(B) for symmetric difference',
            'savings': 'Varies - often significant'
        })

    return suggestions, content

def main():
    # Focus on some specific files with opportunities
    targets = [
        'Private-Uncompressed/task202.py',
        'Private-Uncompressed/task209.py',
        'Private-Uncompressed/task324.py',
        'Private-Uncompressed/task054.py',
        'Private-Uncompressed/task099.py',
        'Private-Uncompressed/task213.py',
        'Private-Uncompressed/task224.py',
        'Private-Uncompressed/task260.py',
        'Work/task324.py',
        'Work/task213.py',
    ]

    print("=" * 80)
    print("DETAILED SET OPERATION ANALYSIS")
    print("=" * 80)
    print()

    for target in targets:
        filepath = Path(target)
        if not filepath.exists():
            continue

        suggestions, content = analyze_specific_patterns(filepath)

        if suggestions:
            print(f"\n{'=' * 80}")
            print(f"FILE: {target}")
            print(f"Current size: {len(content)} chars")
            print(f"{'=' * 80}")
            print()
            print("CODE:")
            print("-" * 80)
            print(content[:500] + ('...' if len(content) > 500 else ''))
            print()
            print("SUGGESTIONS:")
            print("-" * 80)

            for i, sugg in enumerate(suggestions, 1):
                print(f"\n{i}. {sugg['type']}")
                print(f"   Current:  {sugg['current']}")
                print(f"   Improved: {sugg['improved']}")
                print(f"   Savings:  {sugg['savings']}")
            print()

if __name__ == '__main__':
    main()
