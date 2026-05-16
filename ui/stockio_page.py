import tkinter as tk
from tkinter import ttk, messagebox
from theme import COLORS, FONTS
from widgets import PrimaryButton, make_table, page_header
from database import get_connection


def _labeled_entry(parent, label, var):
    """Label + Entry xếp dọc, không gọi .pack() bên ngoài."""
    tk.Label(parent, text=label, font=FONTS["body_bold"],
             bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
    holder = tk.Frame(parent, bg=COLORS["bg_input"],
                      highlightthickness=1, highlightbackground=COLORS["border"])
    holder.pack(fill="x")
    e = tk.Entry(holder, textvariable=var,
                 bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["text_primary"],
                 relief="flat", bd=0, font=FONTS["body"])
    e.pack(fill="x", ipady=8, padx=10)
    e.bind("<FocusIn>",  lambda ev: holder.config(highlightbackground=COLORS["border_focus"]))
    e.bind("<FocusOut>", lambda ev: holder.config(highlightbackground=COLORS["border"]))
    return e


def _form_panel(body, title, width=360):
    """Tạo left panel (card trắng) và trả về frame bên trong để đặt widget."""
    outer = tk.Frame(body, bg=COLORS["bg_card"],
                     highlightthickness=1, highlightbackground=COLORS["border"],
                     width=width)
    outer.pack(side="left", fill="y", padx=(0, 12))
    outer.pack_propagate(False)          # giữ cố định width

    tk.Label(outer, text=title, font=FONTS["heading_sm"],
             bg=COLORS["bg_card"], fg=COLORS["text_white"]).pack(anchor="w", padx=16, pady=(14, 4))
    tk.Frame(outer, bg=COLORS["border"], height=1).pack(fill="x", padx=16, pady=(0, 4))

    inner = tk.Frame(outer, bg=COLORS["bg_card"])
    inner.pack(fill="x", padx=16, pady=4)
    return inner


def _history_panel(body, title):
    """Tạo right panel cho bảng lịch sử."""
    right = tk.Frame(body, bg=COLORS["bg_dark"])
    right.pack(side="left", fill="both", expand=True)
    tk.Label(right, text=title, font=FONTS["heading_sm"],
             bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(anchor="w", pady=(0, 8))
    return right


class StockInPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self.products  = {}
        self.suppliers = {}
        self._build()

    def _load_refs(self):
        a = 1

    def _build(self):
        page_header(self, "📥  Nhập kho", "Ghi nhận hàng hóa nhập vào kho")

        body = tk.Frame(self, bg=COLORS["bg_dark"])
        body.pack(fill="both", expand=True)

        # left form
        f = _form_panel(body, "📝  Phiếu nhập kho")

        # sản phẩm
        tk.Label(f, text="Sản phẩm *", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(0, 2))
        self.v_product = tk.StringVar()
        self.product_combo = ttk.Combobox(f, textvariable=self.v_product,
                                          values=list(self.products.keys()),
                                          state="readonly", font=FONTS["body"])
        self.product_combo.pack(fill="x", ipady=4)
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)

        self.stock_info = tk.Label(f, text="Chọn sản phẩm để xem tồn kho",
                                   font=FONTS["small"], bg=COLORS["bg_card"],
                                   fg=COLORS["text_muted"])
        self.stock_info.pack(anchor="w", pady=(4, 0))

        # fields
        self.v_qty   = tk.StringVar(value="1")
        self.v_price = tk.StringVar(value="0")
        self.v_note  = tk.StringVar()
        self.v_sup   = tk.StringVar()

        _labeled_entry(f, "Số lượng nhập *", self.v_qty)
        _labeled_entry(f, "Giá nhập (VNĐ)",   self.v_price)

        tk.Label(f, text="Nhà cung cấp", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
        ttk.Combobox(f, textvariable=self.v_sup,
                     values=list(self.suppliers.keys()),
                     state="readonly", font=FONTS["body"]).pack(fill="x", ipady=4)

        _labeled_entry(f, "Ghi chú", self.v_note)

        # tổng giá trị
        tk.Frame(f, bg=COLORS["border"], height=1).pack(fill="x", pady=(12, 8))
        tot = tk.Frame(f, bg=COLORS["bg_card"])
        tot.pack(fill="x")
        tk.Label(tot, text="Tổng giá trị:", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(side="left")
        self.total_label = tk.Label(tot, text="0 VNĐ", font=FONTS["heading_sm"],
                                    bg=COLORS["bg_card"], fg=COLORS["accent_yellow"])
        self.total_label.pack(side="right")

        self.v_qty.trace_add("write",   self._update_total)
        self.v_price.trace_add("write", self._update_total)

        PrimaryButton(f, "✅  Xác nhận nhập kho", command=self._submit).pack(
            fill="x", pady=(14, 4))

        # right history
        right = _history_panel(body, "📋  Lịch sử nhập kho")

        cols = ("ID", "Sản phẩm", "SL", "Giá nhập", "Nhà cung cấp", "Ghi chú", "Ngày nhập")
        self.tree = make_table(right, cols)
        for col, w, anch in [
            ("ID", 50, "center"), ("Sản phẩm", 180, "w"),
            ("SL", 60, "center"), ("Giá nhập", 110, "e"),
            ("Nhà cung cấp", 130, "w"), ("Ghi chú", 110, "w"),
            ("Ngày nhập", 150, "center"),
        ]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=anch)

    def _on_product_select(self, _=None):
       a = 1

    def _update_total(self, *_):
        a = 1

    def _submit(self):
        a = 1

    def load_history(self):
        a = 1


class StockOutPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self.products = {}
        self._build()


    def _build(self):
        page_header(self, "📤  Xuất kho", "Ghi nhận hàng hóa xuất ra khỏi kho")

        body = tk.Frame(self, bg=COLORS["bg_dark"])
        body.pack(fill="both", expand=True)

        # ── left form ────────────────────────────────────────
        f = _form_panel(body, "📝  Phiếu xuất kho")

        tk.Label(f, text="Sản phẩm *", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(0, 2))
        self.v_product = tk.StringVar()
        self.product_combo = ttk.Combobox(f, textvariable=self.v_product,
                                          values=list(self.products.keys()),
                                          state="readonly", font=FONTS["body"])
        self.product_combo.pack(fill="x", ipady=4)
        self.product_combo.bind("<<ComboboxSelected>>", self._on_product_select)

        self.stock_info = tk.Label(f, text="Chọn sản phẩm để xem tồn kho",
                                   font=FONTS["small"], bg=COLORS["bg_card"],
                                   fg=COLORS["text_muted"])
        self.stock_info.pack(anchor="w", pady=(4, 0))

        self.v_qty      = tk.StringVar(value="1")
        self.v_price    = tk.StringVar(value="0")
        self.v_customer = tk.StringVar()
        self.v_note     = tk.StringVar()

        _labeled_entry(f, "Số lượng xuất *", self.v_qty)
        _labeled_entry(f, "Giá bán (VNĐ)",   self.v_price)
        _labeled_entry(f, "Khách hàng",       self.v_customer)
        _labeled_entry(f, "Ghi chú",          self.v_note)

        tk.Frame(f, bg=COLORS["border"], height=1).pack(fill="x", pady=(12, 8))
        tot = tk.Frame(f, bg=COLORS["bg_card"])
        tot.pack(fill="x")
        tk.Label(tot, text="Tổng doanh thu:", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(side="left")
        self.total_label = tk.Label(tot, text="0 VNĐ", font=FONTS["heading_sm"],
                                    bg=COLORS["bg_card"], fg=COLORS["accent"])
        self.total_label.pack(side="right")

        self.v_qty.trace_add("write",   self._update_total)
        self.v_price.trace_add("write", self._update_total)

        PrimaryButton(f, "✅  Xác nhận xuất kho", command=self._submit,
                      color=COLORS["accent_purple"]).pack(fill="x", pady=(14, 4))

        # right history
        right = _history_panel(body, "📋  Lịch sử xuất kho")

        cols = ("ID", "Sản phẩm", "SL", "Giá bán", "Khách hàng", "Ghi chú", "Ngày xuất")
        self.tree = make_table(right, cols)
        for col, w, anch in [
            ("ID", 50, "center"), ("Sản phẩm", 180, "w"),
            ("SL", 60, "center"), ("Giá bán", 110, "e"),
            ("Khách hàng", 130, "w"), ("Ghi chú", 110, "w"),
            ("Ngày xuất", 150, "center"),
        ]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=anch)

    def _on_product_select(self, _=None):
       a = 1

    def _update_total(self, *_):
        a = 1

    def _submit(self):
        a = 1

    def load_history(self):
        a = 1
