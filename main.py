import tkinter as tk
from tkinter import messagebox

from view.admin_view import AdminView
from view.customer_view import CustomerView
from view.car_view import CarView
from view.house_view import HouseView


def open_admin():
    try:
        AdminView()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در باز کردن پنل مدیران: {e}")


def open_customer():
    try:
        CustomerView()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در باز کردن پنل مشتریان: {e}")


def open_car():
    try:
        CarView()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در باز کردن پنل خودروها: {e}")


def open_house():
    try:
        HouseView()
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در باز کردن پنل املاک: {e}")


def exit_app():
    if messagebox.askyesno("خروج", "آیا از برنامه خارج می‌شوید؟", parent=app):
        app.destroy()


# --- ساخت پنجره اصلی ---
app = tk.Tk()
app.title("سیستم مدیریت فروشگاه")

# باز شدن تمام‌صفحه (Maximized)
try:
    app.state("zoomed")
except Exception:
    app.attributes("-fullscreen", True)

# فریم مرکزی برای قرارگیری متقارن دکمه‌ها در وسط صفحه
center_frame = tk.Frame(app, padx=30, pady=25, relief="ridge", bd=1)
center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# تیتر اصلی
title_lbl = tk.Label(
    center_frame,
    text="سامانه مدیریت جامع فروشگاه",
    font=("Tahoma", 14, "bold"),
    pady=15
)
title_lbl.pack()

# استایل دکمه‌های منو
btn_style = {
    "width": 25,
    "height": 2,
    "font": ("Tahoma", 10),
    "cursor": "hand2"
}

tk.Button(center_frame, text="مدیریت مدیران", command=open_admin, **btn_style).pack(pady=8)
tk.Button(center_frame, text="مدیریت مشتریان", command=open_customer, **btn_style).pack(pady=8)
tk.Button(center_frame, text="مدیریت خودروها", command=open_car, **btn_style).pack(pady=8)
tk.Button(center_frame, text="مدیریت املاک", command=open_house, **btn_style).pack(pady=8)

# دکمه خروج
tk.Button(
    center_frame,
    text="خروج از برنامه",
    command=exit_app,
    width=25,
    height=1,
    fg="red",
    font=("Tahoma", 10, "bold"),
    cursor="hand2"
).pack(pady=15)

if __name__ == "__main__":
    app.mainloop()