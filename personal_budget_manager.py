import tkinter as tk
from tkinter import messagebox
import locale

def set_budget():
    global budget
    budget_input = budget_entry.get()
    if not budget_input:
        messagebox.showwarning("Missing Input", "Please enter a budget amount.")
        return

    try:
        budget = float(locale.atof(budget_input))
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid budget amount (numeric value).")
    else:
        update_budget_label()

def add_expense():
    expense_name = expense_name_entry.get()
    expense_amount = expense_amount_entry.get()
    
    if not (expense_name and expense_amount):
        messagebox.showwarning("Missing Input", "Please enter both the expense name and amount.")
        return

    try:
        expense_amount = float(locale.atof(expense_amount))
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid expense amount (numeric value).")
    else:
        expenses.append((expense_name, expense_amount))
        update_expense_list()
        update_budget_label()
        clear_input_fields()

def remove_expense():
    selected_expense_index = expense_listbox.curselection()
    if selected_expense_index:
        index = selected_expense_index[0]
        removed_expense = expenses.pop(index)
        update_expense_list()
        update_budget_label()

def update_expense_list():
    expense_listbox.delete(0, tk.END)
    for expense in expenses:
        formatted_amount = locale.format_string('%.2f', expense[1], grouping=True)
        expense_listbox.insert(tk.END, f"{expense[0]} (${formatted_amount})")

def update_budget_label():
    remaining_budget = budget - sum(expense[1] for expense in expenses)
    formatted_budget = locale.format_string('%.2f', remaining_budget, grouping=True)
    budget_label.config(text=f"Remaining Budget: ${formatted_budget}")

def clear_input_fields():
    expense_name_entry.delete(0, tk.END)
    expense_amount_entry.delete(0, tk.END)

app = tk.Tk()
app.title("Budget Manager")

budget = 0
expenses = []

locale.setlocale(locale.LC_ALL, '')

app.geometry("325x475")
app.configure(bg='white')

budget_label = tk.Label(app, text="Enter Your Budget:", font=("Helvetica", 12), bg='white')
budget_entry = tk.Entry(app, font=("Helvetica", 12), width=10)
set_budget_button = tk.Button(app, text="Set Budget", command=set_budget, bg='#4CAF50', fg='black', font=("Helvetica", 10))
expense_name_label = tk.Label(app, text="Expense Name:", font=("Helvetica", 10), bg='white')
expense_name_entry = tk.Entry(app, font=("Helvetica", 10), width=20)
expense_amount_label = tk.Label(app, text="Expense Amount ($):", font=("Helvetica", 10), bg='white')
expense_amount_entry = tk.Entry(app, font=("Helvetica", 10), width=10)
add_expense_button = tk.Button(app, text="Add Expense", command=add_expense, bg='#2196F3', fg='black', font=("Helvetica", 10))
expense_listbox = tk.Listbox(app, font=("Helvetica", 10), width=40, bg='#EAEAEA', selectbackground='#4CAF50', selectforeground='white')
remove_expense_button = tk.Button(app, text="Remove Expense", command=remove_expense, bg='#F44336', fg='black', font=("Helvetica", 10))

budget_label.pack(pady=10)
budget_entry.pack()
set_budget_button.pack(pady=10)
expense_name_label.pack()
expense_name_entry.pack()
expense_amount_label.pack()
expense_amount_entry.pack()
add_expense_button.pack(pady=10)
expense_listbox.pack()
remove_expense_button.pack(pady=10)

app.mainloop()
