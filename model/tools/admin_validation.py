import re


def code_validator(code):
    if code is not None:
        if not (isinstance(code, int) and code > 0):
            raise ValueError("کد باید یک عدد صحیح بزرگتر از صفر باشد.")


def name_validator(name):
    if name is not None:
        cleaned = str(name).strip()
        pattern = r"^[a-zA-Z\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF\u200C\s]{2,30}$"
        if not (len(cleaned) >= 2 and re.match(pattern, cleaned)):
            raise ValueError("نام وارد شده نامعتبر است (حداقل ۲ کاراکتر).")


def family_validator(family):
    if family is not None:
        cleaned = str(family).strip()
        pattern = r"^[a-zA-Z\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF\u200C\s]{2,30}$"
        if not (len(cleaned) >= 2 and re.match(pattern, cleaned)):
            raise ValueError("نام خانوادگی وارد شده نامعتبر است.")


def username_validator(username):
    if username is not None:
        if not (isinstance(username, str) and len(username.strip()) >= 3):
            raise ValueError("نام کاربری باید حداقل ۳ کاراکتر باشد.")


def password_validator(password):
    if password is not None:
        if not (isinstance(password, str) and len(password) >= 4):
            raise ValueError("رمز عبور باید حداقل ۴ کاراکتر باشد.")


def locked_validator(locked):
    if locked not in (True, False, 0, 1):
        raise ValueError("وضعیت قفل نامعتبر است.")