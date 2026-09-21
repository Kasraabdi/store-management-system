import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg

from controller.house_controller import HouseController


class HouseView:
    def __init__(self):
        self.controller = HouseController()
        self.selected_code = None

        if tk._default_root:
            self.win = Toplevel()
            self.win.transient(tk._default_root)
        else:
            self.win = Tk()

        self.win.title("مدیریت املاک")

        try:
            self.win.state("zoomed")
        except Exception:
            self.win.attributes("-fullscreen", True)

        self.win.focus_force()

        # --- ویجت‌های فرم ---
        Label(self.win, text="کد").place(x=20, y=20)
        self.code_txt = Entry(self.win, width=23)
        self.code_txt.place(x=110, y=20)

        Label(self.win, text="نوع ملک").place(x=20, y=58)
        self.type_txt = Entry(self.win, width=23)
        self.type_txt.place(x=110, y=58)

        Label(self.win, text="متراژ").place(x=20, y=96)
        self.meterage_txt = Entry(self.win, width=23)
        self.meterage_txt.place(x=110, y=96)

        Label(self.win, text="تعداد اتاق").place(x=20, y=134)
        self.rooms_txt = Entry(self.win, width=23)
        self.rooms_txt.place(x=110, y=134)

        Label(self.win, text="آدرس").place(x=20, y=172)
        self.address_txt = Entry(self.win, width=23)
        self.address_txt.place(x=110, y=172)

        Label(self.win, text="قیمت").place(x=20, y=210)
        self.price_txt = Entry(self.win, width=23)
        self.price_txt.bind("<KeyRelease>", self.format_price_input)
        self.price_txt.place(x=110, y=210)

        # --- تفکیک بخش امکانات ملک ---
        Label(self.win, text="امکانات:").place(x=20, y=248)
        self.parking_var = IntVar(master=self.win, value=0)
        Checkbutton(self.win, text="پارکینگ", variable=self.parking_var, onvalue=1, offvalue=0).place(x=95, y=248)

        self.elevator_var = IntVar(master=self.win, value=0)
        Checkbutton(self.win, text="آسانسور", variable=self.elevator_var, onvalue=1, offvalue=0).place(x=160, y=248)

        self.storage_var = IntVar(master=self.win, value=0)
        Checkbutton(self.win, text="انباری", variable=self.storage_var, onvalue=1, offvalue=0).place(x=225, y=248)

        # --- بخش وضعیت فروش (کاملاً مجزا) ---
        Label(self.win, text="وضعیت فروش:").place(x=20, y=285)
        self.sold_var = IntVar(master=self.win, value=0)
        Checkbutton(self.win, text="فروخته شده", variable=self.sold_var, onvalue=1, offvalue=0).place(x=110, y=285)

        # --- بخش جستجو ---
        Label(self.win, text="جستجو با نوع ملک").place(x=300, y=20)
        self.search_type_txt = Entry(self.win, width=18)
        self.search_type_txt.bind("<KeyRelease>", self.search_type_address)
        self.search_type_txt.place(x=410, y=20)

        Label(self.win, text="جستجو با آدرس").place(x=550, y=20)
        self.search_address_txt = Entry(self.win, width=18)
        self.search_address_txt.bind("<KeyRelease>", self.search_type_address)
        self.search_address_txt.place(x=640, y=20)

        # --- جدول اطلاعات ---
        table_frame = Frame(self.win)
        table_frame.place(x=300, y=70, relwidth=0.65, relheight=0.82)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        columns = ("code", "house_type", "meterage", "rooms", "parking", "elevator", "storage", "price", "sold", "address")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.table.yview)
        self.table.pack(fill=BOTH, expand=True)

        self.table.heading("code", text="کد")
        self.table.heading("house_type", text="نوع ملک")
        self.table.heading("meterage", text="متراژ")
        self.table.heading("rooms", text="اتاق")
        self.table.heading("parking", text="پارکینگ")
        self.table.heading("elevator", text="آسانسور")
        self.table.heading("storage", text="انباری")
        self.table.heading("price", text="قیمت")
        self.table.heading("sold", text="وضعیت")
        self.table.heading("address", text="آدرس")

        self.table.column("code", width=45, anchor=CENTER)
        self.table.column("house_type", width=90, anchor=CENTER)
        self.table.column("meterage", width=60, anchor=CENTER)
        self.table.column("rooms", width=50, anchor=CENTER)
        self.table.column("parking", width=60, anchor=CENTER)
        self.table.column("elevator", width=60, anchor=CENTER)
        self.table.column("storage", width=60, anchor=CENTER)
        self.table.column("price", width=125, anchor=CENTER)
        self.table.column("sold", width=75, anchor=CENTER)
        self.table.column("address", width=140, anchor=CENTER)

        self.table.tag_configure("SOLD", background="#ffb3b3")
        self.table.tag_configure("AVAILABLE", background="#c2f0c2")

        self.table.bind("<<TreeviewSelect>>", self.select_house)

        # --- دکمه‌های عملیات ---
        Button(self.win, text="ذخیره", command=self.save_click, width=34, height=2).place(x=20, y=325)
        Button(self.win, text="ویرایش", command=self.edit_click, width=15, height=2).place(x=20, y=380)
        Button(self.win, text="حذف", command=self.delete_click, width=15, height=2).place(x=160, y=380)
        Button(self.win, text="پاک‌کردن فرم", command=self.reset_form, width=34, height=1).place(x=20, y=435)
        Button(self.win, text="بازگشت به منوی اصلی", command=self.back_to_menu, width=34, height=2).place(x=20, y=480)

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

        if self.selected_code is not None and code_str == str(self.selected_code):
            self.edit_click()
            return

        status, message = self.controller.save(
            code_str if code_str else None,
            self.type_txt.get().strip(),
            self.meterage_txt.get().strip(),
            self.rooms_txt.get().strip(),
            bool(self.parking_var.get() == 1),
            bool(self.elevator_var.get() == 1),
            bool(self.storage_var.get() == 1),
            self.address_txt.get().strip(),
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
            msg.showwarning("هشدار", "کد ملک مشخص نشده است.", parent=self.win)
            return

        target_code = self.selected_code if self.selected_code is not None else code_str

        status, message = self.controller.edit(
            code_str,
            self.type_txt.get().strip(),
            self.meterage_txt.get().strip(),
            self.rooms_txt.get().strip(),
            bool(self.parking_var.get() == 1),
            bool(self.elevator_var.get() == 1),
            bool(self.storage_var.get() == 1),
            self.address_txt.get().strip(),
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
            msg.showwarning("هشدار", "ابتدا یک ملک را از جدول انتخاب کنید یا کد آن را بنویسید.", parent=self.win)
            return

        status, message = self.controller.delete(int(code))
        if status:
            msg.showinfo("موفقیت", message, parent=self.win)
            self.reset_form()
        else:
            msg.showerror("خطا در حذف", message, parent=self.win)

    def show_data_on_table(self, status, house_list):
        for item in self.table.get_children():
            self.table.delete(item)

        if status and house_list:
            for h in house_list:
                is_sold = bool(h.sold) or str(h.sold).strip() in ("1", "True", "بله")
                status_text = "فروخته شده" if is_sold else "موجود"
                row_tag = "SOLD" if is_sold else "AVAILABLE"

                digits = "".join(ch for ch in str(h.price) if ch.isdigit())
                formatted_price = f"{int(digits):,} تومان" if digits else "-"

                row_vals = (
                    h.code,
                    h.house_type,
                    h.meterage,
                    h.rooms,
                    "دارد" if h.parking else "ندارد",
                    "دارد" if h.elevator else "ندارد",
                    "دارد" if h.storage else "ندارد",
                    formatted_price,
                    status_text,
                    h.address
                )
                self.table.insert("", END, values=row_vals, tags=(row_tag,))
        elif not status:
            msg.showerror("خطا", "خطا در دریافت لیست املاک.", parent=self.win)

    def reset_form(self):
        self.code_txt.delete(0, END)
        self.selected_code = None

        self.type_txt.delete(0, END)
        self.meterage_txt.delete(0, END)
        self.rooms_txt.delete(0, END)
        self.address_txt.delete(0, END)
        self.price_txt.delete(0, END)

        self.parking_var.set(0)
        self.elevator_var.set(0)
        self.storage_var.set(0)
        self.sold_var.set(0)

        if self.table.selection():
            self.table.selection_remove(self.table.selection())

        status, house_list = self.controller.find_all()
        self.show_data_on_table(status, house_list)

    def search_type_address(self, event=None):
        status, house_list = self.controller.find_by_type_address(
            self.search_type_txt.get().strip(),
            self.search_address_txt.get().strip()
        )
        self.show_data_on_table(status, house_list)

    def select_house(self, event=None):
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0]).get("values")
        if not values:
            return

        self.code_txt.delete(0, END)
        self.code_txt.insert(0, str(values[0]))
        self.selected_code = str(values[0])

        self.type_txt.delete(0, END)
        self.type_txt.insert(0, str(values[1]))

        self.meterage_txt.delete(0, END)
        self.meterage_txt.insert(0, str(values[2]))

        self.rooms_txt.delete(0, END)
        self.rooms_txt.insert(0, str(values[3]))

        self.parking_var.set(1 if str(values[4]).strip() == "دارد" else 0)
        self.elevator_var.set(1 if str(values[5]).strip() == "دارد" else 0)
        self.storage_var.set(1 if str(values[6]).strip() == "دارد" else 0)

        digits = "".join(ch for ch in str(values[7]) if ch.isdigit())
        self.price_txt.delete(0, END)
        if digits:
            self.price_txt.insert(0, f"{int(digits):,}")

        self.sold_var.set(1 if str(values[8]).strip() == "فروخته شده" else 0)

        self.address_txt.delete(0, END)
        self.address_txt.insert(0, str(values[9]))