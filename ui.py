import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta

from logic import add_task, delete_task, edit_task
from storage import save_tasks, load_tasks
from config import DEFAULT_DATE

class ToDoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo-приложение")
        self.root.geometry("500x600")

        self.tasks = []
        self.current_date = datetime.strptime(DEFAULT_DATE, "%Y-%m-%d")

        self.create_inputs()
        self.create_date_controls()
        self.create_task_controls()
        self.load_tasks()

    # 🔹 Ввод заголовка и заметки
    def create_inputs(self):
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "Заголовок задачи")

        self.note_text = tk.Text(self.root, width=50, height=3)
        self.note_text.pack(pady=5)
        self.note_text.insert(tk.END, "Текст заметки")

    # 🔹 Управление датой
    def create_date_controls(self):
        self.date_label = tk.Label(self.root, text=f"Дата: {self.current_date.strftime('%Y-%m-%d')}")
        self.date_label.pack()

        date_buttons = tk.Frame(self.root)
        tk.Button(date_buttons, text="←", width=5, command=self.decrease_date).pack(side=tk.LEFT)
        tk.Button(date_buttons, text="→", width=5, command=self.increase_date).pack(side=tk.LEFT)
        date_buttons.pack(pady=5)

        tk.Button(self.root, text="Добавить задачу", command=self.handle_add).pack(pady=5)

    # 🔹 Список задач и кнопки управления
    def create_task_controls(self):
        self.listbox = tk.Listbox(self.root, width=70, height=15)
        self.listbox.pack(pady=10)

        tk.Button(self.root, text="Удалить задачу", command=self.handle_delete).pack(pady=5)
        tk.Button(self.root, text="Редактировать задачу", command=self.handle_edit).pack(pady=5)
        tk.Button(self.root, text="Сохранить задачи", command=self.save_tasks).pack(pady=5)
        tk.Button(self.root, text="Загрузить задачи", command=self.load_tasks).pack(pady=5)

    # 🔹 Обновление даты
    def update_date_label(self):
        self.date_label.config(text=f"Дата: {self.current_date.strftime('%Y-%m-%d')}")

    def increase_date(self):
        self.current_date += timedelta(days=1)
        self.update_date_label()

    def decrease_date(self):
        self.current_date -= timedelta(days=1)
        self.update_date_label()

    # 🔹 Добавление задачи
    def handle_add(self):
        title = self.title_entry.get().strip()
        note = self.note_text.get("1.0", tk.END).strip()
        if not title:
            messagebox.showwarning("Пустой заголовок", "Введите заголовок задачи")
            return
        self.tasks = add_task(self.tasks, title, note, self.current_date.strftime("%Y-%m-%d"))
        self.listbox.insert(tk.END, f"{self.tasks[-1]['date']} — {title}")
        self.title_entry.delete(0, tk.END)
        self.note_text.delete("1.0", tk.END)

    # 🔹 Удаление задачи
    def handle_delete(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks = delete_task(self.tasks, index)
            self.listbox.delete(index)
        else:
            messagebox.showwarning("Нет выбора", "Выберите задачу для удаления")

    # 🔹 Редактирование задачи
    def handle_edit(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            current = self.tasks[index]
            new_title = simpledialog.askstring("Заголовок", "Измените заголовок:", initialvalue=current["title"])
            new_note = simpledialog.askstring("Заметка", "Измените текст заметки:", initialvalue=current["note"])
            if new_title:
                self.tasks = edit_task(self.tasks, index, new_title, new_note or "")
                self.listbox.delete(index)
                self.listbox.insert(index, f"{self.tasks[index]['date']} — {new_title}")
        else:
            messagebox.showwarning("Нет выбора", "Выберите задачу для редактирования")

    # 🔹 Сохранение и загрузка
    def save_tasks(self):
        save_tasks(self.tasks)
        messagebox.showinfo("Сохранено", "Задачи сохранены")

    def load_tasks(self):
        self.tasks = load_tasks()
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, f"{task['date']} — {task['title']}")