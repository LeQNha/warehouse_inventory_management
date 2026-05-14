
import tkinter as tk
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, SearchBar, make_table, page_header


class CategoriesPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()

    def _build(self):
        page_header(self, "🏷️  Quản lý danh mục", "Phân loại sản phẩm theo danh mục")

        toolbar = tk.Frame(self, bg=COLORS["bg_dark"])
        toolbar.pack(fill="x", pady=(0, 12))
        self.search_bar = SearchBar(toolbar, on_search=self.search, placeholder="Tìm danh mục...")
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(0, 12))
        PrimaryButton(toolbar, "Thêm danh mục", command=self.open_add, icon="➕").pack(side="left")

        cols = ("ID", "Tên danh mục", "Mô tả", "Số sản phẩm", "Ngày tạo")
        self.tree = make_table(self, cols)
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Tên danh mục", width=200)
        self.tree.column("Mô tả", width=280)
        self.tree.column("Số sản phẩm", width=100, anchor="center")
        self.tree.column("Ngày tạo", width=140, anchor="center")
        for col in cols:
            self.tree.heading(col, text=col)
        self.tree.bind("<Double-1>", lambda e: self.open_edit())

        action_bar = tk.Frame(self, bg=COLORS["bg_dark"])
        action_bar.pack(fill="x", pady=(8, 0))
        SecondaryButton(action_bar, "Chỉnh sửa", command=self.open_edit, icon="✏️").pack(side="left", padx=(0, 6))
        DangerButton(action_bar, "Xóa", command=self.delete_item, icon="🗑️").pack(side="left")

    def load_data(self, q=""):
        a = 1
    def search(self, q):
        a = 1
    def _selected_id(self):
        a = 1
    def open_add(self):
        a = 1
    def open_edit(self):
        a = 1
    def delete_item(self):
        a = 1

    
class SuppliersPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()

    def _build(self):
        page_header(self, "🏭  Quản lý nhà cung cấp", "Thông tin và liên hệ nhà cung cấp")

        toolbar = tk.Frame(self, bg=COLORS["bg_dark"])
        toolbar.pack(fill="x", pady=(0, 12))
        self.search_bar = SearchBar(toolbar, on_search=self.search, placeholder="Tìm nhà cung cấp...")
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(0, 12))
        PrimaryButton(toolbar, "Thêm nhà cung cấp", command=self.open_add, icon="➕").pack(side="left")

        cols = ("ID", "Tên nhà cung cấp", "SĐT", "Email", "Địa chỉ", "Số SP", "Ngày tạo")
        self.tree = make_table(self, cols)
        widths = [50, 200, 120, 180, 180, 70, 120]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Tên nhà cung cấp", anchor="w")
        self.tree.column("Email", anchor="w")
        self.tree.column("Địa chỉ", anchor="w")
        self.tree.bind("<Double-1>", lambda e: self.open_edit())

        action_bar = tk.Frame(self, bg=COLORS["bg_dark"])
        action_bar.pack(fill="x", pady=(8, 0))
        SecondaryButton(action_bar, "Chỉnh sửa", command=self.open_edit, icon="✏️").pack(side="left", padx=(0, 6))
        DangerButton(action_bar, "Xóa", command=self.delete_item, icon="🗑️").pack(side="left")

    def load_data(self, q=""):
        a = 1

    def search(self, q):
        a = 1

    def _selected_id(self):
        a = 1

    def open_add(self):
        a = 1

    def open_edit(self):
        a = 1

    def delete_item(self):
        a = 1
        
    