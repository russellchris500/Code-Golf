# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import importlib.util
import copy

sys.path.append(os.path.join(os.path.dirname(__file__), 'Examples', 'code_golf_utils'))
from code_golf_utils import colors

class CodeGolfTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Golf Solution Tester")
        self.root.geometry("1600x800")
        
        self.current_example = None
        self.current_pair_index = 0
        self.example_data = None
        self.solution_function = None
        self.all_test_results = {}  # Store results for all examples
        self.overall_tested = False  # Track if we've tested all examples

        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=3, pady=10)
        
        ttk.Label(control_frame, text="Task Number:").grid(row=0, column=0, padx=5)
        self.example_entry = ttk.Entry(control_frame, width=10)
        self.example_entry.grid(row=0, column=1, padx=5)
        self.example_entry.bind('<Return>', lambda e: self.load_example())

        ttk.Label(control_frame, text="Folder:").grid(row=0, column=2, padx=(20, 5))
        self.folder_var = tk.StringVar(value="Work")
        self.folder_combo = ttk.Combobox(control_frame, textvariable=self.folder_var, values=["Work", "Solutions"], width=10, state="readonly")
        self.folder_combo.grid(row=0, column=3, padx=5)

        self.test_button = ttk.Button(control_frame, text="Load & Test", command=self.load_example)
        self.test_button.grid(row=0, column=4, padx=5)

        self.test_all_button = ttk.Button(control_frame, text="Test All", command=self.run_test_all)
        self.test_all_button.grid(row=0, column=6, padx=5)

        ttk.Label(control_frame, text="(Enter 1-400 for task examples)").grid(
            row=0, column=7, padx=20)
        
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.prev_button = ttk.Button(nav_frame, text="< Previous", command=self.prev_pair, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=0, padx=5)
        
        self.pair_label = ttk.Label(nav_frame, text="No example loaded", font=('Arial', 10, 'bold'))
        self.pair_label.grid(row=0, column=1, padx=20)
        
        self.next_button = ttk.Button(nav_frame, text="Next >", command=self.next_pair, state=tk.DISABLED)
        self.next_button.grid(row=0, column=2, padx=5)
        
        self.category_label = ttk.Label(nav_frame, text="", font=('Arial', 9))
        self.category_label.grid(row=0, column=3, padx=20)
        
        self.status_label = ttk.Label(nav_frame, text="", font=('Arial', 12, 'bold'))
        self.status_label.grid(row=0, column=4, padx=20)

        self.overall_status_label = ttk.Label(nav_frame, text="", font=('Arial', 12, 'bold'))
        self.overall_status_label.grid(row=1, column=1, columnspan=3, padx=20, pady=5)
        
        grid_container = ttk.Frame(main_frame)
        grid_container.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        grid_container.columnconfigure(0, weight=1)
        grid_container.columnconfigure(1, weight=1)
        grid_container.columnconfigure(2, weight=1)
        grid_container.rowconfigure(0, weight=1)
        
        input_frame = ttk.LabelFrame(grid_container, text="Input", padding="10")
        input_frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_canvas = tk.Canvas(input_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.input_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        expected_frame = ttk.LabelFrame(grid_container, text="Expected Output", padding="10")
        expected_frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        expected_frame.columnconfigure(0, weight=1)
        expected_frame.rowconfigure(0, weight=1)
        
        self.expected_canvas = tk.Canvas(expected_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.expected_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        actual_frame = ttk.LabelFrame(grid_container, text="Test Output", padding="10")
        actual_frame.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        actual_frame.columnconfigure(0, weight=1)
        actual_frame.rowconfigure(0, weight=1)
        
        self.actual_canvas = tk.Canvas(actual_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.actual_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        legend_frame = ttk.Frame(main_frame)
        legend_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Label(legend_frame, text="Color Legend:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        
        for idx, color in enumerate(colors):
            color_frame = tk.Frame(legend_frame, width=20, height=20, 
                                  bg=f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}',
                                  highlightthickness=1, highlightbackground='black')
            color_frame.grid(row=0, column=idx+1, padx=2)
            ttk.Label(legend_frame, text=str(idx)).grid(row=1, column=idx+1)
    
    def load_solution(self, task_num):
        """Load the solution function from the selected folder"""
        folder = self.folder_var.get()
        solution_path = os.path.join(os.path.dirname(__file__), folder, f'task{task_num:03d}.py')

        if not os.path.exists(solution_path):
            messagebox.showerror("Error", f"Solution file task{task_num:03d}.py not found in {folder} folder")
            return False
        
        try:
            spec = importlib.util.spec_from_file_location(f"task{task_num:03d}", solution_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'p'):
                self.solution_function = module.p
                return True
            else:
                messagebox.showerror("Error", f"Solution file task{task_num:03d}.py does not contain function 'p'")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading solution: {str(e)}")
            return False
    
    def load_example(self):
        try:
            example_num = int(self.example_entry.get())
            
            if not (1 <= example_num <= 400):
                messagebox.showerror("Error", "Please enter a number between 1 and 400")
                return
            
            # Load solution
            if not self.load_solution(example_num):
                return
            
            # Load task data
            file_path = os.path.join(os.path.dirname(__file__), 'Examples', f"task{example_num:03d}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    self.example_data = json.load(f)
            else:
                messagebox.showerror("Error", f"File task{example_num:03d}.json not found")
                return
            
            self.current_pair_index = 0
            self.current_example = example_num
            self.overall_tested = False  # Reset overall test status

            self.update_display()
            
            self.prev_button.config(state=tk.NORMAL if self.current_pair_index > 0 else tk.DISABLED)
            total_pairs = len(self.example_data.get('train', [])) + \
                         len(self.example_data.get('test', [])) + \
                         len(self.example_data.get('arc-gen', []))
            self.next_button.config(state=tk.NORMAL if self.current_pair_index < total_pairs - 1 else tk.DISABLED)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading example: {str(e)}")
    
    def get_current_pair(self):
        if not self.example_data:
            return None, None
        
        train_count = len(self.example_data.get('train', []))
        test_count = len(self.example_data.get('test', []))
        arc_gen_count = len(self.example_data.get('arc-gen', []))
        
        if self.current_pair_index < train_count:
            category = "train"
            index = self.current_pair_index
            data = self.example_data['train'][index]
        elif self.current_pair_index < train_count + test_count:
            category = "test"
            index = self.current_pair_index - train_count
            data = self.example_data['test'][index]
        elif self.current_pair_index < train_count + test_count + arc_gen_count:
            category = "arc-gen"
            index = self.current_pair_index - train_count - test_count
            data = self.example_data['arc-gen'][index]
        else:
            return None, None
        
        return data, category
    
    def test_solution(self, input_grid, expected_output):
        """Test the solution function and return the result"""
        if not self.solution_function:
            return None, "No solution loaded"

        try:
            # Create a deep copy of input to avoid modifying original
            input_copy = copy.deepcopy(input_grid)
            result = self.solution_function(input_copy)

            # Convert result to list format if it's not already
            if isinstance(result, tuple):
                result = [list(row) if isinstance(row, tuple) else row for row in result]
            elif isinstance(result, list):
                # Also convert any tuple rows within a list result
                result = [list(row) if isinstance(row, tuple) else row for row in result]
            else:
                return None, f"Invalid output type: {type(result)}"

            # Check if result matches expected output
            if result == expected_output:
                return result, "PASS"
            else:
                return result, "FAIL"
                
        except Exception as e:
            return None, f"Error: {str(e)}"

    def test_all_examples(self):
        """Test the solution against all examples and store results"""
        if not self.example_data or not self.solution_function:
            return

        self.all_test_results = {}

        # Test all categories
        for category in ['train', 'test', 'arc-gen']:
            if category in self.example_data:
                self.all_test_results[category] = []
                for example in self.example_data[category]:
                    _, status = self.test_solution(example['input'], example['output'])
                    self.all_test_results[category].append(status == "PASS")

    def run_test_all(self):
        """Run test_all_examples and update display"""
        if not self.example_data or not self.solution_function:
            messagebox.showerror("Error", "Please load a task first")
            return

        self.test_all_button.config(text="Testing...", state=tk.DISABLED)
        self.root.update()

        try:
            self.test_all_examples()
            self.overall_tested = True
            self.update_display()
        finally:
            self.test_all_button.config(text="Test All", state=tk.NORMAL)

    def get_overall_status(self):
        """Get overall pass/fail status across all examples"""
        if not self.overall_tested:
            return "Click 'Test All' to check all examples"

        if not self.all_test_results:
            return "No tests run"

        total_passed = 0
        total_tests = 0

        for category, results in self.all_test_results.items():
            total_passed += sum(results)
            total_tests += len(results)

        if total_tests == 0:
            return "No tests found"

        if total_passed == total_tests:
            return "PASSED ALL EXAMPLES"
        else:
            return f"FAILED TO PASS ALL EXAMPLES ({total_passed}/{total_tests} passed)"
    
    def update_display(self):
        pair_data, category = self.get_current_pair()
        
        if not pair_data:
            return
        
        train_count = len(self.example_data.get('train', []))
        test_count = len(self.example_data.get('test', []))
        arc_gen_count = len(self.example_data.get('arc-gen', []))
        total_pairs = train_count + test_count + arc_gen_count
        
        self.pair_label.config(text=f"Pair {self.current_pair_index + 1} of {total_pairs}")
        
        category_index = self.current_pair_index
        if category == "train":
            category_text = f"Train Example {category_index + 1}/{train_count}"
        elif category == "test":
            category_index -= train_count
            category_text = f"Test Example {category_index + 1}/{test_count}"
        else:
            category_index -= (train_count + test_count)
            category_text = f"ARC-GEN Example {category_index + 1}/{arc_gen_count}"
        
        self.category_label.config(text=f"Category: {category_text}")
        
        # Test the solution
        test_result, status = self.test_solution(pair_data['input'], pair_data['output'])

        # Update individual example status display
        if status == "PASS":
            self.status_label.config(text="PASSED THIS EXAMPLE", foreground="green")
        elif status == "FAIL":
            self.status_label.config(text="FAILED THIS EXAMPLE", foreground="red")
        else:
            self.status_label.config(text=f"ERROR: {status}", foreground="red")

        # Update overall status display
        overall_status = self.get_overall_status()
        if "PASSED ALL EXAMPLES" in overall_status:
            self.overall_status_label.config(text=overall_status, foreground="green")
        elif "FAILED TO PASS ALL EXAMPLES" in overall_status:
            self.overall_status_label.config(text=overall_status, foreground="red")
        elif "Click 'Test All'" in overall_status:
            self.overall_status_label.config(text=overall_status, foreground="blue")
        else:
            self.overall_status_label.config(text=overall_status, foreground="black")
        
        # Draw grids
        self.draw_grid(self.input_canvas, pair_data['input'])
        self.draw_grid(self.expected_canvas, pair_data['output'])
        
        if test_result is not None:
            self.draw_grid(self.actual_canvas, test_result)
        else:
            self.actual_canvas.delete("all")
            self.actual_canvas.create_text(
                self.actual_canvas.winfo_width()//2, 
                self.actual_canvas.winfo_height()//2,
                text="Error occurred", fill="red", font=('Arial', 12, 'bold')
            )
        
        self.prev_button.config(state=tk.NORMAL if self.current_pair_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_pair_index < total_pairs - 1 else tk.DISABLED)
    
    def draw_grid(self, canvas, grid):
        canvas.delete("all")

        if not grid:
            return

        # Convert tuple to list if necessary
        if isinstance(grid, tuple):
            grid = list(grid)

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        
        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 300
            canvas_height = 400
        
        margin = 20
        available_width = canvas_width - 2 * margin
        available_height = canvas_height - 2 * margin
        
        if rows > 0 and cols > 0:
            cell_size = min(available_width // cols, available_height // rows, 30)
        else:
            cell_size = 20
        
        grid_width = cols * cell_size
        grid_height = rows * cell_size
        
        offset_x = (canvas_width - grid_width) // 2
        offset_y = (canvas_height - grid_height) // 2
        
        for row_idx, row in enumerate(grid):
            # Convert row tuple to list if necessary
            if isinstance(row, tuple):
                row = list(row)
            for col_idx, value in enumerate(row):
                x1 = offset_x + col_idx * cell_size
                y1 = offset_y + row_idx * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                color = colors[value] if 0 <= value < len(colors) else (200, 200, 200)
                hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
                
                canvas.create_rectangle(x1, y1, x2, y2, 
                                       fill=hex_color, 
                                       outline='#808080',
                                       width=1)
    
    def prev_pair(self):
        if self.current_pair_index > 0:
            self.current_pair_index -= 1
            self.update_display()
    
    def next_pair(self):
        if self.example_data:
            total_pairs = len(self.example_data.get('train', [])) + \
                         len(self.example_data.get('test', [])) + \
                         len(self.example_data.get('arc-gen', []))
            if self.current_pair_index < total_pairs - 1:
                self.current_pair_index += 1
                self.update_display()

def main():
    root = tk.Tk()
    app = CodeGolfTester(root)
    root.mainloop()

if __name__ == "__main__":
    main()