================================================================================
REGEX CANDIDATE ANALYSIS - FILES REFERENCE
================================================================================

This analysis identified 120 out of 400 Code Golf tasks that have fixed grid
dimensions and are potentially suitable for regex-based solutions.

================================================================================
FILES CREATED
================================================================================

1. REGEX_CANDIDATES_SUMMARY.txt
   - Main summary document with top recommendations
   - Organized by tiers (Tier 1 = best candidates)
   - Includes methodology and regex pattern examples
   - START HERE for understanding regex candidates

2. regex_candidates.csv
   - Complete data in CSV format for easy filtering/sorting
   - Columns: task, width, height, total_cells, avg_input_cells,
             avg_output_cells, avg_changes, num_examples, tier
   - Can be opened in Excel or processed with scripts

3. regex_candidates_report.txt
   - Full detailed report showing all 120 candidates
   - Grouped by grid dimensions (3x3, 10x10, etc.)
   - Shows input->output cell counts for each task

4. regex_best_candidates_report.txt
   - Focused report on grids <=10x10 (85 tasks)
   - Sorted by grid size and number of changes
   - Top 20 highlighted at the end

5. find_regex_candidates.py
   - Python script that performs the analysis
   - Scans all 400 task JSON files
   - Checks for fixed dimensions and calculates statistics
   - Run: python find_regex_candidates.py

6. regex_best_candidates.py
   - Focused analysis script for small grids (<=10x10)
   - Calculates average cell changes per example
   - Run: python regex_best_candidates.py

7. lookup_task.py
   - Quick lookup tool for individual tasks
   - Usage: python lookup_task.py <task_number>
   - Example: python lookup_task.py 322
   - Shows dimensions, changes, and assessment

================================================================================
QUICK START
================================================================================

To find the best regex candidates:
1. Read REGEX_CANDIDATES_SUMMARY.txt for recommendations
2. Use lookup_task.py to check specific tasks:
   python lookup_task.py 322
3. Open regex_candidates.csv for filtering/sorting

Top 10 recommended starting points:
  1. task322 (3x3, 2.8 changes)  - Best overall
  2. task380 (3x3, 3.7 changes)
  3. task266 (3x5, 3.2 changes)
  4. task073 (5x5, 3.2 changes)
  5. task081 (7x7, 2.4 changes)  - Excellent!
  6. task314 (8x8, 2.0 changes)  - Excellent!
  7. task020 (10x10, 3.0 changes)
  8. task143 (10x10, 3.5 changes)
  9. task333 (10x10, 4.0 changes)
 10. task042 (10x10, 4.0 changes)

================================================================================
KEY FINDINGS
================================================================================

- 400 tasks analyzed
- 129 tasks have fixed dimensions across all examples
- 120 tasks have fixed dimensions <=20x20
- 85 tasks have fixed dimensions <=10x10
- 13 tasks are 3x3 (best for regex golf)

Tier breakdown:
- Tier 1: 13 tasks (3x3 grids)
- Tier 2: 3 tasks (small non-square grids)
- Tier 3: 8 tasks (6x6 to 8x8 grids)
- Tier 4: 10 tasks (9x9 grids)
- Tier 5: 51 tasks (10x10 grids)
- Tier 6: 35 tasks (11x11 to 20x20 grids)

271 tasks have variable dimensions and are NOT suitable for regex.

================================================================================
METHODOLOGY
================================================================================

A task is deemed suitable for regex when:
1. All examples (train, test, arc-gen) have identical dimensions
2. Input and output grids have the same dimensions
3. Grid size is small (<=20x20, ideally <=10x10)
4. Transformation involves spatial patterns with few cell changes

The regex approach works by:
- Flattening grids into strings
- Using lookahead/lookbehind to match spatial patterns
- Example: For 10x10 grid, cell below is at offset +10

================================================================================
