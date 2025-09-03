import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from collections import defaultdict


class Contract:
    def __init__(self, name, course_type, student):
        self.name = name
        self.course_type = course_type
        self.student = student


class DrivingSchoolApp:
    def __init__(self, master):
        self.master = master
        self.contracts = []

        master.title("Курсы вождения - Договоры")
        master.geometry("900x700")

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.master)
        frame.pack(padx=10, pady=10)

        self.load_button = tk.Button(frame, text="Загрузить договоры", command=self.load_contracts)
        self.load_button.pack(pady=5, fill=tk.X)

        self.segment_by_course_button = tk.Button(
            frame, text="Сегментация по типам курсов", command=self.segment_by_course
        )
        self.segment_by_course_button.pack(pady=5, fill=tk.X)

        self.segment_by_student_button = tk.Button(
            frame, text="Сегментация по обучающимся", command=self.segment_by_student
        )
        self.segment_by_student_button.pack(pady=5, fill=tk.X)

        self.canvas = tk.Canvas(self.master, width=800, height=500, bg="white")
        self.canvas.pack(pady=20)

    def load_contracts(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV файлы", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                required_fields = {"name", "course_type", "student"}
                if set(reader.fieldnames) != required_fields:
                    raise ValueError(f"Неверные заголовки столбцов. Ожидались: {required_fields}")

                self.contracts.clear()
                for row in reader:
                    contract = Contract(row["name"], row["course_type"], row["student"])
                    self.contracts.append(contract)

                messagebox.showinfo("Успех", f"Загружено {len(self.contracts)} договоров.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def segment_by_course(self):
        if not self.contracts:
            messagebox.showwarning("Нет данных", "Сначала загрузите договоры.")
            return

        stats = defaultdict(int)
        for contract in self.contracts:
            stats[contract.course_type] += 1

        self.plot_pie_chart(stats, "Сегментация по типам курсов")

    def segment_by_student(self):
        if not self.contracts:
            messagebox.showwarning("Нет данных", "Сначала загрузите договоры.")
            return

        stats = defaultdict(int)
        for contract in self.contracts:
            stats[contract.student] += 1

        self.plot_pie_chart(stats, "Сегментация по обучающимся")

    def plot_pie_chart(self, data, title):
        self.canvas.delete("all")
        

        labels = list(data.keys())
        values = list(data.values())
        total = sum(values)
        cx, cy, radius = 300, 260, 200

        start_angle = 0

        # Подобранные приятные цвета
        colors = ["#66B2FF", "#5CD6D6", "#99FF99", "#FFD700", "#FFA07A", "#DDA0DD"]

        # Рисуем сектора
        for i, (label, value) in enumerate(zip(labels, values)):
            angle = (value / total) * 360
            end_angle = start_angle + angle

            # Рисуем сектор
            self.canvas.create_arc(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                start=start_angle, extent=angle,
                fill=colors[i % len(colors)], outline="black"
            )

            start_angle = end_angle

        # Легенда справа от графика
        legend_x = cx + radius + 20
        legend_y_start = cy - (len(labels) * 20) // 2

        for i, label in enumerate(labels):
            color = colors[i % len(colors)]
            # Квадратик цвета
            self.canvas.create_rectangle(legend_x, legend_y_start + i*25,
                                         legend_x + 15, legend_y_start + i*25 + 15,
                                         fill=color, outline="black")
            # Текст легенды
            self.canvas.create_text(legend_x + 20, legend_y_start + i*25 + 8,
                                    text=label, anchor="w", font=("Arial", 10), fill="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = DrivingSchoolApp(root)
    root.mainloop()

