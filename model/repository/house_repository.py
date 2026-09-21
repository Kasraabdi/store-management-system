import sqlite3
from model.entity.house import House


class HouseRepository:
    def __init__(self):
        self.db_name = "store_db.sqlite"
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS houses (
                    code INTEGER PRIMARY KEY AUTOINCREMENT,
                    house_type TEXT,
                    meterage TEXT,
                    rooms TEXT,
                    parking INTEGER DEFAULT 0,
                    elevator INTEGER DEFAULT 0,
                    storage INTEGER DEFAULT 0,
                    address TEXT,
                    price TEXT,
                    sold INTEGER DEFAULT 0
                )
            """)
            # افزودن خودکار ستون‌های جدید در صورت وجود دیتابیس قبلی
            for col in ["parking", "elevator", "storage"]:
                try:
                    cursor.execute(f"ALTER TABLE houses ADD COLUMN {col} INTEGER DEFAULT 0")
                except sqlite3.OperationalError:
                    pass
            conn.commit()

    def save(self, house: House):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if house.code:
                cursor.execute("""
                    INSERT INTO houses (code, house_type, meterage, rooms, parking, elevator, storage, address, price, sold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(house.code), house.house_type, house.meterage, house.rooms,
                    1 if house.parking else 0, 1 if house.elevator else 0, 1 if house.storage else 0,
                    house.address, house.price, 1 if house.sold else 0
                ))
            else:
                cursor.execute("""
                    INSERT INTO houses (house_type, meterage, rooms, parking, elevator, storage, address, price, sold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    house.house_type, house.meterage, house.rooms,
                    1 if house.parking else 0, 1 if house.elevator else 0, 1 if house.storage else 0,
                    house.address, house.price, 1 if house.sold else 0
                ))
                house.code = cursor.lastrowid
            conn.commit()
            return house

    def edit(self, house: House, original_code=None):
        target_code = original_code if original_code else house.code
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE houses
                SET code = ?, house_type = ?, meterage = ?, rooms = ?, parking = ?, elevator = ?, storage = ?, address = ?, price = ?, sold = ?
                WHERE code = ?
            """, (
                int(house.code), house.house_type, house.meterage, house.rooms,
                1 if house.parking else 0, 1 if house.elevator else 0, 1 if house.storage else 0,
                house.address, house.price, 1 if house.sold else 0, int(target_code)
            ))
            conn.commit()
            return house

    def delete(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM houses WHERE code = ?", (int(code),))
            conn.commit()

    def find_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, house_type, meterage, rooms, parking, elevator, storage, address, price, sold FROM houses")
            rows = cursor.fetchall()
            return [House(r[0], r[1], r[2], r[3], bool(r[4]), bool(r[5]), bool(r[6]), r[7], r[8], bool(r[9])) for r in rows]

    def find_by_code(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, house_type, meterage, rooms, parking, elevator, storage, address, price, sold FROM houses WHERE code = ?", (int(code),))
            row = cursor.fetchone()
            if row:
                return House(row[0], row[1], row[2], row[3], bool(row[4]), bool(row[5]), bool(row[6]), row[7], row[8], bool(row[9]))
            return None

    def find_by_type_address(self, house_type, address):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, house_type, meterage, rooms, parking, elevator, storage, address, price, sold FROM houses
                WHERE house_type LIKE ? AND address LIKE ?
            """, (f"%{house_type}%", f"%{address}%"))
            rows = cursor.fetchall()
            return [House(r[0], r[1], r[2], r[3], bool(r[4]), bool(r[5]), bool(r[6]), r[7], r[8], bool(r[9])) for r in rows]