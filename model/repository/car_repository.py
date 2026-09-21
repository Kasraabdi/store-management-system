import sqlite3
from model.entity.car import Car


class CarRepository:
    def __init__(self):
        self.db_name = "store_db.sqlite"
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    code INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT,
                    model TEXT,
                    color TEXT,
                    year TEXT,
                    price TEXT,
                    sold INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def save(self, car: Car):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if car.code:
                cursor.execute("""
                    INSERT INTO cars (code, brand, model, color, year, price, sold)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (int(car.code), car.brand, car.model, car.color, car.year, car.price, 1 if car.sold else 0))
            else:
                cursor.execute("""
                    INSERT INTO cars (brand, model, color, year, price, sold)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (car.brand, car.model, car.color, car.year, car.price, 1 if car.sold else 0))
                car.code = cursor.lastrowid
            conn.commit()
            return car

    def edit(self, car: Car, original_code=None):
        target_code = original_code if original_code else car.code
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars
                SET code = ?, brand = ?, model = ?, color = ?, year = ?, price = ?, sold = ?
                WHERE code = ?
            """, (int(car.code), car.brand, car.model, car.color, car.year, car.price, 1 if car.sold else 0, int(target_code)))
            conn.commit()
            return car

    def delete(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cars WHERE code = ?", (int(code),))
            conn.commit()

    def find_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, brand, model, color, year, price, sold FROM cars")
            rows = cursor.fetchall()
            return [Car(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6])) for r in rows]

    def find_by_code(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT code, brand, model, color, year, price, sold FROM cars WHERE code = ?", (int(code),))
            row = cursor.fetchone()
            if row:
                return Car(row[0], row[1], row[2], row[3], row[4], row[5], bool(row[6]))
            return None

    def find_by_brand_model(self, brand, model):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, brand, model, color, year, price, sold FROM cars
                WHERE brand LIKE ? AND model LIKE ?
            """, (f"%{brand}%", f"%{model}%"))
            rows = cursor.fetchall()
            return [Car(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6])) for r in rows]