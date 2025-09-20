# -*- coding: utf-8 -*-
"""
GUI Debug tool to view failing test cases for Code Golf tasks.
Based on test.py but focused only on failures for easier debugging.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import importlib.util
import copy

sys.path.append(os.path.join(os.path.dirname(__file__), 'Examples', 'code_golf_utils'))
from code_golf_utils import colors

class FailureDebugger:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Golf Failure Debugger")
        self.root.geometry("1800x900")

        self.current_failure_index = 0
        self.failures = []
        self.solution_function = None

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Label(control_frame, text="Task Number:").grid(row=0, column=0, padx=5)
        self.task_entry = ttk.Entry(control_frame, width=10)
        self.task_entry.grid(row=0, column=1, padx=5)
        self.task_entry.bind('<Return>', lambda e: self.find_failures())

        ttk.Label(control_frame, text="Folder:").grid(row=0, column=2, padx=(20, 5))
        self.folder_var = tk.StringVar(value="Work")
        self.folder_combo = ttk.Combobox(control_frame, textvariable=self.folder_var,
                                        values=["Work", "Solutions"], width=10, state="readonly")
        self.folder_combo.grid(row=0, column=3, padx=5)

        self.debug_button = ttk.Button(control_frame, text="Find Failures", command=self.find_failures)
        self.debug_button.grid(row=0, column=4, padx=5)

        # Results summary frame
        summary_frame = ttk.Frame(main_frame)
        summary_frame.grid(row=1, column=0, columnspan=4, pady=10)

        self.summary_label = ttk.Label(summary_frame, text="Load a task to see failure summary",
                                      font=('Arial', 12, 'bold'))
        self.summary_label.grid(row=0, column=0, padx=20)

        # Navigation frame
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.prev_button = ttk.Button(nav_frame, text="< Previous Failure",
                                     command=self.prev_failure, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.failure_label = ttk.Label(nav_frame, text="No failures loaded", font=('Arial', 10, 'bold'))
        self.failure_label.grid(row=0, column=1, padx=20)

        self.next_button = ttk.Button(nav_frame, text="Next Failure >",
                                     command=self.next_failure, state=tk.DISABLED)
        self.next_button.grid(row=0, column=2, padx=5)

        self.status_label = ttk.Label(nav_frame, text="", font=('Arial', 10))
        self.status_label.grid(row=0, column=3, padx=20)

        # Grid container
        grid_container = ttk.Frame(main_frame)
        grid_container.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        grid_container.columnconfigure(0, weight=1)
        grid_container.columnconfigure(1, weight=1)
        grid_container.columnconfigure(2, weight=1)
        grid_container.rowconfigure(0, weight=1)

        # Input frame
        input_frame = ttk.LabelFrame(grid_container, text="Input", padding="10")
        input_frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        self.input_canvas = tk.Canvas(input_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.input_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Expected frame
        expected_frame = ttk.LabelFrame(grid_container, text="Expected Output", padding="10")
        expected_frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        expected_frame.columnconfigure(0, weight=1)
        expected_frame.rowconfigure(0, weight=1)

        self.expected_canvas = tk.Canvas(expected_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.expected_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Actual frame
        actual_frame = ttk.LabelFrame(grid_container, text="Actual Output", padding="10")
        actual_frame.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        actual_frame.columnconfigure(0, weight=1)
        actual_frame.rowconfigure(0, weight=1)

        self.actual_canvas = tk.Canvas(actual_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.actual_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Differences frame
        diff_frame = ttk.LabelFrame(main_frame, text="Differences Analysis", padding="10")
        diff_frame.grid(row=4, column=0, columnspan=4, pady=10, sticky=(tk.W, tk.E))
        diff_frame.columnconfigure(0, weight=1)

        self.diff_text = tk.Text(diff_frame, height=6, width=100, font=('Courier', 9))
        diff_scrollbar = ttk.Scrollbar(diff_frame, orient="vertical", command=self.diff_text.yview)
        self.diff_text.configure(yscrollcommand=diff_scrollbar.set)

        self.diff_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        diff_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Color legend
        legend_frame = ttk.Frame(main_frame)
        legend_frame.grid(row=5, column=0, columnspan=4, pady=10)

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

    def test_solution(self, input_grid, expected_output):
        """Test the solution function and return the result"""
        if not self.solution_function:
            return None, "No solution loaded"

        try:
            input_copy = copy.deepcopy(input_grid)
            result = self.solution_function(input_copy)

            if isinstance(result, tuple):
                result = [list(row) if isinstance(row, tuple) else row for row in result]
            elif isinstance(result, list):
                result = [list(row) if isinstance(row, tuple) else row for row in result]
            else:
                return None, f"Invalid output type: {type(result)}"

            if result == expected_output:
                return result, "PASS"
            else:
                return result, "FAIL"

        except Exception as e:
            return None, f"Error: {str(e)}"

    def find_failures(self):
        try:
            task_num = int(self.task_entry.get())

            if not (1 <= task_num <= 400):
                messagebox.showerror("Error", "Please enter a number between 1 and 400")
                return

            # Load solution
            if not self.load_solution(task_num):
                return

            # Load task data
            file_path = os.path.join(os.path.dirname(__file__), 'Examples', f"task{task_num:03d}.json")
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File task{task_num:03d}.json not found")
                return

            with open(file_path, 'r') as f:
                example_data = json.load(f)

            # Find all failures
            self.failures = []
            total_tests = 0

            for category in ['train', 'test', 'arc-gen']:
                if category not in example_data:
                    continue

                for i, example in enumerate(example_data[category]):
                    total_tests += 1
                    result, status = self.test_solution(example['input'], example['output'])

                    if status != "PASS":
                        self.failures.append({
                            'category': category,
                            'index': i,
                            'input': example['input'],
                            'expected': example['output'],
                            'actual': result,
                            'status': status
                        })

            # Update summary
            failure_count = len(self.failures)
            success_rate = ((total_tests - failure_count) / total_tests * 100) if total_tests > 0 else 0

            if failure_count == 0:
                self.summary_label.config(text=f"🎉 All {total_tests} tests passed!", foreground="green")
                self.failure_label.config(text="No failures found")
                self.prev_button.config(state=tk.DISABLED)
                self.next_button.config(state=tk.DISABLED)
                self.status_label.config(text="")
                self.clear_displays()
            else:
                self.summary_label.config(text=f"Found {failure_count} failures out of {total_tests} tests ({success_rate:.1f}% success)",
                                        foreground="red")
                self.current_failure_index = 0
                self.update_failure_display()
                self.prev_button.config(state=tk.NORMAL)
                self.next_button.config(state=tk.NORMAL if failure_count > 1 else tk.DISABLED)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Error finding failures: {str(e)}")

    def update_failure_display(self):
        if not self.failures:
            return

        failure = self.failures[self.current_failure_index]

        # Update labels
        self.failure_label.config(text=f"Failure {self.current_failure_index + 1} of {len(self.failures)}")
        self.status_label.config(text=f"{failure['category']} example {failure['index'] + 1}: {failure['status']}")

        # Draw grids
        self.draw_grid(self.input_canvas, failure['input'], "Input")
        self.draw_grid(self.expected_canvas, failure['expected'], "Expected")

        if failure['actual'] is not None:
            self.draw_grid(self.actual_canvas, failure['actual'], "Actual")
        else:
            self.clear_canvas(self.actual_canvas, "Error occurred")

        # Update differences analysis
        self.update_differences_analysis(failure)

        # Update navigation buttons
        self.prev_button.config(state=tk.NORMAL if self.current_failure_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_failure_index < len(self.failures) - 1 else tk.DISABLED)

    def update_differences_analysis(self, failure):
        self.diff_text.delete(1.0, tk.END)

        expected = failure['expected']
        actual = failure['actual']

        if actual is None:
            self.diff_text.insert(tk.END, f"Error: {failure['status']}\n")
            return

        # Size comparison
        exp_size = (len(expected), len(expected[0]) if expected else 0)
        act_size = (len(actual), len(actual[0]) if actual else 0)

        self.diff_text.insert(tk.END, f"Size comparison:\n")
        self.diff_text.insert(tk.END, f"  Expected: {exp_size[0]}x{exp_size[1]}\n")
        self.diff_text.insert(tk.END, f"  Actual:   {act_size[0]}x{act_size[1]}\n")

        if exp_size != act_size:
            self.diff_text.insert(tk.END, f"  ⚠️ SIZE MISMATCH!\n\n")
        else:
            self.diff_text.insert(tk.END, f"  ✓ Sizes match\n\n")

        # Cell-by-cell differences
        if exp_size == act_size and expected and actual:
            self.diff_text.insert(tk.END, f"Cell differences:\n")
            diff_count = 0
            for r in range(len(expected)):
                for c in range(len(expected[0])):
                    if expected[r][c] != actual[r][c]:
                        self.diff_text.insert(tk.END, f"  ({r},{c}): expected {expected[r][c]}, got {actual[r][c]}\n")
                        diff_count += 1
                        if diff_count >= 20:  # Limit output
                            self.diff_text.insert(tk.END, f"  ... and more differences\n")
                            break
                if diff_count >= 20:
                    break

            if diff_count == 0:
                self.diff_text.insert(tk.END, f"  (No differences found - this shouldn't happen!)\n")
            else:
                self.diff_text.insert(tk.END, f"\nTotal differences: {diff_count}\n")

    def draw_grid(self, canvas, grid, title):
        canvas.delete("all")

        if not grid:
            canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,
                             text="(empty grid)", fill="gray", font=('Arial', 12))
            return

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        canvas.update()
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 400
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

        # Add size label
        canvas.create_text(canvas_width//2, 10, text=f"{title} ({rows}x{cols})",
                          fill="black", font=('Arial', 10, 'bold'))

        for row_idx, row in enumerate(grid):
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

    def clear_canvas(self, canvas, message):
        canvas.delete("all")
        canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,
                          text=message, fill="red", font=('Arial', 12, 'bold'))

    def clear_displays(self):
        for canvas in [self.input_canvas, self.expected_canvas, self.actual_canvas]:
            canvas.delete("all")
        self.diff_text.delete(1.0, tk.END)

    def prev_failure(self):
        if self.current_failure_index > 0:
            self.current_failure_index -= 1
            self.update_failure_display()

    def next_failure(self):
        if self.current_failure_index < len(self.failures) - 1:
            self.current_failure_index += 1
            self.update_failure_display()

def main():
    root = tk.Tk()
    app = FailureDebugger(root)
    root.mainloop()

if __name__ == "__main__":
    main()