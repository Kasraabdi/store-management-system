import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg

from controller.car_controller import CarController


class CarView:
    def __init__(self):
        self.controller = CarController()
        self.selected_code = None

        if tk._default_root:
            self.win = Toplevel()
            self.win.transient(tk._default_root)
        else:
            self.win = Tk()

        self.win.title("مدیریت خودروها")

        try:
            self.win.state("zoomed")
        except Exception:
            self.win.attributes("-fullscreen", True)

        self.win.focus_force()

        # --- ویجت‌های فرم ---
        Label(self.win, text="کد").place(x=20, y=20)
        self.code_txt = Entry(self.win, width=23)  # فعال بودن ورودی دستی کد
        self.code_txt.place(x=120, y=20)

        Label(self.win, text="برند").place(x=20, y=65)
        self.brand_txt = Entry(self.win, width=23)
        self.brand_txt.place(x=120, y=65)

        Label(self.win, text="مدل").place(x=20, y=110)
        self.model_txt = Entry(self.win, width=23)
        self.model_txt.place(x=120, y=110)

        Label(self.win, text="رنگ").place(x=20, y=155)
        self.color_txt = Entry(self.win, width=23)
        self.color_txt.place(x=120, y=155)

        Label(self.win, text="سال ساخت").place(x=20, y=200)
        self.year_txt = Entry(self.win, width=23)
        self.year_txt.place(x=120, y=200)

        Label(self.win, text="قیمت").place(x=20, y=245)
        self.price_txt = Entry(self.win, width=23)
        self.price_txt.bind("<KeyRelease>", self.format_price_input)
        self.price_txt.place(x=120, y=245)

        Label(self.win, text="وضعیت فروش").place(x=20, y=290)
        self.sold_var = IntVar(master=self.win, value=0)
        self.chk_sold = Checkbutton(self.win, text="فروخته شده", variable=self.sold_var, onvalue=1, offvalue=0)
        self.chk_sold.place(x=120, y=290)

        # --- بخش جستجو ---
        Label(self.win, text="جستجو با برند").place(x=300, y=20)
        self.search_brand_txt = Entry(self.win, width=18)
        self.search_brand_txt.bind("<KeyRelease>", self.search_brand_model)
        self.search_brand_txt.place(x=390, y=20)

        Label(self.win, text="جستجو با مدل").place(x=540, y=20)
        self.search_model_txt = Entry(self.win, width=18)
        self.search_model_txt.bind("<KeyRelease>", self.search_brand_model)
        self.search_model_txt.place(x=630, y=20)

        # --- جدول اطلاعات ---
        table_frame = Frame(self.win)
        table_frame.place(x=300, y=70, relwidth=0.65, relheight=0.82)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        columns = ("code", "brand", "model", "color", "year", "price", "sold")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.table.yview)
        self.table.pack(fill=BOTH, expand=True)

        self.table.heading("code", text="کد")
        self.table.heading("brand", text="برند")
        self.table.heading("model", text="مدل")
        self.table.heading("color", text="رنگ")
        self.table.heading("year", text="سال ساخت")
        self.table.heading("price", text="قیمت")
        self.table.heading("sold", text="وضعیت")

        self.table.column("code", width=50, anchor=CENTER)
        self.table.column("brand", width=100, anchor=CENTER)
        self.table.column("model", width=110, anchor=CENTER)
        self.table.column("color", width=90, anchor=CENTER)
        self.table.column("year", width=90, anchor=CENTER)
        self.table.column("price", width=140, anchor=CENTER)
        self.table.column("sold", width=80, anchor=CENTER)

        self.table.tag_configure("SOLD", background="#ffb3b3")
        self.table.tag_configure("AVAILABLE", background="#c2f0c2")

        self.table.bind("<<TreeviewSelect>>", self.select_car)

        # --- دکمه‌های عملیات ---
        Button(self.win, text="ذخیره", command=self.save_click, width=34, height=2).place(x=20, y=330)
        Button(self.win, text="ویرایش", command=self.edit_click, width=15, height=2).place(x=20, y=385)
        Button(self.win, text="حذف", command=self.delete_click, width=15, height=2).place(x=160, y=385)
        Button(self.win, text="پاک‌کردن فرم", command=self.reset_form, width=34, height=1).place(x=20, y=440)
        Button(self.win, text="بازگشت به منوی اصلی", command=self.back_to_menu, width=34, height=2).place(x=20, y=485)

        self.reset_form()

        if isinstance(self.win, Tk):
            self.win.mainloop()

    def back_to_menu(self):
        self.win.destroy()
        if tk._default_root:
            tk._default_root.deiconify()
            tk._default_root.lift()
            tk._default_root.focus_force()

    def format_price_input(self, event=None):
        if event and event.keysym in ("Left", "Right", "Up", "Down", "Home", "End"):
            return
        current = self.price_txt.get()
        digits = "".join(ch for ch in current if ch.isdigit())
        if digits:
            formatted = f"{int(digits):,}"
            if formatted != current:
                self.price_txt.delete(0, END)
                self.price_txt.insert(0, formatted)
        elif current != "":
            self.price_txt.delete(0, END)

    def get_clean_price(self):
        return "".join(ch for ch in self.price_txt.get() if ch.isdigit())

    def save_click(self):
        code_str = self.code_txt.get().strip()

        # اگر سطری انتخاب شده و همان کد بدون تغییر مانده، عملیات ویرایش انجام می‌شود
        if self.selected_code is not None and code_str == str(self.selected_code):
            self.edit_click()
            return

        status, message = self.controller.save(
            code_str if code_str else None,
            self.brand_txt.get().strip(),
            self.model_txt.get().strip(),
            self.color_txt.get().strip(),
            self.year_txt.get().strip(),
            self.get_clean_price(),
            bool(self.sold_var.get() == 1)
        )
        if status:
            msg.showinfo("موفقیت", message, parent=self.win)
            self.reset_form()
        else:
            msg.showerror("خطا در ثبت", message, parent=self.win)

    def edit_click(self):
        code_str = self.code_txt.get().strip()
        if not code_str:
            msg.showwarning("هشدار", "کد خودرو مشخص نشده است.", parent=self.win)
            return

        target_code = self.selected_code if self.selected_code is not None else code_str

        status, message = self.controller.edit(
            code_str,
            self.brand_txt.get().strip(),
            self.model_txt.get().strip(),
            self.color_txt.get().strip(),
            self.year_txt.get().strip(),
            self.get_clean_price(),
            bool(self.sold_var.get() == 1),
            original_code=target_code
        )
        if status:
            msg.showinfo("موفقیت", message, parent=self.win)
            self.reset_form()
        else:
            msg.showerror("خطا در ویرایش", message, parent=self.win)

    def delete_click(self):
        code = self.code_txt.get().strip()
        if not code:
            msg.showwarning("هشدار", "ابتدا یک خودرو را از جدول انتخاب کنید یا کد آن را بنویسید.", parent=self.win)
            return

        status, message = self.controller.delete(int(code))
        if status:
            msg.showinfo("موفقیت", message, parent=self.win)
            self.reset_form()
        else:
            msg.showerror("خطا در حذف", message, parent=self.win)

    def show_data_on_table(self, status, car_list):
        for item in self.table.get_children():
            self.table.delete(item)

        if status and car_list:
            for car in car_list:
                is_sold = bool(car.sold) or str(car.sold).strip() in ("1", "True", "بله")
                status_text = "فروخته شده" if is_sold else "موجود"
                row_tag = "SOLD" if is_sold else "AVAILABLE"

                digits = "".join(ch for ch in str(car.price) if ch.isdigit())
                formatted_price = f"{int(digits):,} تومان" if digits else "-"

                row_vals = (car.code, car.brand, car.model, car.color, car.year, formatted_price, status_text)
                self.table.insert("", END, values=row_vals, tags=(row_tag,))
        elif not status:
            msg.showerror("خطا", "خطا در دریافت لیست خودروها.", parent=self.win)

    def reset_form(self):
        self.code_txt.delete(0, END)
        self.selected_code = None

        self.brand_txt.delete(0, END)
        self.model_txt.delete(0, END)
        self.color_txt.delete(0, END)
        self.year_txt.delete(0, END)
        self.price_txt.delete(0, END)
        self.sold_var.set(0)

        if self.table.selection():
            self.table.selection_remove(self.table.selection())

        status, car_list = self.controller.find_all()
        self.show_data_on_table(status, car_list)

    def search_brand_model(self, event=None):
        status, car_list = self.controller.find_by_brand_model(
            self.search_brand_txt.get().strip(),
            self.search_model_txt.get().strip()
        )
        self.show_data_on_table(status, car_list)

    def select_car(self, event=None):
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0]).get("values")
        if not values:
            return

        self.code_txt.delete(0, END)
        self.code_txt.insert(0, str(values[0]))
        self.selected_code = str(values[0])

        self.brand_txt.delete(0, END)
        self.brand_txt.insert(0, str(values[1]))

        self.model_txt.delete(0, END)
        self.model_txt.insert(0, str(values[2]))

        self.color_txt.delete(0, END)
        self.color_txt.insert(0, str(values[3]))

        self.year_txt.delete(0, END)
        self.year_txt.insert(0, str(values[4]))

        digits = "".join(ch for ch in str(values[5]) if ch.isdigit())
        self.price_txt.delete(0, END)
        if digits:
            self.price_txt.insert(0, f"{int(digits):,}")

        self.sold_var.set(1 if str(values[6]).strip() == "فروخته شده" else 0)