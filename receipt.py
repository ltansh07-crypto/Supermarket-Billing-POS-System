import os
from datetime import datetime
import tkinter as tk
import os
from tkinter import messagebox


def generate_receipt(invoice_no, sale_items, subtotal, gst, total,
                     cash_received, change_due):

    # Create receipts folder if it doesn't exist
    folder = "receipts"
    os.makedirs(folder, exist_ok=True)

    # Create receipt text
    receipt = ""
    receipt += "================================\n"
    receipt += "       SUPER MART STORE\n"
    receipt += "         SALES RECEIPT\n"
    receipt += "================================\n"
    receipt += f"Invoice No: {invoice_no}\n"
    receipt += f"Date: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}\n"
    receipt += "--------------------------------\n"
    receipt += "Item           Qty    Amount\n"
    receipt += "--------------------------------\n"

    for item in sale_items:
        name = item["name"]
        quantity = item["quantity"]
        price = item["price"]
        amount = quantity * price

        receipt += f"{name[:14]:14} {quantity:3}  Rs.{amount:.2f}\n"

    receipt += "--------------------------------\n"
    receipt += f"Subtotal:       Rs.{subtotal:.2f}\n"
    receipt += f"GST:            Rs.{gst:.2f}\n"
    receipt += f"TOTAL:          Rs.{total:.2f}\n"
    receipt += f"Cash Received:  Rs.{cash_received:.2f}\n"
    receipt += f"Change:         Rs.{change_due:.2f}\n"
    receipt += "================================\n"
    receipt += "     THANK YOU! VISIT AGAIN\n"
    receipt += "================================\n"

    # Save receipt file
    file_path = os.path.join(folder, f"{invoice_no}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(receipt)

    return file_path

def show_receipt_window(parent, file_path):
    window = tk.Toplevel(parent)
    window.title("Receipt Preview")
    window.geometry("500x600")
    window.configure(bg="white")

    with open(file_path, "r", encoding="utf-8") as file:
        receipt_text = file.read()

    text_area = tk.Text(
        window,
        font=("Courier New", 11),
        wrap="none",
        padx=15,
        pady=15
    )
    text_area.pack(fill="both", expand=True, padx=10, pady=10)

    text_area.insert("1.0", receipt_text)
    text_area.config(state="disabled")
    tk.Button(
    window,
    text="Print Receipt",
    command=lambda: print_receipt(file_path),
    bg="#228B22",
    fg="white",
    padx=20
).pack(pady=5)
    tk.Button(
        window,
        text="Close",
        command=window.destroy,
        bg="#1E3A5F",
        fg="white",
        padx=20
    ).pack(pady=10)
def print_receipt(file_path):
    try:
        os.startfile(file_path, "print")
        messagebox.showinfo(
            "Print Receipt",
            "Receipt sent to the default printer!"
        )
    except Exception as error:
        messagebox.showerror(
            "Print Error",
            f"Could not print receipt:\n{error}"
        )