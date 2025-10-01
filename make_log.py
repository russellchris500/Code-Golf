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
        out.write(f"{'Task':<10} {'Best':<8} {'Private':<10} {'Public':<8} {'Reported':<6} {'Deficit':<8}\n")
        out.write("-" * 52 + "\n")

        for task_num in range(1, 401):
            best_path = f"Best/task{task_num:03d}.py"
            private_path = f"Private-Compressed/task{task_num:03d}.py"
            public_path = f"Public-Compressed/task{task_num:03d}.py"

            best_size = get_character_count(best_path)
            private_size = get_character_count(private_path)
            public_size = get_character_count(public_path)
            wr_score = best_scores.get(task_num, "-")

            # Calculate deficit based on minimum of all available scores from directories
            available_sizes = []
            if best_size != "-":
                available_sizes.append(best_size)
            if private_size != "-":
                available_sizes.append(private_size)
            if public_size != "-":
                available_sizes.append(public_size)

            if available_sizes and wr_score != "-":
                min_size = min(available_sizes)
                deficit = min_size - wr_score
            else:
                deficit = "-"

            best_display = str(best_size) if best_size != "-" else "-"
            private_display = str(private_size) if private_size != "-" else "-"
            public_display = str(public_size) if public_size != "-" else "-"
            wr_display = str(wr_score) if wr_score != "-" else "-"
            deficit_display = str(deficit) if deficit != "-" else "-"

            out.write(f"Task {task_num:<5} {best_display:<8} {private_display:<10} {public_display:<8} {wr_display:<6} {deficit_display:<8}\n")

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
        best_path = f"Best/task{task_num:03d}.py"
        private_path = f"Private-Compressed/task{task_num:03d}.py"
        public_path = f"Public-Compressed/task{task_num:03d}.py"

        best_size = get_character_count(best_path)
        private_size = get_character_count(private_path)
        public_size = get_character_count(public_path)
        wr_score = best_scores.get(task_num, "-")

        # Calculate deficit based on minimum of all available scores from directories
        available_sizes = []
        if best_size != "-":
            available_sizes.append(best_size)
        if private_size != "-":
            available_sizes.append(private_size)
        if public_size != "-":
            available_sizes.append(public_size)

        if available_sizes and wr_score != "-":
            min_size = min(available_sizes)
            deficit = min_size - wr_score
        else:
            deficit = "-"

        task_data.append({
            'task_num': task_num,
            'best_size': best_size,
            'private_size': private_size,
            'public_size': public_size,
            'wr_score': wr_score,
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
        out.write(f"{'Task':<10} {'Best':<8} {'Private':<10} {'Public':<8} {'Reported':<6} {'Deficit':<8}\n")
        out.write("-" * 52 + "\n")

        for data in task_data:
            best_display = str(data['best_size']) if data['best_size'] != "-" else "-"
            private_display = str(data['private_size']) if data['private_size'] != "-" else "-"
            public_display = str(data['public_size']) if data['public_size'] != "-" else "-"
            wr_display = str(data['wr_score']) if data['wr_score'] != "-" else "-"
            deficit_display = str(data['deficit']) if data['deficit'] != "-" else "-"

            out.write(f"Task {data['task_num']:<5} {best_display:<8} {private_display:<10} {public_display:<8} {wr_display:<6} {deficit_display:<8}\n")

def create_type_sorted_log():
    """Create score_log_type.txt sorted by problem type, then by deficit"""
    # Load best scores
    best_scores = {}
    with open('best_scores.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0]:
                task_num = int(row[0])
                score = int(row[1])
                best_scores[task_num] = score

    # Load ARC types
    task_types = {}
    with open('ARC types.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and len(row) >= 2:
                task_num = int(row[0])
                task_type = row[1].strip()
                task_types[task_num] = task_type

    # Collect all task data
    task_data = []
    for task_num in range(1, 401):
        best_path = f"Best/task{task_num:03d}.py"
        private_path = f"Private-Compressed/task{task_num:03d}.py"
        public_path = f"Public-Compressed/task{task_num:03d}.py"

        best_size = get_character_count(best_path)
        private_size = get_character_count(private_path)
        public_size = get_character_count(public_path)
        wr_score = best_scores.get(task_num, "-")
        task_type = task_types.get(task_num, "unknown")

        # Calculate deficit based on minimum of all available scores from directories
        available_sizes = []
        if best_size != "-":
            available_sizes.append(best_size)
        if private_size != "-":
            available_sizes.append(private_size)
        if public_size != "-":
            available_sizes.append(public_size)

        if available_sizes and wr_score != "-":
            min_size = min(available_sizes)
            deficit = min_size - wr_score
        else:
            deficit = "-"

        task_data.append({
            'task_num': task_num,
            'best_size': best_size,
            'private_size': private_size,
            'public_size': public_size,
            'wr_score': wr_score,
            'deficit': deficit,
            'type': task_type
        })

    # Sort by type (alphabetically), then by deficit (largest to smallest)
    def sort_key(item):
        type_order = item['type'] if item['type'] else "zzz_unknown"  # Put unknown at end
        if item['deficit'] == "-":
            deficit_order = -float('inf')  # Put "-" at end within each type
        else:
            deficit_order = -item['deficit']  # Negative for descending order
        return (type_order, deficit_order, item['task_num'])

    task_data.sort(key=sort_key)

    # Write sorted data to file
    with open('score_log_type.txt', 'w') as out:
        out.write(f"{'Task':<10} {'Best':<8} {'Private':<10} {'Public':<8} {'Reported':<6} {'Deficit':<8} {'Type':<30}\n")
        out.write("-" * 80 + "\n")

        for data in task_data:
            best_display = str(data['best_size']) if data['best_size'] != "-" else "-"
            private_display = str(data['private_size']) if data['private_size'] != "-" else "-"
            public_display = str(data['public_size']) if data['public_size'] != "-" else "-"
            wr_display = str(data['wr_score']) if data['wr_score'] != "-" else "-"
            deficit_display = str(data['deficit']) if data['deficit'] != "-" else "-"
            type_display = data['type'] if data['type'] else "unknown"

            out.write(f"Task {data['task_num']:<5} {best_display:<8} {private_display:<10} {public_display:<8} {wr_display:<6} {deficit_display:<8} {type_display:<30}\n")

if __name__ == "__main__":
    main()
    create_deficit_sorted_log()
    create_type_sorted_log()
    print("Created score_log.txt, score_log_deficit.txt, and score_log_type.txt")