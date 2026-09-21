import sqlite3
from model.entity.customer import Customer
from model.repository.customer_repository import CustomerRepository


class CustomerController:
    def __init__(self):
        self.customer_repo = CustomerRepository()

    def save(self, code, name, family, username, password, phone_number, locked=False):
        try:
            if code and not str(code).isdigit():
                return False, "کد مشتری باید حتماً عدد باشد."

            if hasattr(self.customer_repo, "find_by_username") and self.customer_repo.find_by_username(username):
                return False, "این نام کاربری قبلاً ثبت شده است. لطفاً نام کاربری دیگری انتخاب کنید."

            customer = Customer(int(code) if code else None, name, family, username, password, phone_number, locked)
            self.customer_repo.save(customer)
            return True, "اطلاعات مشتری با موفقیت ثبت شد."
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: customers.code" in str(e):
                return False, "این کد قبلاً برای مشتری دیگری ثبت شده است."
            return False, "این نام کاربری تکراری است."
        except Exception as e:
            return False, f"خطا در ثبت مشتری: {e}"

    def edit(self, code, name, family, username, password, phone_number, locked=False, original_code=None):
        try:
            if not str(code).isdigit():
                return False, "کد مشتری باید حتماً عدد باشد."

            if hasattr(self.customer_repo, "find_by_username"):
                existing = self.customer_repo.find_by_username(username)
                target = int(original_code if original_code else code)
                if existing and existing.code != target:
                    return False, "این نام کاربری برای مشتری دیگری ثبت شده است."

            customer = Customer(int(code), name, family, username, password, phone_number, locked)
            self.customer_repo.edit(customer, original_code)
            return True, "اطلاعات مشتری با موفقیت ویرایش شد."
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: customers.code" in str(e):
                return False, "این کد قبلاً برای مشتری دیگری ثبت شده است."
            return False, "این نام کاربری تکراری است."
        except Exception as e:
            return False, f"خطا در ویرایش مشتری: {e}"

    def delete(self, code):
        try:
            self.customer_repo.delete(code)
            return True, f"مشتری با کد {code} با موفقیت حذف شد."
        except Exception as e:
            return False, f"خطا در حذف مشتری: {e}"

    def find_all(self):
        try:
            customers = self.customer_repo.find_all()
            return True, customers
        except Exception as e:
            return False, f"خطا در دریافت لیست مشتریان: {e}"

    def find_by_code(self, code):
        try:
            customer = self.customer_repo.find_by_code(code)
            if customer:
                return True, customer
            return False, f"مشتری با کد {code} یافت نشد."
        except Exception as e:
            return False, f"خطا در جستجو: {e}"

    def find_by_name_family(self, name, family):
        try:
            customers = self.customer_repo.find_by_name_family(name, family)
            return True, customers
        except Exception as e:
            return False, f"خطا در جستجو: {e}"