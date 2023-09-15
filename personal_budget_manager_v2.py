import tkinter as tk
from tkinter import messagebox
import json

SAVE_FILE_PATH = "budget_data.json"

class BudgetManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Manager [v2]")
        self.root.geometry("400x540")
        self.root.configure(bg='white')

        self.budget = 0
        self.expenses = []

        self.load_data()
        self.create_ui()

    def load_data(self):
        try:
            with open(SAVE_FILE_PATH, "r") as file:
                data = json.load(file)
                self.budget = data.get("budget", 0)
                self.expenses = data.get("expenses", [])
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {"budget": self.budget, "expenses": self.expenses}
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(data, file)

    def set_budget(self):
        budget_input = self.budget_entry.get()
        if not budget_input:
            messagebox.showwarning("Missing Input", "Please enter a budget amount.")
            return

        try:
            self.budget = float(budget_input)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid budget amount (numeric value).")
        else:
            self.update_budget_label()
            self.save_data()
            self.budget_entry.delete(0, tk.END)

    def add_expense(self):
        expense_name = self.expense_name_entry.get()
        expense_amount = self.expense_amount_entry.get()

        if not (expense_name and expense_amount):
            messagebox.showwarning("Missing Input", "Please enter both the expense name and amount.")
            return

        try:
            expense_amount = float(expense_amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid expense amount (numeric value).")
        else:
            self.expenses.append((expense_name, expense_amount))
            self.update_expense_list()
            self.update_budget_label()
            self.clear_input_fields()
            self.save_data()

    def remove_expense(self):
        selected_expense_index = self.expense_listbox.curselection()
        if selected_expense_index:
            index = selected_expense_index[0]
            removed_expense = self.expenses.pop(index)
            self.update_expense_list()
            self.update_budget_label()
            self.save_data()

    def clear_all_expenses(self):
        self.expenses = []
        self.update_expense_list()
        self.update_budget_label()
        self.save_data()

    def update_expense_list(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"{expense[0]} (${expense[1]:.2f})")

    def update_budget_label(self):
        remaining_budget = self.budget - sum(expense[1] for expense in self.expenses)
        self.budget_label.config(text=f"Remaining Budget: ${remaining_budget:.2f}")

    def clear_input_fields(self):
        self.expense_name_entry.delete(0, tk.END)
        self.expense_amount_entry.delete(0, tk.END)

    def create_ui(self):
        self.budget_label = tk.Label(self.root, text="Enter Your Budget:", font=("Helvetica", 12), bg='white')
        self.budget_label.pack(pady=5)

        self.budget_entry = tk.Entry(self.root, font=("Helvetica", 12), width=12, bg='#EAEAEA')
        self.budget_entry.pack(pady=5)

        set_budget_button = tk.Button(self.root, text="Set Budget", command=self.set_budget, bg='#4CAF50', fg='black', font=("Helvetica", 12))
        set_budget_button.pack(pady=5)

        expense_name_label = tk.Label(self.root, text="Expense Name:", font=("Helvetica", 12), bg='white')
        expense_name_label.pack(pady=5)

        self.expense_name_entry = tk.Entry(self.root, font=("Helvetica", 12), width=20, bg='#EAEAEA')
        self.expense_name_entry.pack(pady=5)

        expense_amount_label = tk.Label(self.root, text="Expense Amount ($):", font=("Helvetica", 12), bg='white')
        expense_amount_label.pack(pady=5)

        self.expense_amount_entry = tk.Entry(self.root, font=("Helvetica", 12), width=10, bg='#EAEAEA')
        self.expense_amount_entry.pack(pady=5)
        
        add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense, bg='#2196F3', fg='black', font=("Helvetica", 12))
        add_expense_button.pack(pady=5)

        self.expense_listbox = tk.Listbox(self.root, font=("Helvetica", 12), width=40, bg='#EAEAEA')
        self.expense_listbox.pack(pady=5)

        remove_expense_button = tk.Button(self.root, text="Remove Expense", command=self.remove_expense, bg='#F44336', fg='black', font=("Helvetica", 12))
        remove_expense_button.pack(side=tk.LEFT, padx=(35, 0))

        clear_all_expenses_button = tk.Button(self.root, text="Clear All Expenses", command=self.clear_all_expenses, bg='#FF5722', fg='black', font=("Helvetica", 12))
        clear_all_expenses_button.pack(side=tk.RIGHT, pady=5, padx=(0, 35))

        self.update_expense_list()
        self.update_budget_label()

if __name__ == "__main__":
    app = tk.Tk()
    budget_manager = BudgetManager(app)
    app.mainloop()
