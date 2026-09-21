class House:
    def __init__(self, code=None, house_type=None, meterage=None, rooms=None,
                 parking=False, elevator=False, storage=False,
                 address=None, price=None, sold=False):
        self.code = code
        self.house_type = str(house_type).strip() if house_type is not None else ""
        self.meterage = str(meterage).strip() if meterage is not None else ""
        self.rooms = str(rooms).strip() if rooms is not None else ""
        self.parking = bool(parking)
        self.elevator = bool(elevator)
        self.storage = bool(storage)
        self.address = str(address).strip() if address is not None else ""
        self.price = str(price).strip() if price is not None else ""
        self.sold = bool(sold)

    def __repr__(self):
        return (f"House({self.code}, {self.house_type}, {self.meterage}, {self.rooms}, "
                f"{self.parking}, {self.elevator}, {self.storage}, {self.address}, {self.price}, {self.sold})")