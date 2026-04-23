import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

SETTINGS_FILE = "settings.json"
INVOICE_DATA_FILE = "invoices.json"

# ---------------- SETTINGS FUNCTIONS ----------------
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {
        "store_name": "Your Store",
        "store_address": "Your Address",
        "store_phone": "0000000000",
        "store_location": "Your City",
        "logo_path": ""
    }

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

# ---------------- INVOICE STORAGE ----------------
def load_invoices():
    if os.path.exists(INVOICE_DATA_FILE):
        try:
            with open(INVOICE_DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_invoice_record(record):
    invoices = load_invoices()
    invoices.append(record)
    with open(INVOICE_DATA_FILE, "w") as f:
        json.dump(invoices, f, indent=4)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Invoice Maker")
root.geometry("900x600")
root.configure(bg="white")
root.resizable(False, False)

# ---------------- VARIABLES ----------------
invoice_no_var = tk.StringVar(value=f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}")
date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))

customer_name_var = tk.StringVar()
customer_phone_var = tk.StringVar()

gst_var = tk.StringVar(value="0")
discount_var = tk.StringVar(value="0")

paid_via_var = tk.StringVar(value="Cash")

# Items list
items = []

# ---------------- FUNCTIONS ----------------
def add_item():
    name = item_name_var.get().strip()
    qty = item_qty_var.get().strip()
    price = item_price_var.get().strip()

    if name == "" or qty == "" or price == "":
        messagebox.showwarning("Warning", "Fill item name, quantity and price.")
        return

    try:
        qty = int(qty)
        price = float(price)
    except:
        messagebox.showerror("Error", "Quantity must be integer and price must be number.")
        return

    total = qty * price
    items.append({"name": name, "qty": qty, "price": price, "total": total})

    item_listbox.insert(tk.END, f"{name} | Qty: {qty} | Price: {price} | Total: {total}")

    item_name_var.set("")
    item_qty_var.set("")
    item_price_var.set("")

    update_total()

def delete_item():
    try:
        index = item_listbox.curselection()[0]
        item_listbox.delete(index)
        items.pop(index)
        update_total()
    except:
        messagebox.showwarning("Warning", "Select an item to delete.")

def update_total():
    subtotal = sum(item["total"] for item in items)

    try:
        gst = float(gst_var.get())
    except:
        gst = 0

    try:
        discount = float(discount_var.get())
    except:
        discount = 0

    gst_amount = (subtotal * gst) / 100
    grand_total = subtotal + gst_amount - discount

    subtotal_var.set(f"{subtotal:.2f}")
    gst_amount_var.set(f"{gst_amount:.2f}")
    grand_total_var.set(f"{grand_total:.2f}")

def generate_pdf():
    if customer_name_var.get().strip() == "":
        messagebox.showerror("Error", "Customer name is required.")
        return

    if len(items) == 0:
        messagebox.showerror("Error", "Add at least 1 item.")
        return

    invoice_no = invoice_no_var.get()
    filename = f"{invoice_no}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50

    # Store Info
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, settings["store_name"])
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, settings["store_address"])
    y -= 15
    c.drawString(50, y, f"Phone: {settings['store_phone']} | Location: {settings['store_location']}")
    y -= 30

    # Invoice Info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Invoice No: {invoice_no}")
    c.drawString(350, y, f"Date: {date_var.get()}")
    y -= 20

    # Customer Info
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Customer Name: {customer_name_var.get()}")
    y -= 15
    c.drawString(50, y, f"Customer Phone: {customer_phone_var.get()}")
    y -= 30

    # Table Header
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(320, y, "Price")
    c.drawString(420, y, "Total")
    y -= 15

    c.line(50, y, 500, y)
    y -= 20

    # Items
    c.setFont("Helvetica", 10)
    for item in items:
        c.drawString(50, y, item["name"])
        c.drawString(250, y, str(item["qty"]))
        c.drawString(320, y, f"{item['price']:.2f}")
        c.drawString(420, y, f"{item['total']:.2f}")
        y -= 20

        if y < 150:
            c.showPage()
            y = height - 50

    # Totals
    y -= 10
    c.line(50, y, 500, y)
    y -= 25

    c.setFont("Helvetica-Bold", 11)
    c.drawString(320, y, "Subtotal:")
    c.drawString(420, y, subtotal_var.get())
    y -= 20

    c.drawString(320, y, f"GST ({gst_var.get()}%):")
    c.drawString(420, y, gst_amount_var.get())
    y -= 20

    c.drawString(320, y, "Discount:")
    c.drawString(420, y, discount_var.get())
    y -= 20

    c.setFont("Helvetica-Bold", 13)
    c.drawString(320, y, "Grand Total:")
    c.drawString(420, y, grand_total_var.get())
    y -= 30

    # Paid Via
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Paid Via: {paid_via_var.get()}")
    y -= 40

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, y, "Generated using Armaan Invoice Generator")

    c.save()

    # Save record
    record = {
        "invoice_no": invoice_no,
        "date": date_var.get(),
        "customer_name": customer_name_var.get(),
        "customer_phone": customer_phone_var.get(),
        "items": items,
        "gst_percent": gst_var.get(),
        "discount": discount_var.get(),
        "subtotal": subtotal_var.get(),
        "grand_total": grand_total_var.get(),
        "paid_via": paid_via_var.get()
    }

    save_invoice_record(record)

    messagebox.showinfo("Success", f"Invoice PDF created: {filename}")

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Store Settings")
    settings_window.geometry("450x400")
    settings_window.configure(bg="white")
    settings_window.resizable(False, False)

    store_name_var = tk.StringVar(value=settings["store_name"])
    store_address_var = tk.StringVar(value=settings["store_address"])
    store_phone_var = tk.StringVar(value=settings["store_phone"])
    store_location_var = tk.StringVar(value=settings["store_location"])
    logo_path_var = tk.StringVar(value=settings["logo_path"])

    def browse_logo():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            logo_path_var.set(file_path)

    def save_changes():
        settings["store_name"] = store_name_var.get()
        settings["store_address"] = store_address_var.get()
        settings["store_phone"] = store_phone_var.get()
        settings["store_location"] = store_location_var.get()
        settings["logo_path"] = logo_path_var.get()

        save_settings(settings)
        messagebox.showinfo("Saved", "Settings saved successfully!")
        settings_window.destroy()

    tk.Label(settings_window, text="Store Settings", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    tk.Label(settings_window, text="Store Name", bg="white").pack()
    tk.Entry(settings_window, textvariable=store_name_var, width=40).pack(pady=5)

    tk.Label(settings_window, text="Store Address", bg="white").pack()
    tk.Entry(settings_window, textvariable=store_address_var, width=40).pack(pady=5)

    tk.Label(settings_window, text="Store Phone", bg="white").pack()
    tk.Entry(settings_window, textvariable=store_phone_var, width=40).pack(pady=5)

    tk.Label(settings_window, text="Store Location", bg="white").pack()
    tk.Entry(settings_window, textvariable=store_location_var, width=40).pack(pady=5)

    tk.Label(settings_window, text="Logo Path (optional)", bg="white").pack()
    tk.Entry(settings_window, textvariable=logo_path_var, width=40).pack(pady=5)

    tk.Button(settings_window, text="Browse Logo", command=browse_logo).pack(pady=5)
    tk.Button(settings_window, text="Save Settings", bg="green", fg="white", command=save_changes).pack(pady=10)

# ---------------- UI LAYOUT ----------------
tk.Label(root, text="Invoice Maker", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

top_frame = tk.Frame(root, bg="white")
top_frame.pack(fill="x", padx=20)

tk.Label(top_frame, text="Invoice No:", bg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(top_frame, textvariable=invoice_no_var).grid(row=0, column=1, padx=5, pady=5)

tk.Label(top_frame, text="Date:", bg="white").grid(row=0, column=2, padx=5, pady=5)
tk.Entry(top_frame, textvariable=date_var).grid(row=0, column=3, padx=5, pady=5)

tk.Button(top_frame, text="Settings", command=open_settings).grid(row=0, column=4, padx=10)

cust_frame = tk.Frame(root, bg="white")
cust_frame.pack(fill="x", padx=20)

tk.Label(cust_frame, text="Customer Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(cust_frame, textvariable=customer_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)

tk.Label(cust_frame, text="Customer Phone:", bg="white").grid(row=0, column=2, padx=5, pady=5)
tk.Entry(cust_frame, textvariable=customer_phone_var, width=20).grid(row=0, column=3, padx=5, pady=5)

item_frame = tk.Frame(root, bg="white")
item_frame.pack(fill="x", padx=20, pady=10)

item_name_var = tk.StringVar()
item_qty_var = tk.StringVar()
item_price_var = tk.StringVar()

tk.Label(item_frame, text="Item Name", bg="white").grid(row=0, column=0, padx=5)
tk.Entry(item_frame, textvariable=item_name_var, width=30).grid(row=0, column=1, padx=5)

tk.Label(item_frame, text="Qty", bg="white").grid(row=0, column=2, padx=5)
tk.Entry(item_frame, textvariable=item_qty_var, width=10).grid(row=0, column=3, padx=5)

tk.Label(item_frame, text="Price", bg="white").grid(row=0, column=4, padx=5)
tk.Entry(item_frame, textvariable=item_price_var, width=10).grid(row=0, column=5, padx=5)

tk.Button(item_frame, text="Add Item", bg="blue", fg="white", command=add_item).grid(row=0, column=6, padx=10)

item_listbox = tk.Listbox(root, width=120, height=10)
item_listbox.pack(padx=20)

tk.Button(root, text="Delete Selected Item", bg="red", fg="white", command=delete_item).pack(pady=5)

total_frame = tk.Frame(root, bg="white")
total_frame.pack(fill="x", padx=20, pady=10)

subtotal_var = tk.StringVar(value="0")
gst_amount_var = tk.StringVar(value="0")
grand_total_var = tk.StringVar(value="0")

tk.Label(total_frame, text="GST %:", bg="white").grid(row=0, column=0, padx=5)
gst_entry = tk.Entry(total_frame, textvariable=gst_var, width=10)
gst_entry.grid(row=0, column=1, padx=5)
gst_entry.bind("<KeyRelease>", lambda e: update_total())

tk.Label(total_frame, text="Discount:", bg="white").grid(row=0, column=2, padx=5)
discount_entry = tk.Entry(total_frame, textvariable=discount_var, width=10)
discount_entry.grid(row=0, column=3, padx=5)
discount_entry.bind("<KeyRelease>", lambda e: update_total())

tk.Label(total_frame, text="Paid Via:", bg="white").grid(row=0, column=4, padx=5)
paid_menu = tk.OptionMenu(total_frame, paid_via_var, "Cash", "UPI", "Card", "Bank Transfer")
paid_menu.grid(row=0, column=5, padx=5)

tk.Label(total_frame, text="Subtotal:", bg="white").grid(row=1, column=0, padx=5, pady=5)
tk.Label(total_frame, textvariable=subtotal_var, bg="white").grid(row=1, column=1)

tk.Label(total_frame, text="GST Amount:", bg="white").grid(row=1, column=2, padx=5, pady=5)
tk.Label(total_frame, textvariable=gst_amount_var, bg="white").grid(row=1, column=3)

tk.Label(total_frame, text="Grand Total:", bg="white").grid(row=1, column=4, padx=5, pady=5)
tk.Label(total_frame, textvariable=grand_total_var, bg="white").grid(row=1, column=5)

tk.Button(root, text="Generate PDF Invoice", bg="green", fg="white", font=("Arial", 12, "bold"), command=generate_pdf).pack(pady=10)

# Footer
tk.Label(root, text="Generated using Armaan Invoice Generator", bg="white", fg="gray").pack(side="bottom", pady=5)

root.mainloop()
