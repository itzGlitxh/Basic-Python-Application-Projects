import tkinter as tk
from tkinter import messagebox
import json
import os

# Constants for button colors
BUTTON_ADD_COLOR = '#4CAF50'
BUTTON_DELETE_COLOR = '#F44336'
BUTTON_COMPLETE_COLOR = '#2196F3'
BUTTON_INCOMPLETE_COLOR = '#FFC107'

# File path for tasks data
TASKS_FILE_PATH = "tasks.json"

# Function to save tasks to a JSON file
def save_tasks():
    with open(TASKS_FILE_PATH, "w") as file:
        json.dump(tasks, file)

# Function to load tasks from the JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE_PATH):
        with open(TASKS_FILE_PATH, "r") as file:
            return json.load(file)
    return []

# Function to add a new task
def add_task():
    task_text = task_entry.get()
    due_date = due_date_entry.get()
    if task_text:
        tasks.append({"task": task_text, "due_date": due_date, "completed": False, "text_color": "black"})
        tasks.sort(key=lambda x: x.get("due_date", ""))
        clear_input_fields()
        update_task_list()
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# Function to clear input fields
def clear_input_fields():
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)

# Function to delete a selected task
def delete_task():
    selected_task_index = task_list.curselection()
    if selected_task_index:
        index = selected_task_index[0]
        task_list.delete(index)
        del tasks[index]
        save_tasks()

# Function to mark a task as completed or incomplete
def toggle_completed(completed):
    selected_task_index = task_list.curselection()
    if selected_task_index:
        index = selected_task_index[0]
        tasks[index]["completed"] = completed
        tasks[index]["text_color"] = "gray" if completed else "black"
        task_list.itemconfig(index, {'fg': tasks[index]["text_color"], 'selectbackground': 'royalblue'})
        save_tasks()

# Function to update the task list
def update_task_list():
    task_list.delete(0, tk.END)
    for task_data in tasks:
        formatted_task = task_data['task'] + task_data['due_date'].rjust(45 - len(task_data['task']), ' ')
        text_color = task_data.get("text_color", "black")
        task_list.insert(tk.END, formatted_task)
        task_list.itemconfig(tk.END, {'fg': text_color, 'selectbackground': 'royalblue'})

# Create the main application window
app = tk.Tk()
app.title("Personalized Task Manager")

# Load tasks from the JSON file
tasks = load_tasks()

# Create UI elements
app.geometry("372x468")
app.configure(bg='white')

title_label = tk.Label(app, text="Personal Task Manager", font=("Helvetica", 14, "bold"), bg='white', padx=10)
task_label = tk.Label(app, text="Task:", font=("Helvetica", 10), bg='white')
task_entry = tk.Entry(app, width=25, font=("Helvetica", 10))
due_date_label = tk.Label(app, text="Due Date (MM/DD/YYYY):", font=("Helvetica", 10), bg='white')
due_date_entry = tk.Entry(app, width=25, font=("Helvetica", 10))
add_button = tk.Button(app, text="Add Task", command=add_task, bg=BUTTON_ADD_COLOR, fg='black', font=("Helvetica", 10))
task_list = tk.Listbox(app, selectmode=tk.SINGLE, height=8, width=50, bg='#EAEAEA', selectbackground=BUTTON_ADD_COLOR, selectforeground='white', font=("Helvetica", 10))
delete_button = tk.Button(app, text="Delete Task", command=delete_task, bg=BUTTON_DELETE_COLOR, fg='black', font=("Helvetica", 10))
complete_button = tk.Button(app, text="Mark as Complete", command=lambda: toggle_completed(True), bg=BUTTON_COMPLETE_COLOR, fg='black', font=("Helvetica", 10))
incomplete_button = tk.Button(app, text="Mark as Incomplete", command=lambda: toggle_completed(False), bg=BUTTON_INCOMPLETE_COLOR, fg='black', font=("Helvetica", 10))

# Place UI elements in the window
title_label.pack(pady=5)
task_label.pack(pady=5)
task_entry.pack(pady=5)
due_date_label.pack(pady=5)
due_date_entry.pack(pady=5)
add_button.pack(pady=5)
task_list.pack(pady=5)
delete_button.pack(pady=5)
complete_button.pack(pady=5)
incomplete_button.pack(pady=2.5)

# Populate the task list with existing tasks
update_task_list()

app.mainloop()
