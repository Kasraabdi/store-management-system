import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg

from controller.customer_controller import CustomerController


class CustomerView:
    def __init__(self):
        self.controller = CustomerController()
        self.selected_code = None

        if tk._default_root:
            self.win = Toplevel()
            self.win.transient(tk._default_root)
        else:
            self.win = Tk()

        self.win.title("مدیریت مشتریان")

        try:
            self.win.state("zoomed")
        except Exception:
            self.win.attributes("-fullscreen", True)

        self.win.focus_force()

        # --- ویجت‌های فرم ---
        Label(self.win, text="کد").place(x=20, y=20)
        self.code_txt = Entry(self.win, width=23)
        self.code_txt.place(x=120, y=20)

        Label(self.win, text="نام").place(x=20, y=65)
        self.name_txt = Entry(self.win, width=23)
        self.name_txt.place(x=120, y=65)

        Label(self.win, text="نام خانوادگی").place(x=20, y=110)
        self.family_txt = Entry(self.win, width=23)
        self.family_txt.place(x=120, y=110)

        Label(self.win, text="نام کاربری").place(x=20, y=155)
        self.username_txt = Entry(self.win, width=23)
        self.username_txt.place(x=120, y=155)

        Label(self.win, text="رمز عبور").place(x=20, y=200)
        self.password_txt = Entry(self.win, width=23, show="*")
        self.password_txt.place(x=120, y=200)

        Label(self.win, text="شماره تماس").place(x=20, y=245)
        self.phone_txt = Entry(self.win, width=23)
        self.phone_txt.place(x=120, y=245)

        # فقط مربع تیک بدون متن تکراری
        Label(self.win, text="مسدود").place(x=20, y=290)
        self.locked_var = IntVar(master=self.win, value=0)
        self.chk_locked = Checkbutton(
            self.win,
            text="",
            variable=self.locked_var,
            onvalue=1,
            offvalue=0
        )
        self.chk_locked.place(x=120, y=290)

        # --- بخش جستجو ---
        Label(self.win, text="جستجو با نام").place(x=300, y=20)
        self.search_name_txt = Entry(self.win, width=18)
        self.search_name_txt.bind("<KeyRelease>", self.search_name_family)
        self.search_name_txt.place(x=380, y=20)

        Label(self.win, text="جستجو با نام خانوادگی").place(x=530, y=20)
        self.search_family_txt = Entry(self.win, width=18)
        self.search_family_txt.bind("<KeyRelease>", self.search_name_family)
        self.search_family_txt.place(x=660, y=20)

        # --- جدول اطلاعات ---
        table_frame = Frame(self.win)
        table_frame.place(x=300, y=70, relwidth=0.65, relheight=0.82)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        columns = ("code", "name", "family", "username", "password", "phone", "locked")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.table.yview)
        self.table.pack(fill=BOTH, expand=True)

        self.table.heading("code", text="کد")
        self.table.heading("name", text="نام")
        self.table.heading("family", text="نام خانوادگی")
        self.table.heading("username", text="نام کاربری")
        self.table.heading("password", text="رمز عبور")
        self.table.heading("phone", text="شماره تماس")
        self.table.heading("locked", text="مسدود")

        self.table.column("code", width=50, anchor=CENTER)
        self.table.column("name", width=100, anchor=CENTER)
        self.table.column("family", width=110, anchor=CENTER)
        self.table.column("username", width=100, anchor=CENTER)
        self.table.column("password", width=100, anchor=CENTER)
        self.table.column("phone", width=110, anchor=CENTER)
        self.table.column("locked", width=60, anchor=CENTER)

        self.table.tag_configure("LOCKED", background="#ffb3b3")
        self.table.tag_configure("ACTIVE", background="#c2f0c2")

        self.table.bind("<<TreeviewSelect>>", self.select_customer)

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

    def save_click(self):
        code_str = self.code_txt.get().strip()

        if self.selected_code is not None and code_str == str(self.selected_code):
            self.edit_click()
            return

        status, message = self.controller.save(
            code_str if code_str else None,
            self.name_txt.get().strip(),
            self.family_txt.get().strip(),
            self.username_txt.get().strip(),
            self.password_txt.get().strip(),
            self.phone_txt.get().strip(),
            bool(self.locked_var.get() == 1)
        )
        if status:
            msg.showinfo("موفقیت", message, parent=self.win)
            self.reset_form()
        else:
            msg.showerror("خطا در ثبت", message, parent=self.win)

    def edit_click(self):
        code_str = self.code_txt.get().strip()
        if not code_str:
            msg.showwarning("هشدار", "کد مشتری مشخص نشده است.", parent=self.win)
            return

        target_code = self.selected_code if self.selected_code is not None else code_str

        status, message = self.controller.edit(
            code_str,
            self.name_txt.get().strip(),
            self.family_txt.get().strip(),
            self.username_txt.get().strip(),
            self.password_txt.get().strip(),
            self.phone_txt.get().strip(),
            bool(self.locked_var.get() == 1),
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
            msg.showwarning("هشدار", "ابتدا یک مشتری را از جدول انتخاب کنید یا کد آن را بنویسید.", parent=self.win)
            return

        status, message = self.controller.delete(int(code))
        if status:
            msg.showinfo("موفقیت", message, parent=self.win)
            self.reset_form()
        else:
            msg.showerror("خطا در حذف", message, parent=self.win)

    def show_data_on_table(self, status, customer_list):
        for item in self.table.get_children():
            self.table.delete(item)

        if status and customer_list:
            for c in customer_list:
                is_locked = bool(c.locked) or str(c.locked).strip() in ("1", "True", "بله")
                status_text = "بله" if is_locked else "خیر"
                row_tag = "LOCKED" if is_locked else "ACTIVE"

                row_vals = (
                    c.code,
                    c.name,
                    c.family,
                    c.username,
                    c.password,
                    c.phone_number,
                    status_text
                )
                self.table.insert("", END, values=row_vals, tags=(row_tag,))
        elif not status:
            msg.showerror("خطا", "خطا در دریافت لیست مشتریان.", parent=self.win)

    def reset_form(self):
        self.code_txt.delete(0, END)
        self.selected_code = None

        self.name_txt.delete(0, END)
        self.family_txt.delete(0, END)
        self.username_txt.delete(0, END)
        self.password_txt.delete(0, END)

        self.phone_txt.delete(0, END)
        self.phone_txt.insert(0, "09")

        self.locked_var.set(0)

        if self.table.selection():
            self.table.selection_remove(self.table.selection())

        status, customer_list = self.controller.find_all()
        self.show_data_on_table(status, customer_list)

    def search_name_family(self, event=None):
        status, customer_list = self.controller.find_by_name_family(
            self.search_name_txt.get().strip(),
            self.search_family_txt.get().strip()
        )
        self.show_data_on_table(status, customer_list)

    def select_customer(self, event=None):
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0]).get("values")
        if not values:
            return

        self.code_txt.delete(0, END)
        self.code_txt.insert(0, str(values[0]))
        self.selected_code = str(values[0])

        self.name_txt.delete(0, END)
        self.name_txt.insert(0, str(values[1]))

        self.family_txt.delete(0, END)
        self.family_txt.insert(0, str(values[2]))

        self.username_txt.delete(0, END)
        self.username_txt.insert(0, str(values[3]))

        self.password_txt.delete(0, END)
        self.password_txt.insert(0, str(values[4]))

        self.phone_txt.delete(0, END)
        self.phone_txt.insert(0, str(values[5]))

        val_locked = str(values[6]).strip()
        if val_locked in ("بله", "1", "True"):
            self.locked_var.set(1)
        else:
            self.locked_var.set(0)