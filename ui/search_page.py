import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS
from widgets import PrimaryButton, SecondaryButton, make_table, page_header

class SearchPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()

    def _build(self):
        page_header(self, "🔍  Tìm kiếm", "Tìm kiếm nâng cao sản phẩm trong kho")

        # Filter panel
        filter_card = tk.Frame(self, bg=COLORS["bg_card"],
                               highlightthickness=1, highlightbackground=COLORS["border"])
        filter_card.pack(fill="x", pady=(0, 16))

        header = tk.Frame(filter_card, bg=COLORS["bg_card"])
        header.pack(fill="x", padx=16, pady=(12, 8))
        tk.Label(header, text="Bộ lọc tìm kiếm", font=FONTS["heading_sm"],
                 bg=COLORS["bg_card"], fg=COLORS["text_white"]).pack(side="left")

        fields = tk.Frame(filter_card, bg=COLORS["bg_card"])
        fields.pack(fill="x", padx=16, pady=(0, 12))

        def labeled(parent, label, var, width=20):
            col = tk.Frame(parent, bg=COLORS["bg_card"])
            col.pack(side="left", padx=(0, 16))
            tk.Label(col, text=label, font=FONTS["small"],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")
            frame = tk.Frame(col, bg=COLORS["bg_input"],
                             highlightthickness=1, highlightbackground=COLORS["border"])
            frame.pack()
            e = tk.Entry(frame, textvariable=var, width=width,
                         bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                         insertbackground=COLORS["text_primary"],
                         relief="flat", bd=0, font=FONTS["body"])
            e.pack(ipady=6, padx=8)
            e.bind("<Return>", lambda ev: self._search())
            return e

        def combo_labeled(parent, label, var, values, width=18):
            col = tk.Frame(parent, bg=COLORS["bg_card"])
            col.pack(side="left", padx=(0, 16))
            tk.Label(col, text=label, font=FONTS["small"],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")
            cb = ttk.Combobox(col, textvariable=var, values=values,
                               state="readonly", font=FONTS["body"], width=width)
            cb.pack(ipady=4)
            cb.bind("<<ComboboxSelected>>", lambda e: self._search())
            return cb

        self.v_keyword = tk.StringVar()
        self.v_code = tk.StringVar()
        self.v_cat = tk.StringVar(value="Tất cả")
        self.v_min_qty = tk.StringVar()
        self.v_max_qty = tk.StringVar()

        labeled(fields, "Từ khóa (tên SP)", self.v_keyword, 22)
        labeled(fields, "Mã sản phẩm", self.v_code, 14)


        btn_col = tk.Frame(fields, bg=COLORS["bg_card"])
        btn_col.pack(side="left", padx=(8, 0))
        tk.Label(btn_col, text=" ", font=FONTS["small"], bg=COLORS["bg_card"]).pack()
        PrimaryButton(btn_col, "Tìm kiếm", command=self._search, icon="🔍").pack(side="left", padx=(0, 6))
        SecondaryButton(btn_col, "Xóa lọc", command=self._clear).pack(side="left")

        # Result table
        result_header = tk.Frame(self, bg=COLORS["bg_dark"])
        result_header.pack(fill="x", pady=(0, 6))
        tk.Label(result_header, text="Kết quả tìm kiếm", font=FONTS["heading_sm"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(side="left")
        self.result_count = tk.Label(result_header, text="", font=FONTS["body"],
                                     bg=COLORS["bg_dark"], fg=COLORS["text_secondary"])
        self.result_count.pack(side="right")

        cols = ("Mã SP", "Tên sản phẩm", "Danh mục", "Tồn kho", "Tối thiểu",
                "Giá nhập", "Giá bán", "Nhà cung cấp", "Vị trí")
        self.tree = make_table(self, cols)
        widths = [90, 200, 120, 80, 80, 110, 110, 150, 100]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")
        self.tree.column("Tên sản phẩm", anchor="w")

        # Initial empty state hint
        self._hint()

    def _hint(self):
        a = 1
    def _search(self):
        a = 1

    def _clear(self):
        a = 1
    