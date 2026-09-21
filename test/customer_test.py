from controller.customer_controller import CustomerController
from model.repository.database_creator import create_database

create_database()

controller = CustomerController()

status, existing = controller.find_by_username("ALI123")
if status and existing:
    controller.delete(existing.code)

status, message = controller.save("علی", "بهرامی", "ALI123", "ali345", "09193647381", False)
print(f"نتیجه ثبت مشتری: {status} -> {message}")

status, customers = controller.find_all()
print(f"لیست کل مشتریان: {customers}")