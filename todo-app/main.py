import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------------- SETTINGS ----------------
APP_NAME = "Armaan's To-Do App"
DATA_FILE = "tasks.json"

themes = {
    "Dark": {
        "bg": "#121212",
        "fg": "#ffffff",
        "entry_bg": "#1f1f1f",
        "entry_fg": "#ffffff",
        "button_bg": "#2a2a2a",
        "button_fg": "#ffffff",
        "special_bg": "#00c853",
        "special_fg": "#ffffff"
    },
    "Light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "entry_bg": "#e0e0e0",
        "entry_fg": "#000000",
        "button_bg": "#d6d6d6",
        "button_fg": "#000000",
        "special_bg": "#4caf50",
        "special_fg": "#ffffff"
    },
    "Neon": {
        "bg": "#000000",
        "fg": "#39ff14",
        "entry_bg": "#111111",
        "entry_fg": "#39ff14",
        "button_bg": "#222222",
        "button_fg": "#39ff14",
        "special_bg": "#ff00ff",
        "special_fg": "#ffffff"
    }
}

current_theme = "Dark"

# ---------------- FILE FUNCTIONS ----------------
def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

tasks_data = load_tasks()

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("To-Do App")
root.geometry("550x520")
root.resizable(False, False)

# ---------------- UI FUNCTIONS ----------------
def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    t = themes[theme_name]

    root.configure(bg=t["bg"])
    title_label.configure(bg=t["bg"], fg=t["fg"])

    task_entry.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["fg"])

    task_listbox.configure(bg=t["entry_bg"], fg=t["fg"])

    theme_menu.configure(bg=t["button_bg"], fg=t["fg"], activebackground=t["button_bg"], activeforeground=t["fg"])

    add_btn.configure(bg=t["special_bg"], fg=t["special_fg"])
    delete_btn.configure(bg=t["button_bg"], fg=t["button_fg"])
    clear_btn.configure(bg=t["button_bg"], fg=t["button_fg"])
    mark_btn.configure(bg=t["button_bg"], fg=t["button_fg"])

def refresh_listbox():
    task_listbox.delete(0, tk.END)
    for task in tasks_data:
        task_listbox.insert(tk.END, task)

def add_task():
    task = task_entry.get().strip()
    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return

    tasks_data.append(task)
    save_tasks(tasks_data)
    refresh_listbox()
    task_entry.delete(0, tk.END)

def delete_task():
    try:
        selected = task_listbox.curselection()[0]
        tasks_data.pop(selected)
        save_tasks(tasks_data)
        refresh_listbox()
    except:
        messagebox.showwarning("Warning", "Select a task to delete!")

def clear_all():
    confirm = messagebox.askyesno("Confirm", "Delete all tasks?")
    if confirm:
        tasks_data.clear()
        save_tasks(tasks_data)
        refresh_listbox()

def mark_done():
    try:
        selected = task_listbox.curselection()[0]
        task = tasks_data[selected]

        if "✅" not in task:
            tasks_data[selected] = "✅ " + task

        save_tasks(tasks_data)
        refresh_listbox()
    except:
        messagebox.showwarning("Warning", "Select a task to mark done!")

# ---------------- TITLE ----------------
title_label = tk.Label(root, text=APP_NAME, font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# ---------------- INPUT ----------------
task_entry = tk.Entry(root, font=("Arial", 16))
task_entry.pack(fill="x", padx=20, pady=10, ipady=8)

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

add_btn = tk.Button(btn_frame, text="Add Task", font=("Arial", 12), width=12, command=add_task)
add_btn.grid(row=0, column=0, padx=5)

mark_btn = tk.Button(btn_frame, text="Mark Done", font=("Arial", 12), width=12, command=mark_done)
mark_btn.grid(row=0, column=1, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Task", font=("Arial", 12), width=12, command=delete_task)
delete_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(btn_frame, text="Clear All", font=("Arial", 12), width=12, command=clear_all)
clear_btn.grid(row=0, column=3, padx=5)

# ---------------- TASK LIST ----------------
task_listbox = tk.Listbox(root, font=("Arial", 14), height=15)
task_listbox.pack(fill="both", padx=20, pady=10)

# ---------------- THEME SELECTOR ----------------
theme_var = tk.StringVar(value=current_theme)

theme_label = tk.Label(root, text="Theme:", font=("Arial", 12))
theme_label.pack()

theme_menu = tk.OptionMenu(root, theme_var, *themes.keys(), command=apply_theme)
theme_menu.pack(pady=5)

# Load tasks on startup
refresh_listbox()

# Apply default theme
apply_theme("Dark")

# Start app
root.mainloop()
