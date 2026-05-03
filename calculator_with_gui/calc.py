import tkinter as tk
import math

# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("Neon Calculator")
window.geometry("420x600")
window.configure(bg="#0f172a")

expression = ""

# ---------------- DISPLAY ----------------
display = tk.Entry(
    window,
    font=("Helvetica", 26),
    bg="#020617",
    fg="#8cff00",
    insertbackground="white",
    borderwidth=0,
    justify="right"
)
display.pack(fill="both", padx=15, pady=15, ipady=15)


# ---------------- HISTORY ----------------
history = tk.Text(
    window,
    height=5,
    bg="#020617",
    fg="#00ff77",
    font=("Helvetica",10),
    borderwidth=0
)
history.pack(fill="both", padx=15, pady=5)


# ---------------- FUNCTIONS ----------------
def press(value):
    global expression
    expression += str(value)
    display.delete(0, tk.END)
    display.insert(0, expression)

def equal():
    global expression
    try:
        result = str(eval(expression))
        history.insert(tk.END, expression + " = " + result + "\n")

        display.delete(0, tk.END)
        display.insert(0, result)

        expression = result
    except:
        display.delete(0, tk.END)
        display.insert(0, "Error")
        expression = ""

def clear():
    global expression
    expression = ""
    display.delete(0, tk.END)


# ---------------- SCIENTIFIC ----------------
def log_func():
    value = float(display.get())
    display.delete(0, tk.END)
    display.insert(0, math.log10(value))

def antilog():
    value = float(display.get())
    display.delete(0, tk.END)
    display.insert(0, 10**value)

def sqrt():
    value = float(display.get())
    display.delete(0, tk.END)
    display.insert(0, math.sqrt(value))


# ---------------- BUTTON HOVER ANIMATION ----------------
def on_enter(e):
    e.widget['bg'] = "#04cef2"

def on_leave(e):
    e.widget['bg'] = "#1e293b"


# ---------------- BUTTON GRID ----------------
frame = tk.Frame(window, bg="#0f172a")
frame.pack()

buttons = [
    ('7',1,0),('8',1,1),('9',1,2),('/',1,3),
    ('4',2,0),('5',2,1),('6',2,2),('*',2,3),
    ('1',3,0),('2',3,1),('3',3,2),('-',3,3),
    ('0',4,0),('.',4,1),('=',4,2),('+',4,3)
]

for (text,row,col) in buttons:

    if text == "=":
        cmd = equal
    else:
        cmd = lambda x=text: press(x)

    btn = tk.Button(
        frame,
        text=text,
        command=cmd,
        width=6,
        height=3,
        font=("Helvetica",16),
        bg="#000000",
        fg="white",
        borderwidth=0,
        activebackground="#06b6d4"
    )

    btn.grid(row=row,column=col,padx=6,pady=6)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


# CLEAR
clear_btn = tk.Button(
    frame,
    text="C",
    command=clear,
    width=14,
    height=2,
    font=("Helvetica",14),
    bg="#ef4444",
    fg="white",
    borderwidth=0
)
clear_btn.grid(row=5,column=0,columnspan=2,padx=6,pady=6)


# ---------------- SCIENTIFIC PANEL ----------------
advanced = tk.Frame(window, bg="#0f172a")

def toggle_scientific():
    if advanced.winfo_ismapped():
        advanced.pack_forget()
    else:
        advanced.pack(pady=10)

tk.Button(
    window,
    text="Scientific Mode",
    command=toggle_scientific,
    bg="#22c55e",
    fg="black",
    borderwidth=0,
    font=("Helvetica",12)
).pack(pady=8)


tk.Button(advanced,text="log",command=log_func,width=8).grid(row=0,column=0,padx=5,pady=5)
tk.Button(advanced,text="antilog",command=antilog,width=8).grid(row=0,column=1,padx=5,pady=5)
tk.Button(advanced,text="√",command=sqrt,width=8).grid(row=0,column=2,padx=5,pady=5)


# ---------------- KEYBOARD SUPPORT ----------------
def key_input(event):
    key = event.char

    if key in "0123456789+-*/.":
        press(key)

    elif event.keysym == "Return":
        equal()

    elif event.keysym == "BackSpace":
        display.delete(len(display.get())-1, tk.END)

    elif event.keysym == "Escape":
        clear()


window.bind("<Key>", key_input)


# ---------------- RUN ----------------
window.mainloop()
