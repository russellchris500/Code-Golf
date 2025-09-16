# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'Examples', 'code_golf_utils'))
from code_golf_utils import colors, task_zero

class CodeGolfViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Golf Example Viewer")
        self.root.geometry("1200x800")
        
        self.current_example = None
        self.current_pair_index = 0
        self.example_data = None
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(control_frame, text="Example Number:").grid(row=0, column=0, padx=5)
        self.example_entry = ttk.Entry(control_frame, width=10)
        self.example_entry.grid(row=0, column=1, padx=5)
        self.example_entry.bind('<Return>', lambda e: self.load_example())
        
        self.view_button = ttk.Button(control_frame, text="View", command=self.load_example)
        self.view_button.grid(row=0, column=2, padx=5)
        
        ttk.Label(control_frame, text="(Enter 0 for built-in example or 1-400 for task examples)").grid(
            row=0, column=3, padx=20)
        
        nav_frame = ttk.Frame(main_frame)
        nav_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.prev_button = ttk.Button(nav_frame, text="< Previous", command=self.prev_pair, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=0, padx=5)
        
        self.pair_label = ttk.Label(nav_frame, text="No example loaded", font=('Arial', 10, 'bold'))
        self.pair_label.grid(row=0, column=1, padx=20)
        
        self.next_button = ttk.Button(nav_frame, text="Next >", command=self.next_pair, state=tk.DISABLED)
        self.next_button.grid(row=0, column=2, padx=5)
        
        self.category_label = ttk.Label(nav_frame, text="", font=('Arial', 9))
        self.category_label.grid(row=0, column=3, padx=20)
        
        grid_container = ttk.Frame(main_frame)
        grid_container.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        grid_container.columnconfigure(0, weight=1)
        grid_container.columnconfigure(1, weight=1)
        grid_container.rowconfigure(0, weight=1)
        
        input_frame = ttk.LabelFrame(grid_container, text="Input", padding="10")
        input_frame.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_canvas = tk.Canvas(input_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.input_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        output_frame = ttk.LabelFrame(grid_container, text="Output", padding="10")
        output_frame.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_canvas = tk.Canvas(output_frame, bg='white', highlightthickness=1, highlightbackground='gray')
        self.output_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        legend_frame = ttk.Frame(main_frame)
        legend_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Label(legend_frame, text="Color Legend:", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=5)
        
        for idx, color in enumerate(colors):
            color_frame = tk.Frame(legend_frame, width=20, height=20, 
                                  bg=f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}',
                                  highlightthickness=1, highlightbackground='black')
            color_frame.grid(row=0, column=idx+1, padx=2)
            ttk.Label(legend_frame, text=str(idx)).grid(row=1, column=idx+1)
    
    def load_example(self):
        try:
            example_num = int(self.example_entry.get())
            
            if example_num == 0:
                self.example_data = task_zero
            elif 1 <= example_num <= 400:
                file_path = os.path.join(os.path.dirname(__file__), 'Examples', f"task{example_num:03d}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        self.example_data = json.load(f)
                else:
                    messagebox.showerror("Error", f"File task{example_num:03d}.json not found")
                    return
            else:
                messagebox.showerror("Error", "Please enter a number between 0 and 400")
                return
            
            self.current_pair_index = 0
            self.current_example = example_num
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
        
        self.draw_grid(self.input_canvas, pair_data['input'])
        self.draw_grid(self.output_canvas, pair_data['output'])
        
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
            canvas_width = 400
            canvas_height = 400
        
        margin = 20
        available_width = canvas_width - 2 * margin
        available_height = canvas_height - 2 * margin
        
        if rows > 0 and cols > 0:
            cell_size = min(available_width // cols, available_height // rows, 40)
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
    app = CodeGolfViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()