class Admin:
    def __init__(self, code=None, name=None, family=None, username=None, password=None, locked=False):
        self.code = code
        self.name = str(name).strip() if name is not None else ""
        self.family = str(family).strip() if family is not None else ""
        self.username = str(username).strip() if username is not None else ""
        self.password = str(password).strip() if password is not None else ""
        self.locked = bool(locked)

    def __repr__(self):
        return f"Admin({self.code}, {self.name}, {self.family}, {self.username}, {self.password}, {self.locked})"