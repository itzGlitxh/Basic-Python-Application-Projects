import tkinter as tk
from tkinter import messagebox, simpledialog
import json

SAVE_FILE_PATH = "notes_data.json"

class NoteManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Note Manager")
        self.root.geometry("400x540")
        self.root.configure(bg='white')

        self.note_folders = []
        self.selected_folder_index = None
        self.selected_note_index = None

        self.create_ui()
        self.load_data()

    def load_data(self):
        try:
            with open(SAVE_FILE_PATH, "r") as file:
                data = json.load(file)
                self.note_folders = data.get("note_folders", [])
                self.update_folder_list()
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {"note_folders": self.note_folders}
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(data, file)

    def add_folder(self):
        folder_name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder_name:
            self.note_folders.append({"name": folder_name, "notes": []})
            self.update_folder_list()
            self.save_data()

    def edit_folder(self):
        if self.selected_folder_index is not None:
            folder = self.note_folders[self.selected_folder_index]
            new_name = simpledialog.askstring("Edit Folder", "Edit folder name:", initialvalue=folder["name"])
            if new_name:
                folder["name"] = new_name
                self.update_folder_list()
                self.save_data()

    def delete_folder(self):
        if self.selected_folder_index is not None:
            del self.note_folders[self.selected_folder_index]
            self.selected_folder_index = None
            self.update_folder_list()
            self.save_data()

    def add_note_to_folder(self):
        if self.selected_folder_index is not None:
            folder = self.note_folders[self.selected_folder_index]
            note_text = self.note_entry.get("1.0", tk.END).strip()
            if note_text:
                folder["notes"].append(note_text)
                self.update_note_list(folder)
                self.clear_input_field()
                self.save_data()

    def remove_note_from_folder(self):
        if self.selected_folder_index is not None and self.selected_note_index is not None:
            folder = self.note_folders[self.selected_folder_index]
            if len(folder["notes"]) > self.selected_note_index:
                del folder["notes"][self.selected_note_index]
                self.selected_note_index = None
                self.update_note_list(folder)
                self.save_data()

    def clear_all_notes_from_folder(self):
        if self.selected_folder_index is not None:
            folder = self.note_folders[self.selected_folder_index]
            folder["notes"] = []
            self.update_note_list(folder)
            self.save_data()

    def update_folder_list(self):
        self.folder_listbox.delete(0, tk.END)
        for folder in self.note_folders:
            self.folder_listbox.insert(tk.END, folder["name"])

    def update_note_list(self, folder):
        self.note_listbox.delete(0, tk.END)
        for note in folder["notes"]:
            self.note_listbox.insert(tk.END, note)

    def clear_input_field(self):
        self.note_entry.delete("1.0", tk.END)

    def create_ui(self):
        self.title_label = tk.Label(self.root, text="Personal Note Manager", font=("Helvetica", 16, "bold"), bg='white')
        self.title_label.pack(pady=(10,0))

        self.folder_frame = tk.Frame(self.root, bg='white')
        self.folder_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.folder_label = tk.Label(self.folder_frame, text="Folders:", font=("Helvetica", 12), bg='white')
        self.folder_label.pack(anchor=tk.W)

        self.folder_listbox = tk.Listbox(self.folder_frame, font=("Helvetica", 12), width=30, height=5, bg='#EAEAEA')
        self.folder_listbox.pack(pady=5, fill=tk.BOTH, expand=True, side=tk.LEFT)

        folder_buttons_frame = tk.Frame(self.folder_frame, bg='white')
        folder_buttons_frame.pack(pady=5, padx=5, fill=tk.BOTH, side=tk.LEFT)

        add_folder_button = tk.Button(folder_buttons_frame, text="Add Folder", command=self.add_folder, bg='#2196F3', fg='black', font=("Helvetica", 11))
        add_folder_button.pack(pady=5, fill=tk.BOTH)

        edit_folder_button = tk.Button(folder_buttons_frame, text="Edit Folder", command=self.edit_folder, bg='#FFC107', fg='black', font=("Helvetica", 11))
        edit_folder_button.pack(pady=5, fill=tk.BOTH)

        delete_folder_button = tk.Button(folder_buttons_frame, text="Delete Folder", command=self.delete_folder, bg='#F44336', fg='black', font=("Helvetica", 11))
        delete_folder_button.pack(pady=5, fill=tk.BOTH)

        self.note_frame = tk.Frame(self.root, bg='white')
        self.note_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.note_label = tk.Label(self.note_frame, text="Enter Your Note:", font=("Helvetica", 12), bg='white')
        self.note_label.pack(anchor=tk.W)

        self.note_entry = tk.Text(self.note_frame, font=("Helvetica", 12), width=30, height=2, wrap=tk.WORD, bg='#EAEAEA')
        self.note_entry.pack(pady=5, fill=tk.BOTH, expand=True, side=tk.LEFT)

        note_buttons_frame = tk.Frame(self.note_frame, bg='white')
        note_buttons_frame.pack(pady=5, padx=5, fill=tk.BOTH, side=tk.LEFT)

        add_note_to_folder_button = tk.Button(note_buttons_frame, text="Add Note", command=self.add_note_to_folder, bg='#2196F3', fg='black', font=("Helvetica", 12))
        add_note_to_folder_button.pack(pady=5, fill=tk.BOTH)

        self.note_listbox = tk.Listbox(self.root, font=("Helvetica", 12), width=40, height=10, bg='#EAEAEA')
        self.note_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        remove_note_from_folder_button = tk.Button(self.root, text="Remove Note", command=self.remove_note_from_folder, bg='#F44336', fg='black', font=("Helvetica", 12))
        remove_note_from_folder_button.pack(pady=5, padx=(50,0), fill=tk.BOTH, side=tk.LEFT)

        clear_all_notes_from_folder_button = tk.Button(self.root, text="Clear All Notes", command=self.clear_all_notes_from_folder, bg='#FF5722', fg='black', font=("Helvetica", 12))
        clear_all_notes_from_folder_button.pack(pady=5, padx=(0,50), fill=tk.BOTH, side=tk.RIGHT)

        self.folder_listbox.bind('<<ListboxSelect>>', self.load_selected_folder)
        self.note_listbox.bind('<<ListboxSelect>>', self.load_selected_note)

    def load_selected_folder(self, event):
        selected_folder_index = self.folder_listbox.curselection()
        if selected_folder_index:
            index = selected_folder_index[0]
            folder = self.note_folders[index]
            self.selected_folder_index = index
            self.selected_note_index = None
            self.update_note_list(folder)
            
    def load_selected_note(self, event):
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            self.selected_note_index = selected_note_index[0]

if __name__ == "__main__":
    app = tk.Tk()
    note_manager = NoteManager(app)
    app.mainloop()
