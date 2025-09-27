import os
import csv

def get_character_count(filepath):
    """Count characters in the same manner as verify.py (file size in bytes)"""
    if not os.path.exists(filepath):
        return "-"

    try:
        # verify.py uses os.path.getsize() to count characters
        return os.path.getsize(filepath)
    except:
        return "-"

def main():
    best_scores = {}
    with open('best_scores.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0]:
                task_num = int(row[0])
                score = int(row[1])
                best_scores[task_num] = score

    with open('score_log.txt', 'w') as out:
        out.write(f"{'Task':<10} {'Public':<8} {'Private':<10} {'Best':<6} {'Deficit':<8}\n")
        out.write("-" * 44 + "\n")

        for task_num in range(1, 401):
            public_path = f"Public-Compressed/task{task_num:03d}.py"
            solution_path = f"Private-Compressed/task{task_num:03d}.py"

            public_size = get_character_count(public_path)
            solution_size = get_character_count(solution_path)
            best_score = best_scores.get(task_num, "-")

            # Calculate deficit based on minimum of all available scores
            available_sizes = []
            if public_size != "-":
                available_sizes.append(public_size)
            if solution_size != "-":
                available_sizes.append(solution_size)

            if available_sizes and best_score != "-":
                min_size = min(available_sizes)
                deficit = min_size - best_score
            else:
                deficit = "-"

            public_display = str(public_size) if public_size != "-" else "-"
            solution_display = str(solution_size) if solution_size != "-" else "-"
            best_display = str(best_score) if best_score != "-" else "-"
            deficit_display = str(deficit) if deficit != "-" else "-"

            out.write(f"Task {task_num:<5} {public_display:<8} {solution_display:<10} {best_display:<6} {deficit_display:<8}\n")

def create_deficit_sorted_log():
    """Create score_log_deficit.txt sorted by deficit (largest to smallest)"""
    best_scores = {}
    with open('best_scores.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0]:
                task_num = int(row[0])
                score = int(row[1])
                best_scores[task_num] = score

    # Collect all task data
    task_data = []
    for task_num in range(1, 401):
        public_path = f"Public-Compressed/task{task_num:03d}.py"
        solution_path = f"Private-Compressed/task{task_num:03d}.py"

        public_size = get_character_count(public_path)
        solution_size = get_character_count(solution_path)
        best_score = best_scores.get(task_num, "-")

        # Calculate deficit based on minimum of all available scores
        available_sizes = []
        if public_size != "-":
            available_sizes.append(public_size)
        if solution_size != "-":
            available_sizes.append(solution_size)

        if available_sizes and best_score != "-":
            min_size = min(available_sizes)
            deficit = min_size - best_score
        else:
            deficit = "-"

        task_data.append({
            'task_num': task_num,
            'public_size': public_size,
            'solution_size': solution_size,
            'best_score': best_score,
            'deficit': deficit
        })

    # Sort by deficit (largest to smallest)
    # Put numeric deficits first (sorted descending), then "-" entries at the end
    def sort_key(item):
        if item['deficit'] == "-":
            return (-float('inf'), item['task_num'])  # Put "-" at end, sorted by task number
        else:
            return (-item['deficit'], item['task_num'])  # Negative for descending order

    task_data.sort(key=sort_key)

    # Write sorted data to file
    with open('score_log_deficit.txt', 'w') as out:
        out.write(f"{'Task':<10} {'Public':<8} {'Private':<10} {'Best':<6} {'Deficit':<8}\n")
        out.write("-" * 44 + "\n")

        for data in task_data:
            public_display = str(data['public_size']) if data['public_size'] != "-" else "-"
            solution_display = str(data['solution_size']) if data['solution_size'] != "-" else "-"
            best_display = str(data['best_score']) if data['best_score'] != "-" else "-"
            deficit_display = str(data['deficit']) if data['deficit'] != "-" else "-"

            out.write(f"Task {data['task_num']:<5} {public_display:<8} {solution_display:<10} {best_display:<6} {deficit_display:<8}\n")

if __name__ == "__main__":
    main()
    create_deficit_sorted_log()
    print("Created score_log.txt and score_log_deficit.txt")