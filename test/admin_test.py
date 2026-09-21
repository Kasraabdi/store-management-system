from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg

from controller.admin_controller import AdminController


class AdminView:
    def __init__(self):
        self.controller = AdminController()
        self.win = Tk()
        self.win.title("مدیریت مدیران")
        self.win.geometry("950x580")

        Label(self.win, text="کد").place(x=20, y=20)
        self.code_txt = Entry(self.win, width=23, state="readonly")
        self.code_txt.place(x=120, y=20)

        Label(self.win, text="نام").place(x=20, y=70)
        self.name_txt = Entry(self.win, width=23)
        self.name_txt.place(x=120, y=70)

        Label(self.win, text="نام خانوادگی").place(x=20, y=120)
        self.family_txt = Entry(self.win, width=23)
        self.family_txt.place(x=120, y=120)

        Label(self.win, text="نام کاربری").place(x=20, y=170)
        self.username_txt = Entry(self.win, width=23)
        self.username_txt.place(x=120, y=170)

        Label(self.win, text="رمز عبور").place(x=20, y=220)
        self.password_txt = Entry(self.win, width=23, show="*")
        self.password_txt.place(x=120, y=220)

        Label(self.win, text="مسدود").place(x=20, y=270)
        self.locked_var = BooleanVar(value=False)
        Checkbutton(self.win, text="مسدود شده", variable=self.locked_var).place(x=120, y=270)

        Label(self.win, text="جستجو با نام").place(x=300, y=20)
        self.search_name_txt = Entry(self.win, width=18)
        self.search_name_txt.bind("<KeyRelease>", self.search_name_family)
        self.search_name_txt.place(x=380, y=20)

        Label(self.win, text="جستجو با نام خانوادگی").place(x=530, y=20)
        self.search_family_txt = Entry(self.win, width=18)
        self.search_family_txt.bind("<KeyRelease>", self.search_name_family)
        self.search_family_txt.place(x=660, y=20)

        table_frame = Frame(self.win)
        table_frame.place(x=300, y=70, width=620, height=450)

        scrollbar = Scrollbar(table_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        columns = ("code", "name", "family", "username", "password", "locked")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.table.yview)
        self.table.pack(fill=BOTH, expand=True)

        self.table.heading("code", text="کد")
        self.table.heading("name", text="نام")
        self.table.heading("family", text="نام خانوادگی")
        self.table.heading("username", text="نام کاربری")
        self.table.heading("password", text="رمز عبور")
        self.table.heading("locked", text="مسدود")

        self.table.column("code", width=50)
        self.table.column("name", width=100)
        self.table.column("family", width=110)
        self.table.column("username", width=100)
        self.table.column("password", width=100)
        self.table.column("locked", width=60)

        # تنظیم رنگ‌ها: قرمز برای افراد مسدود، سبز برای افراد فعال
        self.table.tag_configure("Locked", background="#ff9999", foreground="black")
        self.table.tag_configure("OK", background="lightgreen", foreground="black")

        self.table.bind("<ButtonRelease-1>", self.select_admin)

        Button(self.win, text="ذخیره", command=self.save_click, width=34, height=2).place(x=20, y=340)
        Button(self.win, text="ویرایش", command=self.edit_click, width=15, height=2).place(x=20, y=405)
        Button(self.win, text="حذف", command=self.delete_click, width=15, height=2).place(x=160, y=405)
        Button(self.win, text="پاک‌کردن فرم", command=self.reset_form, width=34, height=1).place(x=20, y=465)

        self.reset_form()
        self.win.mainloop()

    def save_click(self):
        name = self.name_txt.get().strip()
        family = self.family_txt.get().strip()
        username = self.username_txt.get().strip()
        password = self.password_txt.get().strip()
        locked = bool(self.locked_var.get())

        status, message = self.controller.save(name, family, username, password, locked)
        if status:
            msg.showinfo("موفقیت", message)
            self.reset_form()
        else:
            msg.showerror("خطا در ثبت", message)

    def edit_click(self):
        code = self.code_txt.get().strip()
        if not code:
            msg.showwarning("هشدار", "ابتدا یک مدیر را از جدول انتخاب کنید.")
            return

        status, message = self.controller.edit(
            int(code),
            self.name_txt.get().strip(),
            self.family_txt.get().strip(),
            self.username_txt.get().strip(),
            self.password_txt.get().strip(),
            bool(self.locked_var.get())
        )
        if status:
            msg.showinfo("موفقیت", message)
            self.reset_form()
        else:
            msg.showerror("خطا در ویرایش", message)

    def delete_click(self):
        code = self.code_txt.get().strip()
        if not code:
            msg.showwarning("هشدار", "ابتدا یک مدیر را از جدول انتخاب کنید.")
            return

        status, message = self.controller.delete(int(code))
        if status:
            msg.showinfo("موفقیت", message)
            self.reset_form()
        else:
            msg.showerror("خطا در حذف", message)

    def show_data_on_table(self, status, admin_list):
        for item in self.table.get_children():
            self.table.delete(item)

        if status and admin_list:
            for admin in admin_list:
                is_locked = bool(admin.locked)
                status_text = "بله" if is_locked else "خیر"
                row_tag = "Locked" if is_locked else "OK"

                row_vals = (
                    admin.code,
                    admin.name,
                    admin.family,
                    admin.username,
                    admin.password,
                    status_text
                )
                self.table.insert("", END, values=row_vals, tags=(row_tag,))
        elif not status:
            msg.showerror("خطا", "خطا در دریافت لیست اطلاعات مدیران.")

    def reset_form(self):
        self.code_txt.config(state="normal")
        self.code_txt.delete(0, END)
        self.code_txt.config(state="readonly")

        self.name_txt.delete(0, END)
        self.family_txt.delete(0, END)
        self.username_txt.delete(0, END)
        self.password_txt.delete(0, END)
        self.locked_var.set(False)

        status, admin_list = self.controller.find_all()
        self.show_data_on_table(status, admin_list)

    def search_name_family(self, event=None):
        status, admin_list = self.controller.find_by_name_family(
            self.search_name_txt.get().strip(),
            self.search_family_txt.get().strip()
        )
        self.show_data_on_table(status, admin_list)

    def select_admin(self, event=None):
        selected_item = self.table.focus()
        if not selected_item:
            return

        values = self.table.item(selected_item).get("values")
        if not values:
            return

        self.code_txt.config(state="normal")
        self.code_txt.delete(0, END)
        self.code_txt.insert(0, str(values[0]))
        self.code_txt.config(state="readonly")

        self.name_txt.delete(0, END)
        self.name_txt.insert(0, str(values[1]))

        self.family_txt.delete(0, END)
        self.family_txt.insert(0, str(values[2]))

        self.username_txt.delete(0, END)
        self.username_txt.insert(0, str(values[3]))

        self.password_txt.delete(0, END)
        self.password_txt.insert(0, str(values[4]))

        self.locked_var.set(True if values[5] == "بله" else False)