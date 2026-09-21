from controller.house_controller import HouseController
from model.repository.database_creator import create_database

create_database()

controller = HouseController()

status, message = controller.save(
    region="اکباتان",
    address="بلوک ۵ ورودی ۲",
    floor=2,
    area=95.5,
    rooms=2,
    elevator=True,
    parking=True,
    storage=True,
    year=1395,
    price=6500000000,
    locked=False
)
print(f"نتیجه ثبت خانه: {status} -> {message}")

status, houses = controller.find_all()
print(f"لیست کل خانه‌ها: {houses}")