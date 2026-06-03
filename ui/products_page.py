import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, SearchBar, make_table, page_header, Card
from database import get_connection


class ProductsPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()
        self.load_data()

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
        conn = get_connection()
        cats = ["Tất cả"] + [r["name"] for r in conn.execute("SELECT name FROM categories ORDER BY name").fetchall()]
        conn.close()
        self.cat_combo["values"] = cats
        if self.cat_var.get() not in cats:
            self.cat_var.set("Tất cả")

    def load_data(self, query=""):
        self._refresh_categories()
        cat_filter = self.cat_var.get()
        conn = get_connection()
        sql = """
            SELECT p.product_code, p.name, c.name as cat, p.quantity,
                   p.import_price, p.export_price, s.name as supplier, p.location,
                   p.id, p.min_quantity
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            LEFT JOIN suppliers s ON p.supplier_id=s.id
            WHERE (p.name LIKE ? OR p.product_code LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%"]
        if cat_filter and cat_filter != "Tất cả":
            sql += " AND c.name = ?"
            params.append(cat_filter)
        sql += " ORDER BY p.name"
        rows = conn.execute(sql, params).fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = "low" if r["quantity"] <= r["min_quantity"] else ("even" if i % 2 else "odd")
            self.tree.insert("", "end", iid=r["id"], tags=(tag,), values=(
                r["product_code"], r["name"], r["cat"] or "–",
                f"{r['quantity']:,}", f"{r['import_price']:,.0f}",
                f"{r['export_price']:,.0f}", r["supplier"] or "–",
                r["location"] or "–"
            ))
        self.status_label.config(text=f"{len(rows)} sản phẩm")

    def search(self, q):
        self.load_data(q)

    def _show_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sản phẩm!")
            return None
        return int(sel[0])

    def open_add(self):
        ProductDialog(self, None, self.current_user, on_save=self.load_data)

    def open_edit(self):
        pid = self._selected_id()
        if pid:
            ProductDialog(self, pid, self.current_user, on_save=self.load_data)

    def delete_product(self):
        pid = self._selected_id()
        if not pid:
            return
        conn = get_connection()
        prod = conn.execute("SELECT name FROM products WHERE id=?", (pid,)).fetchone()
        conn.close()
        if not prod:
            return
        if messagebox.askyesno("Xác nhận xóa",
                               f"Bạn có chắc muốn xóa sản phẩm:\n'{prod['name']}'?",
                               icon="warning"):
            conn = get_connection()
            conn.execute("DELETE FROM products WHERE id=?", (pid,))
            conn.commit()
            conn.close()
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")


class ProductDialog(tk.Toplevel):
    def __init__(self, parent, product_id, current_user, on_save):
        super().__init__(parent)
        self.product_id = product_id
        self.current_user = current_user
        self.on_save = on_save
        self.title("Thêm sản phẩm" if not product_id else "Chỉnh sửa sản phẩm")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("560x620")
        self.resizable(False, False)
        self.grab_set()

        # Center
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"560x620+{pw - 280}+{ph - 310}")

        self.cats = {}
        self.sups = {}
        self._load_refs()
        self._build()
        if product_id:
            self._populate()

    def _load_refs(self):
        conn = get_connection()
        for c in conn.execute("SELECT id, name FROM categories ORDER BY name"):
            self.cats[c["name"]] = c["id"]
        for s in conn.execute("SELECT id, name FROM suppliers ORDER BY name"):
            self.sups[s["name"]] = s["id"]
        conn.close()

    def _field(self, parent, label, var, placeholder=""):
        tk.Label(parent, text=label, font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
        frame = tk.Frame(parent, bg=COLORS["bg_input"],
                         highlightthickness=1, highlightbackground=COLORS["border"])
        frame.pack(fill="x")
        e = tk.Entry(frame, textvariable=var, bg=COLORS["bg_input"],
                     fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"],
                     relief="flat", bd=0, font=FONTS["body"])
        e.pack(fill="x", ipady=8, padx=10)
        e.bind("<FocusIn>", lambda ev: frame.config(highlightbackground=COLORS["border_focus"]))
        e.bind("<FocusOut>", lambda ev: frame.config(highlightbackground=COLORS["border"]))
        return e

    def _combo(self, parent, label, var, choices):
        tk.Label(parent, text=label, font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
        cb = ttk.Combobox(parent, textvariable=var, values=choices,
                          state="readonly", font=FONTS["body"])
        cb.pack(fill="x", ipady=4)
        return cb

    def _build(self):
        tk.Frame(self, bg=COLORS["accent"], height=3).pack(fill="x")
        title = "➕  Thêm sản phẩm mới" if not self.product_id else "✏️  Chỉnh sửa sản phẩm"
        tk.Label(self, text=title, font=FONTS["heading_md"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(pady=(16, 8), padx=20, anchor="w")

        scroll_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        scroll_frame.pack(fill="both", expand=True, padx=20)

        card = tk.Frame(scroll_frame, bg=COLORS["bg_card"],
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=20, pady=16, fill="both")

        # Vars
        self.v_code = tk.StringVar()
        self.v_name = tk.StringVar()
        self.v_cat = tk.StringVar()
        self.v_qty = tk.StringVar(value="0")
        self.v_import = tk.StringVar(value="0")
        self.v_export = tk.StringVar(value="0")
        self.v_sup = tk.StringVar()
        self.v_loc = tk.StringVar()
        self.v_min = tk.StringVar(value="10")

        # Two-column layout
        row1 = tk.Frame(inner, bg=COLORS["bg_card"])
        row1.pack(fill="x")
        left1 = tk.Frame(row1, bg=COLORS["bg_card"])
        left1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        right1 = tk.Frame(row1, bg=COLORS["bg_card"])
        right1.pack(side="left", fill="x", expand=True)

        self._field(left1, "Mã sản phẩm *", self.v_code)
        self._field(right1, "Tên sản phẩm *", self.v_name)

        self._combo(inner, "Danh mục", self.v_cat, list(self.cats.keys()))
        self._combo(inner, "Nhà cung cấp", self.v_sup, list(self.sups.keys()))

        row2 = tk.Frame(inner, bg=COLORS["bg_card"])
        row2.pack(fill="x")
        l2 = tk.Frame(row2, bg=COLORS["bg_card"]); l2.pack(side="left", fill="x", expand=True, padx=(0, 10))
        m2 = tk.Frame(row2, bg=COLORS["bg_card"]); m2.pack(side="left", fill="x", expand=True, padx=(0, 10))
        r2 = tk.Frame(row2, bg=COLORS["bg_card"]); r2.pack(side="left", fill="x", expand=True)

        self._field(l2, "Số lượng", self.v_qty)
        self._field(m2, "Giá nhập (VNĐ)", self.v_import)
        self._field(r2, "Giá bán (VNĐ)", self.v_export)

        row3 = tk.Frame(inner, bg=COLORS["bg_card"])
        row3.pack(fill="x")
        l3 = tk.Frame(row3, bg=COLORS["bg_card"]); l3.pack(side="left", fill="x", expand=True, padx=(0, 10))
        r3 = tk.Frame(row3, bg=COLORS["bg_card"]); r3.pack(side="left", fill="x", expand=True)

        self._field(l3, "Vị trí trong kho", self.v_loc)
        self._field(r3, "SL tối thiểu", self.v_min)

        # Buttons
        btn_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", padx=20, pady=12)
        PrimaryButton(btn_frame, "Lưu", command=self._save, icon="💾").pack(side="right", padx=(6, 0))
        SecondaryButton(btn_frame, "Hủy", command=self.destroy).pack(side="right")

    def _populate(self):
        conn = get_connection()
        p = conn.execute("""
            SELECT p.*, c.name as cat_name, s.name as sup_name
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            LEFT JOIN suppliers s ON p.supplier_id=s.id
            WHERE p.id=?
        """, (self.product_id,)).fetchone()
        conn.close()
        if p:
            self.v_code.set(p["product_code"])
            self.v_name.set(p["name"])
            self.v_cat.set(p["cat_name"] or "")
            self.v_qty.set(str(p["quantity"]))
            self.v_import.set(str(p["import_price"]))
            self.v_export.set(str(p["export_price"]))
            self.v_sup.set(p["sup_name"] or "")
            self.v_loc.set(p["location"] or "")
            self.v_min.set(str(p["min_quantity"]))

    def _save(self):
        code = self.v_code.get().strip()
        name = self.v_name.get().strip()
        if not code or not name:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã và Tên sản phẩm!", parent=self)
            return
        try:
            qty = int(self.v_qty.get() or 0)
            imp = float(self.v_import.get() or 0)
            exp = float(self.v_export.get() or 0)
            min_q = int(self.v_min.get() or 10)
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng và giá phải là số!", parent=self)
            return

        cat_id = self.cats.get(self.v_cat.get())
        sup_id = self.sups.get(self.v_sup.get())

        conn = get_connection()
        try:
            if self.product_id:
                conn.execute("""
                    UPDATE products SET product_code=?, name=?, category_id=?, quantity=?,
                    import_price=?, export_price=?, supplier_id=?, location=?, min_quantity=?
                    WHERE id=?
                """, (code, name, cat_id, qty, imp, exp, sup_id,
                      self.v_loc.get(), min_q, self.product_id))
            else:
                conn.execute("""
                    INSERT INTO products (product_code, name, category_id, quantity,
                    import_price, export_price, supplier_id, location, min_quantity)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (code, name, cat_id, qty, imp, exp, sup_id, self.v_loc.get(), min_q))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu: {e}", parent=self)
            conn.close()
            return
        conn.close()
        self.on_save()
        self.destroy()
        messagebox.showinfo("Thành công", "Đã lưu sản phẩm!")
