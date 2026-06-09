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
                    
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
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
                    
        CREATE TABLE IF NOT EXISTS stock_in (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            import_price REAL,
            supplier_id INTEGER,
            note TEXT,
            import_date TEXT DEFAULT (datetime('now','localtime')),
            created_by INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS stock_out (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            export_price REAL,
            customer TEXT,
            note TEXT,
            export_date TEXT DEFAULT (datetime('now','localtime')),
            created_by INTEGER,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    """)

    # Seed default admin
    admin_pw = hash_password("admin123")
    c.execute("INSERT OR IGNORE INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
              ("admin", admin_pw, "Administrator", "admin"))
    staff_pw = hash_password("staff123")
    c.execute("INSERT OR IGNORE INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
              ("staff", staff_pw, "Staff User", "staff"))

    conn.commit()
    conn.close()
