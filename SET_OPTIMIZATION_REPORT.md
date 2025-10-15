# Set Operation Optimization Report

## Executive Summary

Analyzed all solution files (Solutions/, Work/, Private-Uncompressed/) for opportunities to use Python set operations to reduce character count.

### Key Findings

- **53 files already using set operations** (∩, ∪, -, ^) - Good job!
- **~150+ files with potential optimization opportunities**
- Most common opportunities: List comprehensions with membership tests

## Set Operations Quick Reference

| Operation | Set Syntax | List Comprehension | Savings |
|-----------|------------|-------------------|---------|
| Intersection | `set(A)&set(B)` | `[x for x in A if x in B]` | ~8-15 chars |
| Difference | `set(A)-set(B)` | `[x for x in A if x not in B]` | ~12-20 chars |
| Union | `set(A)\|set(B)` | `A+[x for x in B if x not in A]` | ~15-30 chars |
| Symmetric Diff | `set(A)^set(B)` | Elements in A or B but not both | ~20-40 chars |

### Additional Tips

- **Unpacking sets**: `{*A}` is shorter than `set(A)` (saves 4 chars)
- **Set literals**: `{1,2,3}` vs `set([1,2,3])`
- **Membership testing**: Convert to set once if checking membership 3+ times

## Top Opportunities by Category

### Category 1: List Comprehension with `if x in`

**Pattern**: `[x for x in A if x in B]`
**Replacement**: `list(set(A)&set(B))` or `[*set(A)&set(B)]`

Files with this pattern:
- task008.py, task061.py, task137.py, task138.py
- task202.py, task209.py, task234.py, task349.py
- task014.py, task029.py, task036.py, task091.py
- task118.py, task119.py, task153.py, task158.py
- task184.py, task185.py, task247.py, task277.py
- task319.py, task355.py, task363.py
- And ~30 more...

**Example transformation**:
```python
# Before (35 chars)
[x for x in grid if x in targets]

# After (25 chars) - saves 10 chars
[*set(grid)&set(targets)]
```

### Category 2: List Comprehension with `if x not in`

**Pattern**: `[x for x in A if x not in B]`
**Replacement**: `list(set(A)-set(B))` or `[*set(A)-set(B)]`

Files with this pattern:
- task213.py, task324.py
- task034.py, task054.py, task099.py
- task224.py, task260.py

**Example transformation**:
```python
# Before (39 chars)
[x for x in items if x not in excluded]

# After (27 chars) - saves 12 chars
[*set(items)-set(excluded)]
```

### Category 3: Multiple Membership Tests

**Pattern**: Repeated `if x in list` or `if x not in list`
**Optimization**: Convert list to set once at the start

Files with 3+ membership tests:
- task001.py, task005.py, task011.py, task013.py
- task015.py, task017.py, task027.py, task066.py
- task077.py, task097.py, task104.py, task117.py
- And 100+ more...

**Example transformation**:
```python
# Before (repeated O(n) lookups)
def p(g):
    vals = [1,2,3]
    return [[c for c in row if c in vals] for row in g]

# After (O(1) lookups with set)
def p(g):
    v={1,2,3}
    return[[c for c in row if c in v]for row in g]
```

### Category 4: Filter Function with Membership

**Pattern**: `filter(lambda x: x in/not in collection, iterable)`
**Replacement**: Set operations

Files using filter with membership tests:
- task031.py, task032.py, task078.py, task383.py
- task039.py, task057.py, task177.py, task233.py, task234.py

**Example transformation**:
```python
# Before (40 chars)
list(filter(lambda x:x in valid,items))

# After (22 chars) - saves 18 chars
[*set(items)&set(valid)]
```

### Category 5: Finding Unique Elements

**Pattern**: Converting to set and back for uniqueness
**Note**: Sometimes this is already optimal, but check if you need list output

Files with potential:
- Check for `list(set(...))` patterns that could be simplified

### Category 6: Symmetric Difference Candidates

**Pattern**: Finding elements unique to each of two collections
**Replacement**: `set(A)^set(B)`

Potential files:
- Any file with 2+ "if x not in" checks going both directions
- task324.py may be a candidate

**Example transformation**:
```python
# Before (90+ chars)
unique = [x for x in A if x not in B] + [x for x in B if x not in A]

# After (17 chars) - saves 73+ chars
unique=[*set(A)^set(B)]
```

## Specific File Recommendations

### High Priority (Likely >10 char savings)

1. **task324.py** (1260 chars)
   - Multiple list comprehensions with `if x in` and `if x not in`
   - Could save 20-30 chars with set operations

2. **task213.py** (417 chars)
   - List comprehension with intersection pattern
   - Could save 10-15 chars

3. **task224.py** (331 chars)
   - List comprehension with difference pattern
   - Could save 12-18 chars

4. **task202.py** (671 chars)
   - Intersection pattern detected
   - Could save 8-12 chars

5. **task209.py** (641 chars)
   - Multiple membership tests + intersection
   - Could save 15-20 chars

### Medium Priority (5-10 char savings)

- task008.py, task014.py, task029.py, task036.py
- task061.py, task091.py, task137.py, task138.py
- task178.py, task184.py, task247.py

### Code Golf Pro Tips for Sets

1. **Use `{*X}` instead of `set(X)`** (4 char savings)
2. **Use `[*set_expr]` instead of `list(set_expr)`** (3 char savings)
3. **Chain set operations**: `{*A}&{*B}|{*C}` instead of `set(A).intersection(B).union(C)`
4. **Set literals for constants**: `{1,2,3}` instead of `set([1,2,3])`
5. **Set comprehensions**: `{x for x in...}` when you need unique results
6. **Remember operator precedence**: `&`, `|`, `-`, `^` have specific precedence

## Files Already Excelling with Set Operations

These files are already using set operations effectively:

- task041.py (49 chars) - Using `^` (symmetric diff)
- task043.py (70 chars) - Using `&` (intersection)
- task072.py (72 chars) - Using `^` (symmetric diff)
- task085.py (89 chars) - Using both `&` and `^`
- task091.py (122 chars) - Using `-` (difference)
- task178.py (77 chars) - Using `^` (symmetric diff)
- task293.py (67 chars) - Using `-` (difference)
- task309.py (39 chars) - Using `&` (intersection)
- task337.py (54 chars) - Using `^` (symmetric diff)
- task360.py (62 chars) - Using `-` (difference)

Study these for patterns!

## Action Items

1. **Immediate**: Review high-priority files for set operation conversions
2. **Short-term**: Audit all list comprehensions with `if x in/not in`
3. **Medium-term**: Convert repeated membership tests to set-based lookups
4. **Long-term**: Make set operations your default pattern for membership/filtering

## Summary Statistics

- Total files analyzed: ~400
- Files using set operations: 53 (13%)
- Files with opportunities: ~150 (38%)
- Estimated total savings: 500-1000+ characters across all files

## Notes

- Some patterns may not benefit from sets if dealing with very small collections (< 5 items)
- Order matters: Sets lose ordering, so only use when order doesn't matter or convert back to list
- Some complex comprehensions may not simplify nicely - use judgment
- Always verify with `verify.py` after making changes!
