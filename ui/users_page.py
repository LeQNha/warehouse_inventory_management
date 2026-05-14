import tkinter as tk
from tkinter import messagebox
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, make_table, page_header

class UsersPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()
        self.load_data()

    def _build(self):
        page_header(self, "👥  Quản lý tài khoản", "Quản lý người dùng hệ thống")

        # Warning for non-admin
        if self.current_user["role"] != "admin":
            tk.Label(self, text="⚠️  Chỉ Admin mới có thể quản lý tài khoản",
                     font=FONTS["body"], bg=COLORS["bg_dark"],
                     fg=COLORS["accent_orange"]).pack(pady=20)
            return

        toolbar = tk.Frame(self, bg=COLORS["bg_dark"])
        toolbar.pack(fill="x", pady=(0, 12))
        PrimaryButton(toolbar, "Thêm tài khoản", command=self.open_add, icon="➕").pack(side="left", padx=(0, 6))
        SecondaryButton(toolbar, "Đổi mật khẩu", command=self.change_password, icon="🔑").pack(side="left")

        cols = ("ID", "Tên đăng nhập", "Họ tên", "Vai trò", "Ngày tạo")
        self.tree = make_table(self, cols)
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Tên đăng nhập", width=160)
        self.tree.column("Họ tên", width=200)
        self.tree.column("Vai trò", width=100, anchor="center")
        self.tree.column("Ngày tạo", width=140, anchor="center")
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.bind("<Double-1>", lambda e: self.open_edit())

        # Role tags
        self.tree.tag_configure("admin_row", background="#1A2A1A", foreground=COLORS["accent"])
        self.tree.tag_configure("staff_row", background=COLORS["table_bg"], foreground=COLORS["text_primary"])

        action_bar = tk.Frame(self, bg=COLORS["bg_dark"])
        action_bar.pack(fill="x", pady=(8, 0))
        SecondaryButton(action_bar, "Chỉnh sửa", command=self.open_edit, icon="✏️").pack(side="left", padx=(0, 6))
        DangerButton(action_bar, "Xóa tài khoản", command=self.delete_user, icon="🗑️").pack(side="left")

    def load_data(self):
        a = 1

    def _selected_id(self):
        a = 1

    def open_add(self):
        a = 1

    def open_edit(self):
        a = 1

    def change_password(self):
        a = 1

    def delete_user(self):
        a = 1
