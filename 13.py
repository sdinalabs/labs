import tkinter as tk
from tkinter import filedialog, messagebox
def read_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(x) for x in line.strip().split()]
            matrix.append(row)
    return matrix
def find_path(matrix, start, end):
    rows, cols = len(matrix), len(matrix[0])
    visited = [[False for z in range(cols)] for z in range(rows)]
    path = []
    def dfs(x, y):
        if x < 0 or x >= rows or y < 0 or y >= cols:
            return False
        if matrix[x][y] == 1 or visited[x][y]:
            return False
        if (x, y) == end:
            path.append((x, y))
            return True
        visited[x][y] = True
        path.append((x, y))
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            if dfs(x + dx, y + dy):
                return True
        path.pop()
        return False
    if dfs(start[0], start[1]):
        return path
    return None
def visualize_labyrinth(matrix, path, start, end):
    visualization_window = tk.Toplevel()
    visualization_window.title("Лабиринт - решение")
    
    cell_size = 30
    canvas_width = len(matrix[0]) * cell_size
    canvas_height = len(matrix) * cell_size
    
    canvas = tk.Canvas(visualization_window, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack(padx=10, pady=10)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            
            if matrix[i][j] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='gray')
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='gray')
    if path:
        for idx, (i, j) in enumerate(path):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if (i, j) == start:
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='green', outline='green')
            elif (i, j) == end:
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='red', outline='red')
            else:
                canvas.create_oval(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill='blue', outline='blue')
            if idx > 0:
                prev_i, prev_j = path[idx - 1]
                center_x1 = prev_j * cell_size + cell_size // 2
                center_y1 = prev_i * cell_size + cell_size // 2
                center_x2 = j * cell_size + cell_size // 2
                center_y2 = i * cell_size + cell_size // 2
                canvas.create_line(center_x1, center_y1, center_x2, center_y2, 
                                 fill='blue', width=2)
    info_text = f"Длина пути: {len(path)} шагов" if path else "Путь не найден"
    info_label = tk.Label(visualization_window, text=info_text, font=("Arial", 12))
    info_label.pack(pady=5)
def select_file():
    filename = filedialog.askopenfilename(
        title="Выберите файл с лабиринтом",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if filename:
        file_label.config(text=f"Выбран файл: {filename.split('/')[-1]}")
        solve_labyrinth(filename)
def solve_labyrinth(filename):
    try:
        matrix = read_matrix(filename)
        if len(matrix) != 15 or any(len(row) != 15 for row in matrix):
            messagebox.showerror("Ошибка", "Матрица должна быть размером 15x15")
            return
        start = (0, 0)
        if matrix[start[0]][start[1]] == 1:
            messagebox.showerror("Ошибка", "Стартовая позиция заблокирована")
            return
        end = (14, 14)
        if matrix[end[0]][end[1]] == 1:
            messagebox.showerror("Ошибка", "Конечная позиция заблокирована")
            return
        path = find_path(matrix, start, end)
        if path:
            messagebox.showinfo("Успех", f"Путь найден! Длина пути: {len(path)} шагов")
            visualize_labyrinth(matrix, path, start, end)
        else:
            messagebox.showinfo("Результат", "Путь не найден!")
            visualize_labyrinth(matrix, [], start, end)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл не найден")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
def create_main_window():
    global file_label
    root = tk.Tk()
    root.title("Решатель лабиринтов")
    root.geometry("400x200")
    
    title_label = tk.Label(root, text="Решатель лабиринтов", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    desc_label = tk.Label(root, text="Выберите файл с матрицей лабиринта 15x15", font=("Arial", 10))
    desc_label.pack(pady=5)
    
    select_button = tk.Button(root, text="Выбрать файл", command=select_file, 
                             font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
    select_button.pack(pady=10)
    
    file_label = tk.Label(root, text="Файл не выбран", font=("Arial", 9), fg="gray")
    file_label.pack(pady=5)
    
    exit_button = tk.Button(root, text="Выход", command=root.quit, 
                           font=("Arial", 10), bg="#f44336", fg="white", padx=15, pady=5)
    exit_button.pack(pady=10) 
    return root
def main():
    root = create_main_window()
    root.mainloop()
if __name__ == "__main__":
    main()

