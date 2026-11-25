
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database
from datetime import datetime
import receipt
# ==============================
# MAIN APPLICATION CLASS
# ==============================

class SuperMartPOS:

    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("SuperMart POS | Supermarket Billing System")
        self.root.geometry("1200x700")
        self.root.minsize(950, 600)
        self.root.configure(bg="#F4F6FA")

        # Colors
        self.sidebar_color = "#172554"
        self.active_color = "#2563EB"
        self.background_color = "#F4F6FA"
        self.text_color = "#1E293B"

        # Create main layout
        self.create_sidebar()
        self.create_main_content()

        # Open dashboard by default
        self.show_dashboard()

    # ==============================
    # SIDEBAR
    # ==============================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=self.sidebar_color,
            width=240
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Application logo/title
        logo = tk.Label(
            self.sidebar,
            text="🛒 SuperMart",
            font=("Arial", 22, "bold"),
            bg=self.sidebar_color,
            fg="white"
        )
        logo.pack(pady=(30, 5))

        subtitle = tk.Label(
            self.sidebar,
            text="BILLING & POS SYSTEM",
            font=("Arial", 9),
            bg=self.sidebar_color,
            fg="#94A3B8"
        )
        subtitle.pack(pady=(0, 40))

        # Navigation buttons
        self.nav_buttons = {}

        navigation = [
            ("POS Counter", self.show_pos),
            ("Inventory", self.show_inventory),
            ("Dashboard", self.show_dashboard),
            ("Bills", self.show_bills)
        ]

        for name, command in navigation:

            button = tk.Button(
                self.sidebar,
                text="   " + name,
                font=("Arial", 12, "bold"),
                bg=self.sidebar_color,
                fg="white",
                activebackground=self.active_color,
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=15,
                pady=15,
                cursor="hand2",
                command=command
            )

            button.pack(fill="x", padx=12, pady=5)

            self.nav_buttons[name] = button

        # Bottom label
        footer = tk.Label(
            self.sidebar,
            text="SuperMart POS\nVersion 1.0",
            font=("Arial", 9),
            bg=self.sidebar_color,
            fg="#94A3B8"
        )
        footer.pack(side="bottom", pady=20)

    # ==============================
    # MAIN CONTENT AREA
    # ==============================

    def create_main_content(self):

        self.main_frame = tk.Frame(
            self.root,
            bg=self.background_color
        )
        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Top header
        self.header = tk.Frame(
            self.main_frame,
            bg="white",
            height=75
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        self.page_title = tk.Label(
            self.header,
            text="Dashboard",
            font=("Arial", 21, "bold"),
            bg="white",
            fg=self.text_color
        )
        self.page_title.pack(side="left", padx=30)

        self.user_label = tk.Label(
            self.header,
            text="Admin",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#475569"
        )
        self.user_label.pack(side="right", padx=30)

        # Area where pages will appear
        self.content_frame = tk.Frame(
            self.main_frame,
            bg=self.background_color
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

    # ==============================
    # PAGE MANAGEMENT
    # ==============================

    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_page(self, title, active_button):

        self.clear_content()

        self.page_title.config(text=title)

        # Highlight selected navigation button
        for name, button in self.nav_buttons.items():

            if name == active_button:
                button.config(bg=self.active_color)
            else:
                button.config(bg=self.sidebar_color)

    # ==============================
    # DASHBOARD PAGE
    # ==============================

    def show_dashboard(self):

        self.update_page("Dashboard", "Dashboard")

        heading = tk.Label(
            self.content_frame,
            text="Welcome to SuperMart POS",
            font=("Arial", 23, "bold"),
            bg=self.background_color,
            fg=self.text_color
        )
        heading.pack(anchor="w", pady=(10, 5))

        description = tk.Label(
            self.content_frame,
            text="Manage your supermarket operations from one place.",
            font=("Arial", 11),
            bg=self.background_color,
            fg="#64748B"
        )
        description.pack(anchor="w", pady=(0, 25))

        # Dashboard cards
        cards_frame = tk.Frame(
            self.content_frame,
            bg=self.background_color
        )
        cards_frame.pack(fill="x")

        stats = database.get_dashboard_stats()

        cards = [
        ("Total Sales", f"₹ {stats['total_sales']:.2f}"),
        ("Total Products", str(stats["total_products"])),
        ("Total Bills", str(stats["total_bills"])),
        ("Low Stock Items", str(stats["low_stock"]))
        ]

        for title, value in cards:

            card = tk.Frame(
                cards_frame,
                bg="white",
                padx=20,
                pady=20
            )
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=8
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 10),
                bg="white",
                fg="#64748B"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=value,
                font=("Arial", 21, "bold"),
                bg="white",
                fg=self.active_color
            ).pack(anchor="w", pady=10)

        tk.Label(
            self.content_frame,
            text="Sales and business analytics will appear here.",
            font=("Arial", 12),
            bg=self.background_color,
            fg="#64748B"
        ).pack(anchor="w", pady=40)

    
    # ==========================================
    # POS COUNTER PAGE
    # ==========================================

    def show_pos(self):

        self.update_page("POS Counter", "POS Counter")

        self.cart = {}

        # Page heading
        tk.Label(
            self.content_frame,
            text="SuperMart Billing Counter",
            font=("Arial", 21, "bold"),
            bg=self.background_color,
            fg=self.text_color
        ).pack(anchor="w", pady=(0, 10))

        # Main POS layout
        main_area = tk.Frame(
            self.content_frame,
            bg=self.background_color
        )
        main_area.pack(fill="both", expand=True)

        # LEFT SIDE: PRODUCTS
        left = tk.Frame(main_area, bg="white")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(
            left,
            text="Available Products",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=self.text_color
        ).pack(anchor="w", padx=12, pady=12)

        search_frame = tk.Frame(left, bg="white")
        search_frame.pack(fill="x", padx=12)

        self.pos_search = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.pos_search,
            font=("Arial", 11)
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=7)

        tk.Button(
            search_frame,
            text="Search",
            bg=self.active_color,
            fg="white",
            command=self.search_pos_products
        ).pack(side="left", padx=5)

        product_columns = ("id", "name", "price", "stock")

        self.pos_product_table = ttk.Treeview(
            left,
            columns=product_columns,
            show="headings",
            height=15
        )

        for col, heading, width in [
            ("id", "ID", 40),
            ("name", "Product", 145),
            ("price", "Price ₹", 75),
            ("stock", "Stock", 65)
        ]:
            self.pos_product_table.heading(col, text=heading)
            self.pos_product_table.column(
                col, width=width, anchor="center"
            )

        self.pos_product_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        tk.Button(
            left,
            text="ADD TO CART  +",
            bg="#16A34A",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.add_to_cart
        ).pack(fill="x", padx=12, pady=(0, 12))

        self.pos_product_table.bind(
            "<Double-1>",
            lambda event: self.add_to_cart()
        )

        # RIGHT SIDE: CART
        right = tk.Frame(main_area, bg="white", width=390)
        right.pack(side="right", fill="both", padx=(8, 0))
        right.pack_propagate(False)

        tk.Label(
            right,
            text="Shopping Cart",
            font=("Arial", 15, "bold"),
            bg="white",
            fg=self.text_color
        ).pack(anchor="w", padx=12, pady=12)

        cart_columns = ("name", "qty", "price", "total")

        self.cart_table = ttk.Treeview(
            right,
            columns=cart_columns,
            show="headings",
            height=12
        )

        for col, heading, width in [
            ("name", "Product", 120),
            ("qty", "Qty", 45),
            ("price", "Price", 65),
            ("total", "Total", 75)
        ]:
            self.cart_table.heading(col, text=heading)
            self.cart_table.column(
                col, width=width, anchor="center"
            )

        self.cart_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Cart controls
        controls = tk.Frame(right, bg="white")
        controls.pack(fill="x", padx=10, pady=5)

        tk.Button(
            controls,
            text="+ Qty",
            bg="#2563EB",
            fg="white",
            command=self.increase_cart_quantity
        ).pack(side="left", padx=3)

        tk.Button(
            controls,
            text="- Qty",
            bg="#64748B",
            fg="white",
            command=self.decrease_cart_quantity
        ).pack(side="left", padx=3)

        tk.Button(
            controls,
            text="Remove",
            bg="#DC2626",
            fg="white",
            command=self.remove_cart_item
        ).pack(side="left", padx=3)

        # BILL SUMMARY
        summary = tk.Frame(right, bg="#F1F5F9")
        summary.pack(fill="x", padx=10, pady=10)

        self.subtotal_label = tk.Label(
            summary,
            text="Subtotal: ₹0.00",
            font=("Arial", 10),
            bg="#F1F5F9"
        )
        self.subtotal_label.pack(anchor="w", padx=10, pady=3)

        self.gst_label = tk.Label(
            summary,
            text="GST: ₹0.00",
            font=("Arial", 10),
            bg="#F1F5F9"
        )
        self.gst_label.pack(anchor="w", padx=10, pady=3)

        self.total_label = tk.Label(
            summary,
            text="TOTAL: ₹0.00",
            font=("Arial", 16, "bold"),
            fg="#16A34A",
            bg="#F1F5F9"
        )
        self.total_label.pack(anchor="w", padx=10, pady=8)

        tk.Button(
            right,
            text="CHECKOUT & PAY",
            bg="#16A34A",
            fg="white",
            font=("Arial", 13, "bold"),
            command=self.checkout
        ).pack(fill="x", padx=10, pady=(0, 5))

        tk.Button(
            right,
            text="Clear Cart",
            bg="#DC2626",
            fg="white",
            command=self.clear_cart
        ).pack(fill="x", padx=10, pady=(0, 10))

        self.refresh_pos_products()
        self.update_cart_display()

    # ==========================================
    # LOAD PRODUCTS
    # ==========================================

    def refresh_pos_products(self, products=None):

        for row in self.pos_product_table.get_children():
            self.pos_product_table.delete(row)

        if products is None:
            products = database.get_products()

        for product in products:

            self.pos_product_table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["name"],
                    product["price"],
                    product["stock"]
                )
            )

    # ==========================================
    # SEARCH POS PRODUCTS
    # ==========================================

    def search_pos_products(self):

        search_text = self.pos_search.get().strip()

        products = database.search_products(search_text)

        self.refresh_pos_products(products)

    # ==========================================
    # ADD PRODUCT TO CART
    # ==========================================

    def add_to_cart(self):

        selected = self.pos_product_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Product",
                "Please select a product first."
            )
            return

        product_id = int(
            self.pos_product_table.item(
                selected[0], "values"
            )[0]
        )

        products = database.get_products()

        product = next(
            (p for p in products if p["id"] == product_id),
            None
        )

        if product is None:
            messagebox.showerror(
                "Error",
                "Product not found."
            )
            return

        if product["stock"] <= 0:
            messagebox.showwarning(
                "Out of Stock",
                "This product is out of stock."
            )
            return

        if product_id in self.cart:

            if self.cart[product_id]["qty"] >= product["stock"]:
                messagebox.showwarning(
                    "Stock Limit",
                    "Available stock limit reached."
                )
                return

            self.cart[product_id]["qty"] += 1

        else:

            self.cart[product_id] = {
                "id": product_id,
                "name": product["name"],
                "price": float(product["price"]),
                "stock": int(product["stock"]),
                "gst": float(product["gst_rate"] or 0),
                "qty": 1
            }

        self.update_cart_display()

    # ==========================================
    # UPDATE CART DISPLAY AND TOTALS
    # ==========================================

    def update_cart_display(self):

        if not hasattr(self, "cart_table"):
            return

        for row in self.cart_table.get_children():
            self.cart_table.delete(row)

        subtotal = 0
        gst_total = 0

        for product_id, item in self.cart.items():

            item_total = item["price"] * item["qty"]
            item_gst = item_total * item["gst"] / 100

            subtotal += item_total
            gst_total += item_gst

            self.cart_table.insert(
                "",
                "end",
                iid=str(product_id),
                values=(
                    item["name"],
                    item["qty"],
                    f'{item["price"]:.2f}',
                    f'{item_total:.2f}'
                )
            )

        total = subtotal + gst_total

        self.subtotal_label.config(
            text=f"Subtotal: ₹{subtotal:.2f}"
        )

        self.gst_label.config(
            text=f"GST: ₹{gst_total:.2f}"
        )

        self.total_label.config(
            text=f"TOTAL: ₹{total:.2f}"
        )

    # ==========================================
    # INCREASE QUANTITY
    # ==========================================

    def increase_cart_quantity(self):

        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Item",
                "Select a cart item first."
            )
            return

        product_id = int(selected[0])
        item = self.cart[product_id]

        if item["qty"] < item["stock"]:
            item["qty"] += 1
            self.update_cart_display()
        else:
            messagebox.showwarning(
                "Stock Limit",
                "No more stock available."
            )

    # ==========================================
    # DECREASE QUANTITY
    # ==========================================

    def decrease_cart_quantity(self):

        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Item",
                "Select a cart item first."
            )
            return

        product_id = int(selected[0])

        self.cart[product_id]["qty"] -= 1

        if self.cart[product_id]["qty"] <= 0:
            del self.cart[product_id]

        self.update_cart_display()

    # ==========================================
    # REMOVE CART ITEM
    # ==========================================

    def remove_cart_item(self):

        selected = self.cart_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Item",
                "Select an item to remove."
            )
            return

        product_id = int(selected[0])

        del self.cart[product_id]

        self.update_cart_display()

    # ==========================================
    # CLEAR CART
    # ==========================================

    def clear_cart(self):

        if not self.cart:
            return

        confirm = messagebox.askyesno(
            "Clear Cart",
            "Are you sure you want to clear the cart?"
        )

        if confirm:
            self.cart.clear()
            self.update_cart_display()

    # ==========================================
    # CHECKOUT AND PAYMENT
    # ==========================================

    def checkout(self):

        if not self.cart:
            messagebox.showwarning(
                "Empty Cart",
                "Please add products before checkout."
            )
            return

        subtotal = sum(
            item["price"] * item["qty"]
            for item in self.cart.values()
        )

        gst_total = sum(
            item["price"] * item["qty"] * item["gst"] / 100
            for item in self.cart.values()
        )

        total = round(subtotal + gst_total, 2)

        cash = simpledialog.askfloat(
            "Cash Payment",
            f"Total Amount: ₹{total:.2f}\n\nEnter cash received:",
            minvalue=0.0,
            parent=self.root
        )

        if cash is None:
            return

        cash = round(cash, 2)

        if cash < total:
            messagebox.showerror(
                "Insufficient Payment",
                f"Required: ₹{total:.2f}\nReceived: ₹{cash:.2f}"
            )
            return

        change = round(cash - total, 2)

        invoice_no = "INV" + datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        sale_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Save everything in one database transaction
        conn = database.connect_db()

        try:

            conn.execute("BEGIN IMMEDIATE")

            # Check current stock again
            for product_id, item in self.cart.items():

                row = conn.execute(
                    "SELECT stock FROM products WHERE id=?",
                    (product_id,)
                ).fetchone()

                if row is None or row["stock"] < item["qty"]:
                    raise ValueError(
                        f"Insufficient stock for {item['name']}."
                    )

            cursor = conn.execute("""
                INSERT INTO sales (
                    invoice_no, sale_date, subtotal, gst,
                    discount, total, payment_method,
                    cash_received, change_due
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice_no,
                sale_date,
                round(subtotal, 2),
                round(gst_total, 2),
                0,
                total,
                "Cash",
                cash,
                change
            ))

            sale_id = cursor.lastrowid

            for product_id, item in self.cart.items():

                conn.execute("""
                    INSERT INTO sale_items (
                        sale_id, product_id, product_name,
                        quantity, price, gst_rate
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    sale_id,
                    product_id,
                    item["name"],
                    item["qty"],
                    item["price"],
                    item["gst"]
                ))

                conn.execute("""
                    UPDATE products
                    SET stock = stock - ?
                    WHERE id = ?
                """, (
                    item["qty"],
                    product_id
                ))

            conn.commit()

        except Exception as error:

            conn.rollback()

            messagebox.showerror(
                "Checkout Failed",
                str(error)
            )

            return

        finally:
            conn.close()
        print("CHECKOUT SUCCESSFUL - RECEIPT SECTION REACHED")
        
        # Generate receipt after successful payment
        sale_items = []

        for item in self.cart.values():
            sale_items.append({
                "name": item["name"],
                "quantity": item["qty"],
                "price": item["price"]
            })

        try:
            receipt_path = receipt.generate_receipt(
                invoice_no,
                sale_items,
                subtotal,
                gst_total,
                total,
                cash,
                change
            )

            print("Receipt generated:", receipt_path)
            receipt.show_receipt_window(self.root, receipt_path)

        except Exception as error:
            messagebox.showwarning(
                "Receipt Warning",
                f"Payment successful, but receipt could not be generated:\n{error}"
            )


        # Clear cart after successful payment
        self.cart.clear()

        self.update_cart_display()
        self.refresh_pos_products()

        messagebox.showinfo(
            "Payment Successful",
            f"Payment completed!\n\n"
            f"Invoice: {invoice_no}\n"
            f"Total: ₹{total:.2f}\n"
            f"Cash Received: ₹{cash:.2f}\n"
            f"Change: ₹{change:.2f}"
        )

    # ==========================================
    # INVENTORY MANAGEMENT
    # ==========================================

    def show_inventory(self):

        self.update_page("Inventory", "Inventory")

        # Heading
        tk.Label(
            self.content_frame,
            text="Inventory Management",
            font=("Arial", 22, "bold"),
            bg=self.background_color,
            fg=self.text_color
        ).pack(anchor="w", pady=10)

        # Search bar
        search_frame = tk.Frame(
            self.content_frame,
            bg=self.background_color
        )
        search_frame.pack(fill="x", pady=15)

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            width=35
        )
        search_entry.pack(side="left", ipady=8)

        search_entry.insert(0, "")

        tk.Button(
            search_frame,
            text="Search",
            bg=self.active_color,
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.search_inventory
        ).pack(side="left", padx=10)

        tk.Button(
            search_frame,
            text="Show All",
            bg="#64748B",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.refresh_inventory
        ).pack(side="left")

        # Action buttons
        button_frame = tk.Frame(
            self.content_frame,
            bg=self.background_color
        )
        button_frame.pack(fill="x", pady=10)

        tk.Button(
            button_frame,
            text="+ Add Product",
            bg="#16A34A",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.add_inventory_product
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Edit Product",
            bg="#2563EB",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.edit_inventory_product
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Delete Product",
            bg="#DC2626",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.delete_inventory_product
        ).pack(side="left", padx=5)

        # Product table
        table_frame = tk.Frame(
            self.content_frame,
            bg="white"
        )
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = (
            "id",
            "barcode",
            "name",
            "category",
            "price",
            "stock",
            "gst"
        )

        self.inventory_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "barcode": "Barcode",
            "name": "Product Name",
            "category": "Category",
            "price": "Price (₹)",
            "stock": "Stock",
            "gst": "GST (%)"
        }

        widths = {
            "id": 45,
            "barcode": 100,
            "name": 150,
            "category": 110,
            "price": 90,
            "stock": 70,
            "gst": 75
        }

        for col in columns:
            self.inventory_table.heading(
                col,
                text=headings[col]
            )

            self.inventory_table.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.inventory_table.yview
        )

        self.inventory_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.inventory_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(side="right", fill="y")

        self.refresh_inventory()

    # ==========================================
    # DISPLAY PRODUCTS
    # ==========================================

    def refresh_inventory(self):

        if not hasattr(self, "inventory_table"):
            return

        for row in self.inventory_table.get_children():
            self.inventory_table.delete(row)

        products = database.get_products()

        for product in products:

            self.inventory_table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["barcode"] or "",
                    product["name"],
                    product["category"] or "",
                    product["price"],
                    product["stock"],
                    product["gst_rate"]
                )
            )

    # ==========================================
    # SEARCH PRODUCTS
    # ==========================================

    def search_inventory(self):

        search_text = self.search_var.get().strip()

        for row in self.inventory_table.get_children():
            self.inventory_table.delete(row)

        products = database.search_products(search_text)

        for product in products:

            self.inventory_table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["barcode"] or "",
                    product["name"],
                    product["category"] or "",
                    product["price"],
                    product["stock"],
                    product["gst_rate"]
                )
            )

    # ==========================================
    # ADD PRODUCT
    # ==========================================

    def add_inventory_product(self):

        self.open_product_form()

    # ==========================================
    # EDIT PRODUCT
    # ==========================================

    def edit_inventory_product(self):

        selected = self.inventory_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a product first."
            )
            return

        values = self.inventory_table.item(
            selected[0], "values"
        )

        self.open_product_form(values)

    # ==========================================
    # PRODUCT FORM
    # ==========================================

    def open_product_form(self, product=None):

        window = tk.Toplevel(self.root)

        window.title(
            "Edit Product" if product else "Add Product"
        )

        window.geometry("400x480")
        window.configure(bg="white")
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="Edit Product" if product else "Add New Product",
            font=("Arial", 18, "bold"),
            bg="white",
            fg=self.text_color
        ).pack(pady=20)

        fields = [
            "Barcode",
            "Product Name",
            "Category",
            "Price",
            "Stock",
            "GST Rate"
        ]

        entries = {}

        for index, field in enumerate(fields):

            tk.Label(
                window,
                text=field,
                font=("Arial", 10, "bold"),
                bg="white",
                fg=self.text_color
            ).pack(anchor="w", padx=35)

            entry = tk.Entry(
                window,
                font=("Arial", 11),
                width=35
            )
            entry.pack(padx=35, pady=5)

            entries[field] = entry

        if product:

            values = [
                product[1],
                product[2],
                product[3],
                product[4],
                product[5],
                product[6]
            ]

            for field, value in zip(fields, values):
                entries[field].insert(0, str(value))

        def save_product():

            try:

                barcode = entries["Barcode"].get().strip()
                name = entries["Product Name"].get().strip()
                category = entries["Category"].get().strip()

                price = float(entries["Price"].get())
                stock = int(entries["Stock"].get())
                gst = float(entries["GST Rate"].get())

                if not barcode or not name:
                    raise ValueError(
                        "Barcode and product name are required."
                    )

                if price < 0 or stock < 0 or not 0 <= gst <= 100:
                    raise ValueError(
                        "Enter valid price, stock and GST values."
                    )

                if product:

                    database.update_product(
                        product[0],
                        name,
                        category,
                        price,
                        stock,
                        gst
                    )

                    messagebox.showinfo(
                        "Success",
                        "Product updated successfully!"
                    )

                else:

                    success = database.add_product(
                        barcode,
                        name,
                        category,
                        price,
                        stock,
                        gst
                    )

                    if not success:
                        messagebox.showerror(
                            "Error",
                            "Barcode already exists!"
                        )
                        return

                    messagebox.showinfo(
                        "Success",
                        "Product added successfully!"
                    )

                window.destroy()
                self.refresh_inventory()

            except ValueError as error:

                messagebox.showerror(
                    "Invalid Input",
                    str(error) or "Please enter valid values."
                )

            except Exception as error:

                messagebox.showerror(
                    "Database Error",
                    str(error)
                )

        tk.Button(
            window,
            text="Save Product",
            bg="#16A34A",
            fg="white",
            font=("Arial", 11, "bold"),
            command=save_product
        ).pack(pady=20)

    # ==========================================
    # DELETE PRODUCT
    # ==========================================

    def delete_inventory_product(self):

        selected = self.inventory_table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a product first."
            )
            return

        values = self.inventory_table.item(
            selected[0], "values"
        )

        product_id = values[0]
        product_name = values[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {product_name}?"
        )

        if confirm:

            success = database.delete_product(product_id)

            if success:

                messagebox.showinfo(
                    "Success",
                    "Product deleted successfully!"
                )

                self.refresh_inventory()

            else:

                messagebox.showerror(
                    "Cannot Delete",
                    "This product is already linked to a sale."
                )


    # ==============================
    # BILLS PAGE
    # ==============================

    def show_bills(self):

        self.update_page("Bills", "Bills")

        heading = tk.Label(
            self.content_frame,
            text="Billing History",
            font=("Arial", 22, "bold"),
            bg="#f5f6fa",
            fg="#1e293b"
        )
        heading.pack(anchor="w", pady=15)

        columns = (
            "invoice", "date", "subtotal",
            "gst", "total", "payment"
        )

        table = ttk.Treeview(
            self.content_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "invoice": "Invoice Number",
            "date": "Date",
            "subtotal": "Subtotal",
            "gst": "GST",
            "total": "Total",
            "payment": "Payment Method"
        }

        for col in columns:
            table.heading(col, text=headings[col])
            table.column(col, width=150, anchor="center")

        table.pack(fill="both", expand=True, pady=10)

        sales = database.get_sales()

        for sale in sales:
            table.insert(
                "",
                "end",
                values=(
                    sale["invoice_no"],
                    sale["sale_date"],
                    f"₹ {sale['subtotal']:.2f}",
                    f"₹ {sale['gst']:.2f}",
                    f"₹ {sale['total']:.2f}",
                    sale["payment_method"]
                )
            )
# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":

    root = tk.Tk()

    app = SuperMartPOS(root)

    root.mainloop()
