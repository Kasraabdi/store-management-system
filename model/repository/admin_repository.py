import sqlite3
from model.entity.admin import Admin


class AdminRepository:
    def __init__(self):
        self.db_name = "store_db.sqlite"
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    code INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    family TEXT,
                    username TEXT UNIQUE,
                    password TEXT,
                    locked INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def save(self, admin: Admin):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if admin.code:
                cursor.execute("""
                    INSERT INTO admins (code, name, family, username, password, locked)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (int(admin.code), admin.name, admin.family, admin.username, admin.password, 1 if admin.locked else 0))
            else:
                cursor.execute("""
                    INSERT INTO admins (name, family, username, password, locked)
                    VALUES (?, ?, ?, ?, ?)
                """, (admin.name, admin.family, admin.username, admin.password, 1 if admin.locked else 0))
                admin.code = cursor.lastrowid
            conn.commit()
            return admin

    def edit(self, admin: Admin, original_code=None):
        target_code = original_code if original_code else admin.code
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE admins
                SET code = ?, name = ?, family = ?, username = ?, password = ?, locked = ?
                WHERE code = ?
            """, (int(admin.code), admin.name, admin.family, admin.username, admin.password, 1 if admin.locked else 0, int(target_code)))
            conn.commit()
            return admin

    def delete(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admins WHERE code = ?", (int(code),))
            conn.commit()

    def find_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, name, family, username, password, locked FROM admins")
            rows = cursor.fetchall()
            return [Admin(r[0], r[1], r[2], r[3], r[4], bool(r[5])) for r in rows]

    def find_by_code(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, name, family, username, password, locked FROM admins WHERE code = ?", (int(code),))
            row = cursor.fetchone()
            if row:
                return Admin(row[0], row[1], row[2], row[3], row[4], bool(row[5]))
            return None

    def find_by_name_family(self, name, family):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, family, username, password, locked FROM admins
                WHERE name LIKE ? AND family LIKE ?
            """, (f"%{name}%", f"%{family}%"))
            rows = cursor.fetchall()
            return [Admin(r[0], r[1], r[2], r[3], r[4], bool(r[5])) for r in rows]

    def find_by_username(self, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, name, family, username, password, locked FROM admins WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return Admin(row[0], row[1], row[2], row[3], row[4], bool(row[5]))
            return None

    def find_by_username_and_password(self, username, password):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, family, username, password, locked FROM admins
                WHERE username = ? AND password = ?
            """, (username, password))
            row = cursor.fetchone()
            if row:
                return Admin(row[0], row[1], row[2], row[3], row[4], bool(row[5]))
            return None