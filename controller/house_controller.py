import sqlite3
from model.entity.house import House
from model.repository.house_repository import HouseRepository


class HouseController:
    def __init__(self):
        self.house_repo = HouseRepository()

    def save(self, code, house_type, meterage, rooms, parking, elevator, storage, address, price, sold=False):
        try:
            if code and not str(code).isdigit():
                return False, "کد ملک باید حتماً عددی باشد."
            house = House(
                int(code) if code else None,
                house_type, meterage, rooms,
                parking, elevator, storage,
                address, price, sold
            )
            self.house_repo.save(house)
            return True, "ملک با موفقیت ثبت شد."
        except sqlite3.IntegrityError:
            return False, "این کد قبلاً برای ملک دیگری ثبت شده است. لطفاً کد دیگری وارد کنید."
        except Exception as e:
            return False, f"خطا در ثبت ملک: {e}"

    def edit(self, code, house_type, meterage, rooms, parking, elevator, storage, address, price, sold=False, original_code=None):
        try:
            if not str(code).isdigit():
                return False, "کد ملک باید حتماً عددی باشد."
            house = House(
                int(code),
                house_type, meterage, rooms,
                parking, elevator, storage,
                address, price, sold
            )
            self.house_repo.edit(house, original_code)
            return True, "اطلاعات ملک با موفقیت ویرایش شد."
        except sqlite3.IntegrityError:
            return False, "این کد قبلاً برای ملک دیگری ثبت شده است."
        except Exception as e:
            return False, f"خطا در ویرایش ملک: {e}"

    def delete(self, code):
        try:
            self.house_repo.delete(code)
            return True, f"ملک با کد {code} با موفقیت حذف شد."
        except Exception as e:
            return False, f"خطا در حذف ملک: {e}"

    def find_all(self):
        try:
            houses = self.house_repo.find_all()
            return True, houses
        except Exception as e:
            return False, f"خطا در دریافت لیست املاک: {e}"

    def find_by_code(self, code):
        try:
            house = self.house_repo.find_by_code(code)
            if house:
                return True, house
            return False, f"ملکی با کد {code} یافت نشد."
        except Exception as e:
            return False, f"خطا در جستجو: {e}"

    def find_by_type_address(self, house_type, address):
        try:
            houses = self.house_repo.find_by_type_address(house_type, address)
            return True, houses
        except Exception as e:
            return False, f"خطا در جستجو: {e}"