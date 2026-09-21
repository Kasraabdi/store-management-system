class Car:
    def __init__(self, code=None, brand=None, model=None, color=None, year=None, price=None, sold=False):
        self.code = code
        self.brand = str(brand).strip() if brand is not None else ""
        self.model = str(model).strip() if model is not None else ""
        self.color = str(color).strip() if color is not None else ""
        self.year = str(year).strip() if year is not None else ""
        self.price = str(price).strip() if price is not None else ""
        self.sold = bool(sold)

    def __repr__(self):
        return f"Car({self.code}, {self.brand}, {self.model}, {self.color}, {self.year}, {self.price}, {self.sold})"