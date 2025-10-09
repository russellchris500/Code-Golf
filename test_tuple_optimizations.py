from check_for_improvement import process_task

tuple_optimized = [74, 79, 146, 191, 218, 219, 319, 324]

print(f"Processing {len(tuple_optimized)} tuple-optimized tasks...")

updated = []
failed = []
not_better = []

for task_num in tuple_optimized:
    try:
        result = process_task(task_num)

        if result['best_written']:
            updated.append(task_num)
            saved = result['best_previous_len'] - result['chosen_len']
            print(f"+ task{task_num:03d}: Updated Best_Decompressed ({result['best_previous_len']}B -> {result['chosen_len']}B, saved {saved}B)")
        elif result['validation_error']:
            failed.append(task_num)
            print(f"x task{task_num:03d}: FAILED - {result['validation_error']}")
        else:
            not_better.append(task_num)
            print(f"- task{task_num:03d}: Not better ({result['chosen_len']}B vs {result['best_previous_len']}B)")
    except Exception as e:
        failed.append(task_num)
        print(f"ERROR task{task_num:03d}: {e}")

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Updated Best_Decompressed: {len(updated)}")
print(f"  Failed: {len(failed)}")
print(f"  Not better: {len(not_better)}")

if updated:
    print(f"\nUpdated: {updated}")
if failed:
    print(f"Failed: {failed}")
