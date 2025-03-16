import tkinter as tk
from tkinter import messagebox, font
import copy


class Sudoku:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.num_solutions = 0

    def verify_row(self, i):
        for j in range(9):
            if self.grid[i][j] != 0:
                for k in range(j + 1, 9):
                    if self.grid[i][j] == self.grid[i][k]:
                        return False
        return True

    def verify_column(self, j):
        for i in range(9):
            if self.grid[i][j] != 0:
                for k in range(i + 1, 9):
                    if self.grid[i][j] == self.grid[k][j]:
                        return False
        return True

    def verify_square(self, i, j):
        a, c = i // 3, j // 3
        for l in range(3):
            for m in range(3):
                if self.grid[3 * a + l][3 * c + m] != 0:
                    for n in range(3):
                        for o in range(3):
                            if (3 * a + l != 3 * a + n or 3 * c + o != 3 * c + m):
                                if self.grid[3 * a + l][3 * c + m] == self.grid[3 * a + n][3 * c + o]:
                                    return False
        return True

    def verify_possible(self, i, j, val):
        if i == 111 or j == 111:
            return False
        self.grid[i][j] = val
        result = self.verify_row(i) and self.verify_column(j) and self.verify_square(i, j)
        self.grid[i][j] = 0
        return result

    def grid_correct(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0 and not (
                        self.verify_row(i) and self.verify_column(j) and self.verify_square(i, j)):
                    return False
        return True

    def solve_grid(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return self._solve_grid(i, j)
        return False

    def _solve_grid(self, i, j):
        if (i > 8 or j > 8) and self.grid_correct():
            return True
        if i > 8 or j > 8:
            return False
        for val in range(1, 10):
            if self.verify_possible(i, j, val):
                self.grid[i][j] = val
                next_i, next_j = self.next_cell(i, j)
                if self._solve_grid(next_i, next_j):
                    return True
        self.grid[i][j] = 0
        return False

    def next_cell(self, i, j):
        for k in range(j + 1, 9):
            if self.grid[i][k] == 0:
                return (i, k)
        for l in range(i + 1, 9):
            for k in range(9):
                if self.grid[l][k] == 0:
                    return (l, k)
        return (111, 111)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Custom font
        self.cell_font = font.Font(family="Arial", size=12, weight="bold")
        self.label_font = font.Font(family="Arial", size=14, weight="bold")

        # Input grid
        self.input_cells = []
        self.create_grid(30, "Input Puzzle", self.input_cells, editable=True)

        # Result grid
        self.result_cells = []
        self.create_grid(350, "Solution", self.result_cells, editable=False)

        # Buttons
        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049",
                        "relief": "flat", "padx": 10, "pady": 5}
        submit_btn = tk.Button(root, text="Solve", command=self.solve, **button_style)
        submit_btn.place(x=200, y=650)

        clear_btn = tk.Button(root, text="Clear", command=self.clear, **button_style)
        clear_btn.place(x=300, y=650)

    def create_grid(self, y_offset, title, cell_list, editable=True):
        # Title label
        tk.Label(self.root, text=title, font=self.label_font, bg="#f0f0f0", fg="#333").place(x=220, y=y_offset)

        # Create canvas for background colors and grid lines
        canvas = tk.Canvas(self.root, width=300, height=300, bg="#ffffff", highlightthickness=0)
        canvas.place(x=150, y=y_offset + 30)

        # Add alternating background colors for 3x3 sub-grids
        for i in range(3):
            for j in range(3):
                color = "#e6f3ff" if (i + j) % 2 == 0 else "#ffffff"  # Light blue and white
                canvas.create_rectangle(i * 100, j * 100, (i + 1) * 100, (j + 1) * 100, fill=color, outline="")

        # Draw grid lines
        for i in range(0, 301, 33):
            canvas.create_line(i, 0, i, 300, fill="gray")
            canvas.create_line(0, i, 300, i, fill="gray")
        for i in range(0, 301, 100):
            canvas.create_line(i, 0, i, 300, fill="black", width=2)
            canvas.create_line(0, i, 300, i, fill="black", width=2)

        # Create entry widgets
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=self.cell_font, justify="center", relief="flat", bg="white",
                                 fg="#333")
                entry.place(x=153 + j * 33, y=y_offset + 33 + i * 33)
                if not editable:
                    entry.config(state="readonly", readonlybackground="white")
                row.append(entry)
            cell_list.append(row)

    def get_input_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.input_cells[i][j].get()
                row.append(int(val) if val.isdigit() and 0 <= int(val) <= 9 else 0)
            grid.append(row)
        return grid

    def display_result(self, grid):
        for i in range(9):
            for j in range(9):
                self.result_cells[i][j].config(state="normal")
                self.result_cells[i][j].delete(0, tk.END)
                self.result_cells[i][j].insert(0, str(grid[i][j]) if grid[i][j] != 0 else "")
                self.result_cells[i][j].config(state="readonly")

    def solve(self):
        try:
            input_grid = self.get_input_grid()
            sudoku = Sudoku(input_grid)
            original_grid = copy.deepcopy(sudoku.grid)

            if sudoku.solve_grid():
                self.display_result(sudoku.grid)
            else:
                sudoku.grid = original_grid
                if sudoku.grid_correct():
                    messagebox.showinfo("Result", "Puzzle is valid but has no additional solutions")
                else:
                    messagebox.showerror("Error", "No solution exists or input is invalid")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers (0-9)")

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.input_cells[i][j].delete(0, tk.END)
                self.result_cells[i][j].config(state="normal")
                self.result_cells[i][j].delete(0, tk.END)
                self.result_cells[i][j].config(state="readonly")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    app = SudokuGUI(root)
    root.mainloop()