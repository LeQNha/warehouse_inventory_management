import tkinter as tk
from tkinter import messagebox, ttk
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, SearchBar, make_table, page_header


class CategoriesPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user


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


# ══════════════════════════════════════════════
#  SUPPLIERS PAGE
# ══════════════════════════════════════════════
class SuppliersPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        
