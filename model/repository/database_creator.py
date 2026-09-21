import sqlite3
from model.entity.customer import Customer


class CustomerRepository:
    def __init__(self):
        self.db_name = "store_db.sqlite"
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    code INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    family TEXT,
                    username TEXT UNIQUE,
                    password TEXT,
                    phone_number TEXT,
                    locked INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def save(self, customer: Customer):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (name, family, username, password, phone_number, locked)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                customer.name,
                customer.family,
                customer.username,
                customer.password,
                customer.phone_number,
                1 if customer.locked else 0
            ))
            conn.commit()
            customer.code = cursor.lastrowid
            return customer

    def edit(self, customer: Customer):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET name = ?, family = ?, username = ?, password = ?, phone_number = ?, locked = ?
                WHERE code = ?
            """, (
                customer.name,
                customer.family,
                customer.username,
                customer.password,
                customer.phone_number,
                1 if customer.locked else 0,
                customer.code
            ))
            conn.commit()
            return customer

    def delete(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE code = ?", (code,))
            conn.commit()

    def find_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, name, family, username, password, phone_number, locked FROM customers")
            rows = cursor.fetchall()
            return [Customer(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6])) for r in rows]

    def find_by_code(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, name, family, username, password, phone_number, locked FROM customers WHERE code = ?", (code,))
            row = cursor.fetchone()
            if row:
                return Customer(row[0], row[1], row[2], row[3], row[4], row[5], bool(row[6]))
            return None

    def find_by_username(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, name, family, username, password, phone_number, locked FROM customers WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return Customer(row[0], row[1], row[2], row[3], row[4], row[5], bool(row[6]))
            return None

    def find_by_username_and_password(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, family, username, password, phone_number, locked FROM customers
                WHERE username = ? AND password = ?
            """, (username, password))
            row = cursor.fetchone()
            if row:
                return Customer(row[0], row[1], row[2], row[3], row[4], row[5], bool(row[6]))
            return None

    def find_by_name_family(self, name, family):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, family, username, password, phone_number, locked FROM customers
                WHERE name LIKE ? AND family LIKE ?
            """, (f"%{name}%", f"%{family}%"))
            rows = cursor.fetchall()
            return [Customer(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6])) for r in rows]