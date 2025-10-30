import zipfile
import os
from pathlib import Path

def create_solutions_zip():
    solutions_dir = Path("Best-Updated-2")
    zip_path = "submission.zip"
    
    if not solutions_dir.exists():
        print(f"Error: {solutions_dir} directory not found")
        return
    
    task_files = sorted(solutions_dir.glob("task*.py"))
    
    if not task_files:
        print("No task*.py files found in solutions folder")
        return
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in task_files:
            # Add file with just its name (no directory structure)
            arcname = file_path.name
            zipf.write(file_path, arcname)
            print(f"Added: {arcname}")
    
    print(f"\nCreated submission.zip with {len(task_files)} files")

if __name__ == "__main__":
    create_solutions_zip()