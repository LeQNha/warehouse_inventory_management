import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), "database", "warehouse.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'staff',
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category_id INTEGER,
            quantity INTEGER DEFAULT 0,
            import_price REAL DEFAULT 0,
            export_price REAL DEFAULT 0,
            supplier_id INTEGER,
            location TEXT,
            min_quantity INTEGER DEFAULT 10,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        );
    """)

    # Seed default admin
    admin_pw = hash_password("admin123")
    c.execute("INSERT OR IGNORE INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
              ("admin", admin_pw, "Administrator", "admin"))
    staff_pw = hash_password("staff123")
    c.execute("INSERT OR IGNORE INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
              ("staff", staff_pw, "Staff User", "staff"))

    # Seed categories
    for cat in [("Điện tử", "Thiết bị điện tử"), ("Thực phẩm", "Thực phẩm & đồ uống"),
                ("Nội thất", "Bàn ghế, tủ kệ"), ("Quần áo", "Trang phục thời trang"),
                ("Văn phòng phẩm", "Dụng cụ văn phòng")]:
        c.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", cat)


    conn.commit()
    conn.close()
