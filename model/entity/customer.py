class Customer:
    def __init__(self, code=None, name=None, family=None, username=None, password=None, phone_number="09", locked=False):
        self.code = code
        self.name = name
        self.family = family
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.locked = locked

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is not None:
            cleaned = str(value).strip()
            if len(cleaned) < 2:
                raise ValueError("نام وارد شده نامعتبر است (حداقل ۲ کاراکتر).")
            self._name = cleaned
        else:
            self._name = None

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, value):
        if value is not None:
            cleaned = str(value).strip()
            if len(cleaned) < 2:
                raise ValueError("نام خانوادگی وارد شده نامعتبر است.")
            self._family = cleaned
        else:
            self._family = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value is not None:
            cleaned = str(value).strip()
            if len(cleaned) < 3:
                raise ValueError("نام کاربری باید حداقل ۳ کاراکتر باشد.")
            self._username = cleaned
        else:
            self._username = None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if value is not None:
            cleaned = str(value).strip()
            if len(cleaned) < 4:
                raise ValueError("رمز عبور باید حداقل ۴ کاراکتر باشد.")
            self._password = cleaned
        else:
            self._password = None

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if value is not None:
            self._phone_number = str(value).strip()
        else:
            self._phone_number = "09"

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = bool(value)

    def __repr__(self):
        return f"{self.__dict__}"