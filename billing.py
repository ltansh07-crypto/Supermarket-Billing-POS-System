
import receipt


def calculate_bill(cart):
    subtotal = 0

    for item in cart:
        subtotal += item["price"] * item["quantity"]

    gst = subtotal * 0.05
    total = subtotal + gst

    return subtotal, gst, total


def checkout(cart):
    if not cart:
        print("Your cart is empty!")
        return

    subtotal, gst, total = calculate_bill(cart)

    print("\n========== BILL SUMMARY ==========")
    print(f"Subtotal: Rs.{subtotal:.2f}")
    print(f"GST (5%): Rs.{gst:.2f}")
    print(f"Total: Rs.{total:.2f}")

    cash_received = float(input("\nEnter cash received: Rs."))

    if cash_received < total:
        print("Insufficient payment!")
        return

    change_due = cash_received - total

    invoice_no = "INV" + str(__import__("datetime").datetime.now().strftime("%Y%m%d%H%M%S"))

    file_path = receipt.generate_receipt(
        invoice_no,
        cart,
        subtotal,
        gst,
        total,
        cash_received,
        change_due
    )

    print("\nPayment successful!")
    print(f"Change returned: Rs.{change_due:.2f}")
    print("Receipt generated:", file_path)

    cart.clear()
