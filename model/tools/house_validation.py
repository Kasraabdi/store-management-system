import re


def code_validator(code):
    if code is not None:
        if not (isinstance(code, int) and code > 0):
            raise ValueError("کد باید یک عدد صحیح بزرگتر از صفر باشد.")


def region_validator(region):
    if region is not None:
        if not (isinstance(region, str) and re.match(r"^[a-zA-Zآ-ی0-9\s]{2,40}$", region.strip())):
            raise ValueError("نام منطقه نامعتبر است.")


def address_validator(address):
    if address is not None:
        if not (isinstance(address, str) and len(address.strip()) >= 3):
            raise ValueError("آدرس باید حداقل ۳ کاراکتر باشد.")


def floor_validator(floor):
    if floor is not None:
        try:
            int(floor)
        except (ValueError, TypeError):
            raise ValueError("شماره طبقه نامعتبر است.")


def area_validator(area):
    if area is not None:
        try:
            area_val = float(area)
            if area_val <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("متراژ وارد شده نامعتبر است.")


def rooms_validator(rooms):
    if rooms is not None:
        try:
            rooms_val = int(rooms)
            if rooms_val < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("تعداد اتاق نامعتبر است.")


def elevator_validator(elevator):
    if elevator not in (True, False, 0, 1):
        raise ValueError("وضعیت آسانسور نامعتبر است.")


def parking_validator(parking):
    if parking not in (True, False, 0, 1):
        raise ValueError("وضعیت پارکینگ نامعتبر است.")


def storage_validator(storage):
    if storage not in (True, False, 0, 1):
        raise ValueError("وضعیت انباری نامعتبر است.")


def year_validator(year):
    if year is not None:
        try:
            year_val = int(year)
            if not ((1300 <= year_val <= 1500) or (1900 <= year_val <= 2100)):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("سال ساخت نامعتبر است.")


def price_validator(price):
    if price is not None:
        try:
            price_val = float(price)
            if price_val < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("قیمت نامعتبر است.")


def locked_validator(locked):
    if locked not in (True, False, 0, 1):
        raise ValueError("وضعیت قفل نامعتبر است.")