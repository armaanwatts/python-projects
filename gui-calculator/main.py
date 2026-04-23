import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------------- SETTINGS ----------------
APP_NAME = "Armaan's Calculator"
HISTORY_FILE = "history.json"

themes = {
    "Dark": {
        "bg": "#121212",
        "fg": "#ffffff",
        "button_bg": "#1f1f1f",
        "button_fg": "#ffffff",
        "special_bg": "#ff4444",
        "special_fg": "#ffffff",
        "equal_bg": "#00c853",
        "equal_fg": "#ffffff"
    },
    "Light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "button_bg": "#e0e0e0",
        "button_fg": "#000000",
        "special_bg": "#ff5252",
        "special_fg": "#ffffff",
        "equal_bg": "#4caf50",
        "equal_fg": "#ffffff"
    },
    "Neon": {
        "bg": "#000000",
        "fg": "#39ff14",
        "button_bg": "#111111",
        "button_fg": "#39ff14",
        "special_bg": "#ff00ff",
        "special_fg": "#ffffff",
        "equal_bg": "#00ffff",
        "equal_fg": "#000000"
    }
}

current_theme = "Dark"
expression = ""

# ---------------- HISTORY FUNCTIONS ----------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

history_data = load_history()

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("520x520")
root.resizable(False, False)

# ---------------- UI FUNCTIONS ----------------
def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    t = themes[theme_name]

    root.configure(bg=t["bg"])
    title_label.configure(bg=t["bg"], fg=t["fg"])
    display.configure(bg=t["button_bg"], fg=t["fg"], insertbackground=t["fg"])

    history_label.configure(bg=t["bg"], fg=t["fg"])
    history_listbox.configure(bg=t["button_bg"], fg=t["fg"])

    theme_menu.configure(bg=t["button_bg"], fg=t["fg"], activebackground=t["button_bg"], activeforeground=t["fg"])

    for btn in all_buttons:
        if btn["text"] == "=":
            btn.configure(bg=t["equal_bg"], fg=t["equal_fg"])
        elif btn["text"] in ["C", "⌫"]:
            btn.configure(bg=t["special_bg"], fg=t["special_fg"])
        else:
            btn.configure(bg=t["button_bg"], fg=t["button_fg"])

def press(key):
    global expression
    expression += str(key)
    display_var.set(expression)

def clear():
    global expression
    expression = ""
    display_var.set("")

def backspace():
    global expression
    expression = expression[:-1]
    display_var.set(expression)

def calculate():
    global expression, history_data
    try:
        result = str(eval(expression))
        entry = f"{expression} = {result}"
        history_listbox.insert(tk.END, entry)

        history_data.append(entry)
        save_history(history_data)

        expression = result
        display_var.set(result)

    except:
        messagebox.showerror("Error", "Invalid Calculation")
        expression = ""
        display_var.set("")

# ---------------- TITLE ----------------
title_label = tk.Label(root, text=APP_NAME, font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# ---------------- DISPLAY ----------------
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Arial", 22), justify="right", bd=5)
display.pack(fill="x", padx=10, pady=10, ipady=10)

# ---------------- MAIN FRAME ----------------
main_frame = tk.Frame(root)
main_frame.pack()

# ---------------- BUTTON FRAME ----------------
btn_frame = tk.Frame(main_frame)
btn_frame.grid(row=0, column=0, padx=10)

buttons = [
    ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
    ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
    ("0", 3, 0), (".", 3, 1), ("+", 3, 2), ("=", 3, 3),
    ("C", 4, 0), ("⌫", 4, 1)
]

all_buttons = []

for (text, row, col) in buttons:
    if text == "=":
        btn = tk.Button(btn_frame, text=text, width=6, height=2, font=("Arial", 16), command=calculate)
    elif text == "C":
        btn = tk.Button(btn_frame, text=text, width=6, height=2, font=("Arial", 16), command=clear)
    elif text == "⌫":
        btn = tk.Button(btn_frame, text=text, width=6, height=2, font=("Arial", 16), command=backspace)
    else:
        btn = tk.Button(btn_frame, text=text, width=6, height=2, font=("Arial", 16),
                        command=lambda t=text: press(t))

    btn.grid(row=row, column=col, padx=5, pady=5)
    all_buttons.append(btn)

# ---------------- HISTORY FRAME ----------------
history_frame = tk.Frame(main_frame)
history_frame.grid(row=0, column=1, padx=10)

history_label = tk.Label(history_frame, text="History", font=("Arial", 14, "bold"))
history_label.pack(pady=5)

history_listbox = tk.Listbox(history_frame, width=25, height=15, font=("Arial", 10))
history_listbox.pack()

# Load old history
for item in history_data:
    history_listbox.insert(tk.END, item)

# ---------------- THEME SELECTOR ----------------
theme_label = tk.Label(root, text="Select Theme:", font=("Arial", 12))
theme_label.pack(pady=5)

theme_var = tk.StringVar(value=current_theme)
theme_menu = tk.OptionMenu(root, theme_var, *themes.keys(), command=apply_theme)
theme_menu.pack(pady=5)

# Apply default theme
apply_theme("Dark")

# ---------------- START ----------------
root.mainloop()
