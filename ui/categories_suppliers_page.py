
import tkinter as tk
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, SearchBar, make_table, page_header
from database import get_connection
from tkinter import messagebox, ttk

class CategoriesPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()
        self.load_data()

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
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.id, c.name, c.description,
                   (SELECT COUNT(*) FROM products p WHERE p.category_id=c.id) as cnt,
                   c.created_at
            FROM categories c
            WHERE c.name LIKE ? OR c.description LIKE ?
            ORDER BY c.name
        """, (f"%{q}%", f"%{q}%")).fetchall()
        conn.close()
        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 else "odd"
            self.tree.insert("", "end", iid=r["id"], tags=(tag,), values=(
                r["id"], r["name"], r["description"] or "–",
                r["cnt"], (r["created_at"] or "")[:10]
            ))

    def search(self, q): self.load_data(q)

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một danh mục!")
            return None
        return int(sel[0])

    def open_add(self):
        CategoryDialog(self, None, on_save=self.load_data)

    def open_edit(self):
        cid = self._selected_id()
        if cid:
            CategoryDialog(self, cid, on_save=self.load_data)

    def delete_item(self):
        cid = self._selected_id()
        if not cid:
            return
        conn = get_connection()
        cat = conn.execute("SELECT name FROM categories WHERE id=?", (cid,)).fetchone()
        cnt = conn.execute("SELECT COUNT(*) FROM products WHERE category_id=?", (cid,)).fetchone()[0]
        conn.close()
        if cnt > 0:
            messagebox.showwarning("Không thể xóa",
                                   f"Danh mục '{cat['name']}' đang có {cnt} sản phẩm!\nHãy chuyển sản phẩm trước.")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa danh mục '{cat['name']}'?", icon="warning"):
            conn = get_connection()
            conn.execute("DELETE FROM categories WHERE id=?", (cid,))
            conn.commit()
            conn.close()
            self.load_data()


class CategoryDialog(tk.Toplevel):
    def __init__(self, parent, cat_id, on_save):
        super().__init__(parent)
        self.cat_id = cat_id
        self.on_save = on_save
        self.title("Thêm danh mục" if not cat_id else "Sửa danh mục")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("420x280")
        self.resizable(False, False)
        self.grab_set()
        self._center(parent)
        self._build()
        if cat_id:
            self._populate()

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"420x280+{pw - 210}+{ph - 140}")

    def _field(self, parent, label, var, multiline=False):
        tk.Label(parent, text=label, font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(10, 2))
        frame = tk.Frame(parent, bg=COLORS["bg_input"],
                         highlightthickness=1, highlightbackground=COLORS["border"])
        frame.pack(fill="x")
        e = tk.Entry(frame, textvariable=var, bg=COLORS["bg_input"],
                     fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"],
                     relief="flat", bd=0, font=FONTS["body"])
        e.pack(fill="x", ipady=8, padx=10)
        return e

    def _build(self):
        tk.Frame(self, bg=COLORS["accent"], height=3).pack(fill="x")
        tk.Label(self, text="🏷️  Danh mục sản phẩm", font=FONTS["heading_md"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(pady=12, padx=20, anchor="w")

        card = tk.Frame(self, bg=COLORS["bg_card"],
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="x", padx=20)
        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=16, pady=12, fill="x")

        self.v_name = tk.StringVar()
        self.v_desc = tk.StringVar()
        self._field(inner, "Tên danh mục *", self.v_name)
        self._field(inner, "Mô tả", self.v_desc)

        btn = tk.Frame(self, bg=COLORS["bg_dark"])
        btn.pack(fill="x", padx=20, pady=12)
        PrimaryButton(btn, "Lưu", command=self._save, icon="💾").pack(side="right", padx=(6, 0))
        SecondaryButton(btn, "Hủy", command=self.destroy).pack(side="right")

    def _populate(self):
        conn = get_connection()
        c = conn.execute("SELECT * FROM categories WHERE id=?", (self.cat_id,)).fetchone()
        conn.close()
        if c:
            self.v_name.set(c["name"])
            self.v_desc.set(c["description"] or "")

    def _save(self):
        name = self.v_name.get().strip()
        if not name:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên danh mục!", parent=self)
            return
        conn = get_connection()
        try:
            if self.cat_id:
                conn.execute("UPDATE categories SET name=?, description=? WHERE id=?",
                             (name, self.v_desc.get(), self.cat_id))
            else:
                conn.execute("INSERT INTO categories (name, description) VALUES (?, ?)",
                             (name, self.v_desc.get()))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self)
            conn.close(); return
        conn.close()
        self.on_save()
        self.destroy()


    
class SuppliersPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()
        self.load_data()

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
        conn = get_connection()
        rows = conn.execute("""
            SELECT s.id, s.name, s.phone, s.email, s.address,
                   (SELECT COUNT(*) FROM products p WHERE p.supplier_id=s.id) as cnt,
                   s.created_at
            FROM suppliers s
            WHERE s.name LIKE ? OR s.phone LIKE ? OR s.email LIKE ?
            ORDER BY s.name
        """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
        conn.close()
        self.tree.delete(*self.tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 else "odd"
            self.tree.insert("", "end", iid=r["id"], tags=(tag,), values=(
                r["id"], r["name"], r["phone"] or "–",
                r["email"] or "–", r["address"] or "–",
                r["cnt"], (r["created_at"] or "")[:10]
            ))

    def search(self, q): self.load_data(q)

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một nhà cung cấp!")
            return None
        return int(sel[0])

    def open_add(self):
        SupplierDialog(self, None, on_save=self.load_data)

    def open_edit(self):
        sid = self._selected_id()
        if sid:
            SupplierDialog(self, sid, on_save=self.load_data)

    def delete_item(self):
        sid = self._selected_id()
        if not sid:
            return
        conn = get_connection()
        sup = conn.execute("SELECT name FROM suppliers WHERE id=?", (sid,)).fetchone()
        cnt = conn.execute("SELECT COUNT(*) FROM products WHERE supplier_id=?", (sid,)).fetchone()[0]
        conn.close()
        if cnt > 0:
            messagebox.showwarning("Không thể xóa",
                                   f"NCC '{sup['name']}' đang cung cấp {cnt} sản phẩm!")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa nhà cung cấp '{sup['name']}'?", icon="warning"):
            conn = get_connection()
            conn.execute("DELETE FROM suppliers WHERE id=?", (sid,))
            conn.commit()
            conn.close()
            self.load_data()


class SupplierDialog(tk.Toplevel):
    def __init__(self, parent, sup_id, on_save):
        super().__init__(parent)
        self.sup_id = sup_id
        self.on_save = on_save
        self.title("Thêm nhà cung cấp" if not sup_id else "Sửa nhà cung cấp")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("460x380")
        self.resizable(False, False)
        self.grab_set()
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"460x380+{pw - 230}+{ph - 190}")
        self._build()
        if sup_id:
            self._populate()

    def _field(self, parent, label, var):
        tk.Label(parent, text=label, font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
        frame = tk.Frame(parent, bg=COLORS["bg_input"],
                         highlightthickness=1, highlightbackground=COLORS["border"])
        frame.pack(fill="x")
        e = tk.Entry(frame, textvariable=var, bg=COLORS["bg_input"],
                     fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"],
                     relief="flat", bd=0, font=FONTS["body"])
        e.pack(fill="x", ipady=8, padx=10)
        return e

    def _build(self):
        tk.Frame(self, bg=COLORS["accent_blue"], height=3).pack(fill="x")
        tk.Label(self, text="🏭  Nhà cung cấp", font=FONTS["heading_md"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(pady=12, padx=20, anchor="w")

        card = tk.Frame(self, bg=COLORS["bg_card"],
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="x", padx=20)
        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=16, pady=12, fill="x")

        self.v_name = tk.StringVar()
        self.v_phone = tk.StringVar()
        self.v_email = tk.StringVar()
        self.v_addr = tk.StringVar()

        self._field(inner, "Tên nhà cung cấp *", self.v_name)

        row = tk.Frame(inner, bg=COLORS["bg_card"])
        row.pack(fill="x")
        l = tk.Frame(row, bg=COLORS["bg_card"]); l.pack(side="left", fill="x", expand=True, padx=(0, 8))
        r = tk.Frame(row, bg=COLORS["bg_card"]); r.pack(side="left", fill="x", expand=True)
        self._field(l, "Số điện thoại", self.v_phone)
        self._field(r, "Email", self.v_email)
        self._field(inner, "Địa chỉ", self.v_addr)

        btn = tk.Frame(self, bg=COLORS["bg_dark"])
        btn.pack(fill="x", padx=20, pady=12)
        PrimaryButton(btn, "Lưu", command=self._save, icon="💾").pack(side="right", padx=(6, 0))
        SecondaryButton(btn, "Hủy", command=self.destroy).pack(side="right")

    def _populate(self):
        conn = get_connection()
        s = conn.execute("SELECT * FROM suppliers WHERE id=?", (self.sup_id,)).fetchone()
        conn.close()
        if s:
            self.v_name.set(s["name"])
            self.v_phone.set(s["phone"] or "")
            self.v_email.set(s["email"] or "")
            self.v_addr.set(s["address"] or "")

    def _save(self):
        name = self.v_name.get().strip()
        if not name:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên nhà cung cấp!", parent=self)
            return
        conn = get_connection()
        try:
            if self.sup_id:
                conn.execute("UPDATE suppliers SET name=?, phone=?, email=?, address=? WHERE id=?",
                             (name, self.v_phone.get(), self.v_email.get(), self.v_addr.get(), self.sup_id))
            else:
                conn.execute("INSERT INTO suppliers (name, phone, email, address) VALUES (?, ?, ?, ?)",
                             (name, self.v_phone.get(), self.v_email.get(), self.v_addr.get()))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self)
            conn.close(); return
        conn.close()
        self.on_save()
        self.destroy()
        
    