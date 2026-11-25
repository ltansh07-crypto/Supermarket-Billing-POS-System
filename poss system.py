# Supermarket Billing & POS System

PRODUCTS = {
    "1": {"name": "Rice (1 kg)", "price": 60.0},
    "2": {"name": "Milk (1 litre)", "price": 55.0},
    "3": {"name": "Bread", "price": 40.0},
    "4": {"name": "Eggs (12 pcs)", "price": 90.0},
    "5": {"name": "Sugar (1 kg)", "price": 50.0},
}


def show_menu():
    print("\nAvailable Products")
    print("-" * 38)
    for code, product in PRODUCTS.items():
        print(f"{code}. {product['name']:<20} Rs. {product['price']:.2f}")


def main():
    cart = []

    print("=" * 40)
    print("   SUPERMARKET BILLING & POS SYSTEM")
    print("=" * 40)

    while True:
        show_menu()
        code = input("\nEnter product code (or 'b' to bill): ").strip().lower()

        if code == "b":
            break

        if code not in PRODUCTS:
            print("Invalid product code.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue
        except ValueError:
            print("Please enter a valid whole number.")
            continue

        product = PRODUCTS[code]
        cart.append({
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity,
        })
        print(f"Added {quantity} x {product['name']}.")

    if not cart:
        print("\nNo items purchased. Thank you!")
        return

    subtotal = sum(item["price"] * item["quantity"] for item in cart)
    discount = subtotal * 0.05 if subtotal >= 1000 else 0.0
    taxable_amount = subtotal - discount
    tax = taxable_amount * 0.05
    grand_total = taxable_amount + tax

    print("\n" + "=" * 40)
    print("                 RECEIPT")
    print("=" * 40)
    print(f"{'Item':<18}{'Qty':>5}{'Amount':>17}")
    print("-" * 40)

    for item in cart:
        amount = item["price"] * item["quantity"]
        print(f"{item['name']:<18}{item['quantity']:>5}{amount:>17.2f}")

    print("-" * 40)
    print(f"{'Subtotal':<23}Rs. {subtotal:>12.2f}")
    print(f"{'Discount (5%)':<23}Rs. {discount:>12.2f}")
    print(f"{'Tax (5%)':<23}Rs. {tax:>12.2f}")
    print(f"{'GRAND TOTAL':<23}Rs. {grand_total:>12.2f}")

    while True:
        try:
            payment = float(input("\nEnter amount received: Rs. "))
            if payment < grand_total:
                print("Insufficient amount. Please pay the full bill.")
                continue
            break
        except ValueError:
            print("Please enter a valid amount.")

    change = payment - grand_total
    print(f"Change: Rs. {change:.2f}")
    print("=" * 40)
    print("      Thank you! Visit again.")


if __name__ == "__main__":
    main()
