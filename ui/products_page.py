import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, SearchBar, make_table, page_header, Card

class ProductsPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()
    
    def _build(self):
        page_header(self, "📦  Quản lý sản phẩm", "Thêm, sửa, xóa và theo dõi sản phẩm trong kho")

        # Toolbar
        toolbar = tk.Frame(self, bg=COLORS["bg_dark"])
        toolbar.pack(fill="x", pady=(0, 12))

        self.search_bar = SearchBar(toolbar, on_search=self.search, placeholder="Tìm theo tên, mã sản phẩm...")
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(0, 12))

        PrimaryButton(toolbar, "Thêm sản phẩm", command=self.open_add, icon="➕").pack(side="left", padx=(0, 6))
        SecondaryButton(toolbar, "Làm mới", command=self.load_data, icon="🔄").pack(side="left")

        # Category filter
        filter_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        filter_frame.pack(fill="x", pady=(0, 10))

        tk.Label(filter_frame, text="Danh mục:", font=FONTS["body"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"]).pack(side="left", padx=(0, 8))
        self.cat_var = tk.StringVar(value="Tất cả")
        self.cat_combo = ttk.Combobox(filter_frame, textvariable=self.cat_var,
                                      state="readonly", width=20, font=FONTS["body"])
        self.cat_combo.pack(side="left", padx=(0, 8))
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self.load_data())
        self._refresh_categories()

        # Table
        cols = ("Mã SP", "Tên sản phẩm", "Danh mục", "Tồn kho", "Giá nhập", "Giá bán", "Nhà cung cấp", "Vị trí")
        self.tree = make_table(self, cols)
        widths = [90, 200, 120, 80, 100, 100, 150, 100]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Tên sản phẩm", anchor="w")

        # Right-click menu
        self.menu = tk.Menu(self, tearoff=0, bg=COLORS["bg_card"],
                            fg=COLORS["text_primary"], activebackground=COLORS["accent"],
                            activeforeground="white", bd=0, relief="flat", font=FONTS["body"])
        self.menu.add_command(label="✏️  Chỉnh sửa", command=self.open_edit)
        self.menu.add_command(label="🗑️  Xóa", command=self.delete_product)
        self.tree.bind("<Button-3>", self._show_menu)
        self.tree.bind("<Double-1>", lambda e: self.open_edit())

        # Bottom action bar
        action_bar = tk.Frame(self, bg=COLORS["bg_dark"])
        action_bar.pack(fill="x", pady=(8, 0))
        SecondaryButton(action_bar, "Chỉnh sửa", command=self.open_edit, icon="✏️").pack(side="left", padx=(0, 6))
        DangerButton(action_bar, "Xóa sản phẩm", command=self.delete_product, icon="🗑️").pack(side="left")

        self.status_label = tk.Label(action_bar, text="", font=FONTS["small"],
                                     bg=COLORS["bg_dark"], fg=COLORS["text_secondary"])
        self.status_label.pack(side="right")
    
    def _refresh_categories(self):
        a = 1 

    def load_data(self, query=""):
        a = 1

    def search(self, q):
        a = 1
    
    def _show_menu(self, event):
        a = 1
    
    def _selected_id(self):
        a = 1
    
    def open_add(self):
        a = 1
    
    def open_edit(self):
        a = 1
    
    def delete_product(self):
        a = 1
    

    