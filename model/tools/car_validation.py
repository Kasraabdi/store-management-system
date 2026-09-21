import re


def code_validator(code):
    if code is not None:
        if not (isinstance(code, int) and code > 0):
            raise ValueError("کد باید یک عدد صحیح بزرگتر از صفر باشد.")


def name_validator(name):
    if name is not None:
        if not (isinstance(name, str) and re.match(r"^[a-zA-Zآ-ی0-9\s]{2,30}$", name.strip())):
            raise ValueError("نام خودرو وارد شده نامعتبر است.")


def model_validator(model):
    if model is not None:
        if not (isinstance(model, str) and len(model.strip()) >= 2):
            raise ValueError("مدل خودرو باید حداقل ۲ کاراکتر باشد.")


def color_validator(color):
    if color is not None:
        if not (isinstance(color, str) and re.match(r"^[a-zA-Zآ-ی\s]{2,20}$", color.strip())):
            raise ValueError("رنگ خودرو نامعتبر است.")


def year_validator(year):
    if year is not None:
        try:
            year_val = int(year)
            if not ((1300 <= year_val <= 1500) or (1900 <= year_val <= 2100)):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("سال ساخت نامعتبر است (باید یک سال معتبر ۴ رقمی باشد).")


def price_validator(price):
    if price is not None:
        try:
            price_val = float(price)
            if price_val < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("قیمت خودرو نامعتبر است.")


def locked_validator(locked):
    if locked not in (True, False, 0, 1):
        raise ValueError("وضعیت قفل نامعتبر است.")