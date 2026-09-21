import sqlite3
from model.entity.car import Car
from model.repository.car_repository import CarRepository


class CarController:
    def __init__(self):
        self.car_repo = CarRepository()

    def save(self, code, brand, model, color, year, price, sold=False):
        try:
            if code and not str(code).isdigit():
                return False, "کد خودرو باید حتماً عددی باشد."
            car = Car(int(code) if code else None, brand, model, color, year, price, sold)
            self.car_repo.save(car)
            return True, "خودرو با موفقیت ثبت شد."
        except sqlite3.IntegrityError:
            return False, "این کد قبلاً برای خودروی دیگری ثبت شده است. لطفاً کد دیگری وارد کنید."
        except Exception as e:
            return False, f"خطا در ثبت خودرو: {e}"

    def edit(self, code, brand, model, color, year, price, sold=False, original_code=None):
        try:
            if not str(code).isdigit():
                return False, "کد خودرو باید حتماً عددی باشد."
            car = Car(int(code), brand, model, color, year, price, sold)
            self.car_repo.edit(car, original_code)
            return True, "اطلاعات خودرو با موفقیت ویرایش شد."
        except sqlite3.IntegrityError:
            return False, "این کد قبلاً برای خودروی دیگری ثبت شده است."
        except Exception as e:
            return False, f"خطا در ویرایش خودرو: {e}"

    def delete(self, code):
        try:
            self.car_repo.delete(code)
            return True, f"خودرو با کد {code} با موفقیت حذف شد."
        except Exception as e:
            return False, f"خطا در حذف خودرو: {e}"

    def find_all(self):
        try:
            cars = self.car_repo.find_all()
            return True, cars
        except Exception as e:
            return False, f"خطا در دریافت لیست خودروها: {e}"

    def find_by_code(self, code):
        try:
            car = self.car_repo.find_by_code(code)
            if car:
                return True, car
            return False, f"خودرویی با کد {code} یافت نشد."
        except Exception as e:
            return False, f"خطا در جستجو: {e}"

    def find_by_brand_model(self, brand, model):
        try:
            cars = self.car_repo.find_by_brand_model(brand, model)
            return True, cars
        except Exception as e:
            return False, f"خطا در جستجو: {e}"