from controller.car_controller import CarController
from model.repository.database_creator import create_database

create_database()

controller = CarController()

# ثبت بدون علامت $ و با نوع داده عددی صحیح
status, message = controller.save("بنز", "CLS", "مشکی", 2022, 50000, False)
print(f"نتیجه ثبت خودرو: {status} -> {message}")

status, cars = controller.find_all()
print(f"لیست کل خودروها: {cars}")