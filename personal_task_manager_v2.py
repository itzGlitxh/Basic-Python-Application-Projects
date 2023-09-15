import tkinter as tk
from tkinter import messagebox
import json
import os
from tkcalendar import Calendar
from datetime import datetime

TASKS_FILE_PATH = "tasks.json"

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personalized Task Manager")
        self.root.geometry("400x540")
        self.root.configure(bg='white')

        self.selected_due_date = ""
        self.tasks = []

        self.load_tasks()
        self.create_ui()
        self.update_task_list()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE_PATH):
            with open(TASKS_FILE_PATH, "r") as file:
                self.tasks = json.load(file)

    def save_tasks(self):
        with open(TASKS_FILE_PATH, "w") as file:
            json.dump(self.tasks, file)

    def on_date_select(self, event):
        selected_date = self.due_date_calendar.get_date()
        if selected_date:
            try:
                selected_date = datetime.strptime(selected_date, "%m/%d/%y")
                self.selected_due_date = selected_date.strftime("%m/%d/%Y")
            except ValueError:
                pass  # Ignore invalid date selections

    def add_task(self):
        task_text = self.task_var.get()

        if not self.selected_due_date:
            selected_date = self.due_date_calendar.get_date()
            if selected_date:
                try:
                    selected_date = datetime.strptime(selected_date, "%m/%d/%y")
                    self.selected_due_date = selected_date.strftime("%m/%d/%Y")
                except ValueError:
                    return

        try:
            due_date = datetime.strptime(self.selected_due_date, "%m/%d/%Y").date()
        except ValueError:
            return

        if task_text:
            task = {
                "task": task_text,
                "due_date": due_date.strftime("%m/%d/%Y"),
                "completed": False,
                "text_color": "black"
            }
            self.tasks.append(task)
            self.tasks.sort(key=lambda x: x.get("due_date", ""))
            self.clear_input_fields()
            self.update_task_list()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def clear_input_fields(self):
        self.task_var.set("")
        self.selected_due_date = ""

    def delete_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            del self.tasks[index]
            self.save_tasks()
            self.update_task_list()

    def toggle_completed(self, completed):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            index = selected_task_index[0]
            self.tasks[index]["completed"] = completed
            self.tasks[index]["text_color"] = "gray" if completed else "black"
            self.update_task_list()
            self.save_tasks()

    def clear_all_tasks(self):
        self.tasks = []
        self.save_tasks()
        self.update_task_list()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task_data in self.tasks:
            formatted_task = f"{task_data['due_date']}: {task_data['task']}"
            text_color = task_data.get("text_color", "black")
            self.task_list.insert(tk.END, formatted_task)
            self.task_list.itemconfig(tk.END, {'fg': text_color, 'selectbackground': 'royalblue'})

    def create_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        label_spacing = 5

        self.title_label = tk.Label(self.root, text="Personal Task Manager [v2]", font=("Helvetica", 18, "bold"), bg='white')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        self.task_label = tk.Label(self.root, text="Task:", font=("Helvetica", 12), bg='white')
        self.task_label.grid(row=1, column=0, pady=label_spacing, padx=10, sticky="e")

        self.task_var = tk.StringVar()
        self.task_entry = tk.Entry(self.root, width=27, font=("Helvetica", 12), bg='white', textvariable=self.task_var)
        self.task_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        self.due_date_label = tk.Label(self.root, text="Due Date:", font=("Helvetica", 12), bg='white')
        self.due_date_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")

        current_time = datetime.now()
        self.due_date_calendar = Calendar(self.root, selectmode="day", year=current_time.year, month=current_time.month, day=current_time.day)
        self.due_date_calendar.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        self.due_date_calendar.bind("<<CalendarSelected>>", self.on_date_select)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task, bg='#4CAF50', fg='black', font=("Helvetica", 12))
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="we")

        self.task_list = tk.Listbox(self.root, selectmode=tk.SINGLE, height=8, width=50, bg='#EAEAEA', selectbackground='#4CAF50', selectforeground='white', font=("Helvetica", 12))
        self.task_list.grid(row=4, column=0, columnspan=2, pady=5, padx=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task, bg='#F44336', fg='black', font=("Helvetica", 12))
        self.delete_button.grid(row=5, column=0, pady=5, padx=10, sticky="w")

        self.clear_all_button = tk.Button(self.root, text="Clear All Tasks", command=self.clear_all_tasks, bg='#FF5722', fg='black', font=("Helvetica", 12))
        self.clear_all_button.grid(row=5, column=1, pady=5, padx=10, sticky="e")

        self.complete_button = tk.Button(self.root, text="Mark as Complete", command=lambda: self.toggle_completed(True), bg='#2196F3', fg='black', font=("Helvetica", 12))
        self.complete_button.grid(row=6, column=0, pady=3, padx=10, sticky="w", columnspan=2)

        self.incomplete_button = tk.Button(self.root, text="Mark as Incomplete", command=lambda: self.toggle_completed(False), bg='#FFC107', fg='black', font=("Helvetica", 12))
        self.incomplete_button.grid(row=6, column=0, columnspan=2, pady=3, padx=10, sticky="e")

if __name__ == "__main__":
    app = tk.Tk()
    task_manager = TaskManager(app)
    app.mainloop()
