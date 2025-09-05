import json
from datetime import datetime
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout

TASKS_FILE = "tasks.json"

class ToDoLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)

        # Красный фон
        with self.canvas.before:
            Color(1, 0.85, 0.85, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Выбор даты через Spinner
        self.day_spinner = Spinner(text="День", values=[str(i) for i in range(1, 32)], size_hint_y=None, height=40)
        self.month_spinner = Spinner(text="Месяц", values=[str(i).zfill(2) for i in range(1, 13)], size_hint_y=None, height=40)
        self.year_spinner = Spinner(text="Год", values=["2025", "2026", "2027"], size_hint_y=None, height=40)

        # Выбор времени через Spinner
        self.hour_spinner = Spinner(text="Часы", values=[str(i).zfill(2) for i in range(0, 24)], size_hint_y=None, height=40)
        self.minute_spinner = Spinner(text="Минуты", values=[str(i).zfill(2) for i in range(0, 60)], size_hint_y=None, height=40)

        # Добавляем спиннеры в интерфейс
        self.add_widget(self.day_spinner)
        self.add_widget(self.month_spinner)
        self.add_widget(self.year_spinner)
        self.add_widget(self.hour_spinner)
        self.add_widget(self.minute_spinner)

        # Кнопка добавления задачи
        self.add_widget(MDButton(
            MDButtonText(text="Добавить задачу"),
            style="elevated",
            on_release=self.confirm_task
        ))

        # Область отображения задач
        self.task_box = MDGridLayout(cols=1, spacing=10, size_hint_y=None)
        self.task_box.bind(minimum_height=self.task_box.setter("height"))
        scroll = MDScrollView()
        scroll.add_widget(self.task_box)
        self.add_widget(scroll)

        # Загрузка задач
        self.tasks = []
        self.load_tasks()
        self.refresh_tasks()

        # Проверка задач каждую минуту
        Clock.schedule_interval(self.check_tasks, 60)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def confirm_task(self, instance):
        # Проверка, что все поля заполнены
        if "День" in self.day_spinner.text or "Месяц" in self.month_spinner.text or \
           "Год" in self.year_spinner.text or "Часы" in self.hour_spinner.text or \
           "Минуты" in self.minute_spinner.text:
            self.show_popup("Выберите дату и время задачи")
            return

        try:
            dt = datetime(
                year=int(self.year_spinner.text),
                month=int(self.month_spinner.text),
                day=int(self.day_spinner.text),
                hour=int(self.hour_spinner.text),
                minute=int(self.minute_spinner.text)
            )
        except ValueError:
            self.show_popup("Неверная дата или время")
            return

        task = {
            "text": f"Задача на {dt.strftime('%Y-%m-%d %H:%M')}",
            "date": dt.strftime("%Y-%m-%d %H:%M"),
            "done": False,
            "notified": False
        }
        self.tasks.append(task)

        # Сброс выбора
        self.day_spinner.text = "День"
        self.month_spinner.text = "Месяц"
        self.year_spinner.text = "Год"
        self.hour_spinner.text = "Часы"
        self.minute_spinner.text = "Минуты"

        self.save_tasks()
        self.refresh_tasks()

    def toggle_done(self, checkbox, task):
        task["done"] = checkbox.active
        self.save_tasks()
        self.refresh_tasks()

    def remove_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()
        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_box.clear_widgets()
        for task in self.tasks:
            item = MDBoxLayout(size_hint_y=None, height=40, spacing=10)

            checkbox = MDCheckbox(active=task["done"])
            checkbox.bind(active=lambda cb, val, t=task: self.toggle_done(cb, t))
            item.add_widget(checkbox)

            label = MDLabel(
                text=task["text"],
                theme_text_color="Hint" if task["done"] else "Primary"
            )
            item.add_widget(label)

            btn = MDButton(
                MDButtonText(text="Удалить"),
                style="outlined",
                on_release=lambda x, t=task: self.remove_task(t)
            )
            item.add_widget(btn)

            self.task_box.add_widget(item)

    def check_tasks(self, dt):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        for task in self.tasks:
            if not task["done"] and not task.get("notified") and task["date"] == now:
                self.show_popup(f'Время задачи: {task["text"]}')
                task["notified"] = True
                self.save_tasks()

    def show_popup(self, message):
        popup = Popup(title="Напоминание", content=MDLabel(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except:
            self.tasks = []

    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

class ToDoApp(MDApp):
    def build(self):
        return ToDoLayout()

if __name__ == "__main__":
    ToDoApp().run()