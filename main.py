import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

TASKS_FILE = "tasks.json"

class ToDoLayout(BoxLayout):
    tasks = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_tasks()

    def add_task(self, text):
        if text:
            self.tasks.append(text)
            self.ids.task_input.text = ""
            self.save_tasks()

    def remove_task(self, text):
        if text in self.tasks:
            self.tasks.remove(text)
            self.save_tasks()

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
        except:
            self.tasks = []

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)

class ToDoApp(App):
    def build(self):
        return ToDoLayout()

if __name__ == "__main__":
    ToDoApp().run()