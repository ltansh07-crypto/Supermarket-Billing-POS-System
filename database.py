
import sqlite3
import os

# ==================================
# DATABASE CONNECTION
# ==================================

DB_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "supermarket.db"
)


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==================================
# CREATE DATABASE TABLES
# ==================================

def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            gst_rate REAL DEFAULT 0
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT UNIQUE,
            sale_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            gst REAL NOT NULL,
            discount REAL DEFAULT 0,
            total REAL NOT NULL,
            payment_method TEXT,
            cash_received REAL DEFAULT 0,
            change_due REAL DEFAULT 0
        )
    """)

    # Individual items in each sale
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            gst_rate REAL DEFAULT 0,
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


# ==================================
# INSERT SAMPLE PRODUCTS
# ==================================

def insert_sample_products():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:

        products = [
            ("1001", "Rice 1kg", "Groceries", 65, 100, 5),
            ("1002", "Wheat Flour 1kg", "Groceries", 45, 80, 5),
            ("1003", "Milk 1L", "Dairy", 60, 50, 5),
            ("1004", "Sugar 1kg", "Groceries", 48, 90, 5),
            ("1005", "Cooking Oil 1L", "Groceries", 150, 40, 5),
            ("1006", "Biscuits", "Snacks", 20, 100, 5),
            ("1007", "Soap", "Personal Care", 35, 60, 18),
            ("1008", "Shampoo", "Personal Care", 120, 30, 18),
            ("1009", "Bread", "Bakery", 40, 25, 5),
            ("1010", "Salt 1kg", "Groceries", 25, 75, 5)
        ]

        cursor.executemany("""
            INSERT INTO products
            (barcode, name, category, price, stock, gst_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, products)

        print("Sample products inserted successfully!")

    else:
        print("Products already exist. Sample data skipped.")

    conn.commit()
    conn.close()


# ==================================
# GET ALL PRODUCTS
# ==================================

def get_products():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products ORDER BY id")

    products = cursor.fetchall()

    conn.close()

    return products


# ==================================
# ADD NEW PRODUCT
# ==================================

def add_product(barcode, name, category, price, stock, gst_rate):

    conn = connect_db()

    try:

        conn.execute("""
            INSERT INTO products
            (barcode, name, category, price, stock, gst_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (barcode, name, category, price, stock, gst_rate))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ==================================
# UPDATE PRODUCT
# ==================================

def update_product(product_id, name, category, price, stock, gst_rate):

    conn = connect_db()

    conn.execute("""
        UPDATE products
        SET name=?, category=?, price=?, stock=?, gst_rate=?
        WHERE id=?
    """, (name, category, price, stock, gst_rate, product_id))

    conn.commit()
    conn.close()


# ==================================
# DELETE PRODUCT
# ==================================

def delete_product(product_id):

    conn = connect_db()

    try:
        conn.execute(
            "DELETE FROM products WHERE id=?",
            (product_id,)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ==================================
# SEARCH PRODUCTS
# ==================================

def search_products(search_text):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE name LIKE ?
        OR barcode LIKE ?
        OR category LIKE ?
        ORDER BY name
    """, (
        f"%{search_text}%",
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    results = cursor.fetchall()

    conn.close()

    return results


# ==================================
# RUN DATABASE
# ==================================

# ==================================
# GET DASHBOARD STATISTICS
# ==================================

def get_dashboard_stats():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM sales")
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sales")
    total_bills = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products WHERE stock <= 10")
    low_stock = cursor.fetchone()[0]

    conn.close()

    return {
        "total_sales": total_sales,
        "total_products": total_products,
        "total_bills": total_bills,
        "low_stock": low_stock
    }


# ==================================
# GET ALL BILLS
# ==================================

def get_sales():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT invoice_no, sale_date, subtotal, gst, total,
               payment_method
        FROM sales
        ORDER BY id DESC
    """)

    sales = cursor.fetchall()

    conn.close()

    return sales

if __name__ == "__main__":

    create_tables()
    insert_sample_products()

    print("\n========== SUPERMART PRODUCTS ==========")

    for product in get_products():

        print(
            product["id"],
            product["name"],
            "| Price: ₹", product["price"],
            "| Stock:", product["stock"]
        )

    print("\nDatabase setup completed!")
