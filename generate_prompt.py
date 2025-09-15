# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os

class TaskAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Analysis Generator")
        self.root.geometry("800x600")

        self.color_names = {
            0: "black", 1: "blue", 2: "red", 3: "green", 4: "yellow",
            5: "gray", 6: "pink", 7: "orange", 8: "light blue", 9: "brown"
        }

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # Instructions label
        instructions_label = ttk.Label(main_frame, text="Enter a Task Number and a Description of the Transformation and click Generate Prompt", font=('Arial', 10))
        instructions_label.grid(row=0, column=0, pady=5)

        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Task Number (1-400):").grid(row=0, column=0, padx=5)
        self.task_entry = ttk.Entry(input_frame, width=10)
        self.task_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        self.task_entry.bind('<Return>', lambda e: self.analyze_task())


        # Manual description section
        desc_frame = ttk.LabelFrame(main_frame, text="Manual Description of Transformation", padding="10")
        desc_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        desc_frame.columnconfigure(0, weight=1)
        desc_frame.rowconfigure(0, weight=1)

        self.description_text = tk.Text(desc_frame, height=4, wrap=tk.WORD)
        self.description_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        desc_scroll = ttk.Scrollbar(desc_frame, orient="vertical", command=self.description_text.yview)
        desc_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.description_text.configure(yscrollcommand=desc_scroll.set)

        # Generate button section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=10)

        self.analyze_button = ttk.Button(button_frame, text="Generate Prompt", command=self.analyze_task)
        self.analyze_button.grid(row=0, column=0)

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.grid(row=4, column=0, pady=5)

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Generated Prompt", padding="10")
        results_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=80, height=30)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Copy button
        copy_frame = ttk.Frame(main_frame)
        copy_frame.grid(row=6, column=0, pady=5)

        self.copy_button = ttk.Button(copy_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_button.grid(row=0, column=0)

    def analyze_task(self):
        try:
            task_num = int(self.task_entry.get())

            if not (1 <= task_num <= 400):
                messagebox.showerror("Error", "Please enter a number between 1 and 400")
                return

            # Load task data
            file_path = os.path.join(os.path.dirname(__file__), 'Examples', f"task{task_num:03d}.json")
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File task{task_num:03d}.json not found")
                return

            self.status_label.config(text="Loading and analyzing task data...")
            self.root.update()

            with open(file_path, 'r') as f:
                task_data = json.load(f)

            # Analyze the data
            results = self.analyze_grids(task_data)

            # Display results
            self.display_results(task_num, results)
            self.copy_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Analysis complete for task {task_num}")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing task: {str(e)}")
            self.status_label.config(text="Error occurred during analysis")

    def analyze_grids(self, task_data):
        dimension_combinations = set()
        input_colors = set()
        output_colors = set()

        # Process all categories (train, test, arc-gen, etc.)
        for category_key, category_data in task_data.items():
            if isinstance(category_data, list):
                for example in category_data:
                    if isinstance(example, dict) and 'input' in example and 'output' in example:
                        input_grid = example['input']
                        output_grid = example['output']

                        if (isinstance(input_grid, list) and input_grid and
                            isinstance(output_grid, list) and output_grid):

                            # Get input dimensions
                            input_rows = len(input_grid)
                            input_cols = len(input_grid[0]) if input_grid[0] else 0

                            # Get output dimensions
                            output_rows = len(output_grid)
                            output_cols = len(output_grid[0]) if output_grid[0] else 0

                            # Store the combination
                            dimension_combinations.add(((input_rows, input_cols), (output_rows, output_cols)))

                            # Get input colors
                            for row in input_grid:
                                for cell in row:
                                    if isinstance(cell, int) and 0 <= cell <= 9:
                                        input_colors.add(cell)

                            # Get output colors
                            for row in output_grid:
                                for cell in row:
                                    if isinstance(cell, int) and 0 <= cell <= 9:
                                        output_colors.add(cell)

        return {
            'dimension_combinations': sorted(dimension_combinations),
            'input_colors': sorted(input_colors),
            'output_colors': sorted(output_colors)
        }

    def display_results(self, task_num, results):
        self.results_text.delete(1.0, tk.END)

        # Get manual description
        manual_description = self.description_text.get(1.0, tk.END).strip()
        if not manual_description:
            manual_description = "[PLEASE ENTER A MANUAL DESCRIPTION OF THE TRANSFORMATION]"

        # Format dimension combinations
        dim_combos = []
        for combo in results['dimension_combinations']:
            input_dim, output_dim = combo
            dim_combos.append(f"{input_dim[0]}x{input_dim[1]} -> {output_dim[0]}x{output_dim[1]}")
        dim_combo_str = ", ".join(dim_combos) if dim_combos else "[NO DIMENSION COMBINATIONS FOUND]"

        # Format input colors
        input_color_strs = []
        for color in results['input_colors']:
            input_color_strs.append(f"{color}={self.color_names[color]}")
        input_colors_str = ", ".join(input_color_strs) if input_color_strs else "[NO INPUT COLORS FOUND]"

        # Format output colors
        output_color_strs = []
        for color in results['output_colors']:
            output_color_strs.append(f"{color}={self.color_names[color]}")
        output_colors_str = ", ".join(output_color_strs) if output_color_strs else "[NO OUTPUT COLORS FOUND]"

        # Generate the prompt
        output = f"""I'm competing in a Python golf competition (where the goal is to write code that accomplishes a given task using the minimum number of characters).

Write Python code for me that takes as input a 2-dimensional grid (as a list of lists) and produces as output a 2-dimensional grid (as a list of lists or tuple of tuples) where the only possible input/output dimension combinations are:
{dim_combo_str}

The input grid's values are integers that each represent a color from the set {{ {input_colors_str} }}.
The output grid's values are integers that each represent a color from the set {{ {output_colors_str} }}.

The function should transform the input as follows: 
{manual_description}.

The code may transform the input in place or create a new list of lists or tuple of tuples, whichever can be done with the fewest characters.

The code should be contained in a function (or lambda function) named "p", with grid argument "g".

The code will never be expected to handle any grid sizes or colors/values other than those explicitly outlined here, so hardcoding such values is acceptable.

Run time and memory are not concerns. The only concern is minimal characters in the code.

Use only the standard Python library. Nothing may be imported.

Write this code to 'Work/task{task_num:03d}.py'."""

        self.results_text.insert(1.0, output)
        self.current_results = output

    def copy_to_clipboard(self):
        if hasattr(self, 'current_results'):
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_results)
            self.status_label.config(text="Results copied to clipboard!")

def main():
    root = tk.Tk()
    app = TaskAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()