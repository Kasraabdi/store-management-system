import sqlite3
from model.entity.admin import Admin
from model.repository.admin_repository import AdminRepository


class AdminController:
    def __init__(self):
        self.admin_repo = AdminRepository()

    def save(self, code, name, family, username, password, locked=False):
        try:
            if code and not str(code).isdigit():
                return False, "کد مدیر باید حتماً عدد باشد."
            admin = Admin(int(code) if code else None, name, family, username, password, locked)
            self.admin_repo.save(admin)
            return True, "اطلاعات مدیر با موفقیت ثبت شد."
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: admins.code" in str(e):
                return False, "این کد قبلاً برای مدیر دیگری ثبت شده است."
            return False, "این نام کاربری قبلاً ثبت شده است. لطفاً نام کاربری دیگری انتخاب کنید."
        except Exception as e:
            return False, f"خطا در ثبت مدیر: {e}"

    def edit(self, code, name, family, username, password, locked=False, original_code=None):
        try:
            if not str(code).isdigit():
                return False, "کد مدیر باید حتماً عدد باشد."
            admin = Admin(int(code), name, family, username, password, locked)
            self.admin_repo.edit(admin, original_code)
            return True, "اطلاعات مدیر با موفقیت ویرایش شد."
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: admins.code" in str(e):
                return False, "این کد قبلاً برای مدیر دیگری ثبت شده است."
            return False, "این نام کاربری برای مدیر دیگری ثبت شده است."
        except Exception as e:
            return False, f"خطا در ویرایش مدیر: {e}"

    def delete(self, code):
        try:
            self.admin_repo.delete(code)
            return True, f"مدیر با کد {code} با موفقیت حذف شد."
        except Exception as e:
            return False, f"خطا در حذف مدیر: {e}"

    def find_all(self):
        try:
            admins = self.admin_repo.find_all()
            return True, admins
        except Exception as e:
            return False, f"خطا در دریافت لیست مدیران: {e}"

    def find_by_code(self, code):
        try:
            admin = self.admin_repo.find_by_code(code)
            if admin:
                return True, admin
            return False, f"مدیری با کد {code} یافت نشد."
        except Exception as e:
            return False, f"خطا در جستجو: {e}"

    def find_by_name_family(self, name, family):
        try:
            admins = self.admin_repo.find_by_name_family(name, family)
            return True, admins
        except Exception as e:
            return False, f"خطا در جستجو: {e}"

    def find_by_username(self, username):
        try:
            admin = self.admin_repo.find_by_username(username)
            if admin:
                return True, admin
            return False, f"مدیری با نام کاربری {username} یافت نشد."
        except Exception as e:
            return False, f"خطا در جستجو: {e}"

    def find_by_username_and_password(self, username, password):
        try:
            admin = self.admin_repo.find_by_username_and_password(username, password)
            if admin:
                return True, admin
            return False, "نام کاربری یا رمز عبور اشتباه است."
        except Exception as e:
            return False, f"خطا در ورود به سیستم: {e}"