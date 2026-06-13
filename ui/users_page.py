import tkinter as tk
from tkinter import messagebox
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, make_table, page_header
from database import get_connection, hash_password

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
        if self.current_user["role"] != "admin":
            return
        conn = get_connection()
        rows = conn.execute("SELECT * FROM users ORDER BY role DESC, username").fetchall()
        conn.close()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            tag = "admin_row" if r["role"] == "admin" else "staff_row"
            role_display = "🔑 Admin" if r["role"] == "admin" else "👤 Staff"
            self.tree.insert("", "end", iid=r["id"], tags=(tag,), values=(
                r["id"], r["username"], r["full_name"] or "–",
                role_display, (r["created_at"] or "")[:10]
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một tài khoản!")
            return None
        return int(sel[0])

    def open_add(self):
        UserDialog(self, None, self.current_user, on_save=self.load_data)

    def open_edit(self):
        uid = self._selected_id()
        if uid:
            UserDialog(self, uid, self.current_user, on_save=self.load_data)

    def change_password(self):
        uid = self._selected_id()
        if uid:
            ChangePasswordDialog(self, uid, on_save=self.load_data)

    def delete_user(self):
        uid = self._selected_id()
        if not uid:
            return
        if uid == self.current_user["id"]:
            messagebox.showwarning("Không thể xóa", "Bạn không thể tự xóa tài khoản của mình!")
            return
        conn = get_connection()
        user = conn.execute("SELECT username, role FROM users WHERE id=?", (uid,)).fetchone()
        conn.close()
        if user["role"] == "admin":
            conn = get_connection()
            admin_count = conn.execute("SELECT COUNT(*) FROM users WHERE role='admin'").fetchone()[0]
            conn.close()
            if admin_count <= 1:
                messagebox.showwarning("Không thể xóa", "Phải có ít nhất 1 Admin trong hệ thống!")
                return
        if messagebox.askyesno("Xác nhận", f"Xóa tài khoản '{user['username']}'?", icon="warning"):
            conn = get_connection()
            conn.execute("DELETE FROM users WHERE id=?", (uid,))
            conn.commit()
            conn.close()
            self.load_data()

class UserDialog(tk.Toplevel):
    def __init__(self, parent, user_id, current_user, on_save):
        super().__init__(parent)
        self.user_id = user_id
        self.current_user = current_user
        self.on_save = on_save
        self.title("Thêm tài khoản" if not user_id else "Sửa tài khoản")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("420x360")
        self.resizable(False, False)
        self.grab_set()
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"420x360+{pw - 210}+{ph - 180}")
        self._build()
        if user_id:
            self._populate()

    def _field(self, parent, label, var, show=None):
        tk.Label(parent, text=label, font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
        frame = tk.Frame(parent, bg=COLORS["bg_input"],
                         highlightthickness=1, highlightbackground=COLORS["border"])
        frame.pack(fill="x")
        kw = {"show": show} if show else {}
        e = tk.Entry(frame, textvariable=var, bg=COLORS["bg_input"],
                     fg=COLORS["text_primary"], insertbackground=COLORS["text_primary"],
                     relief="flat", bd=0, font=FONTS["body"], **kw)
        e.pack(fill="x", ipady=8, padx=10)
        return e

    def _build(self):
        tk.Frame(self, bg=COLORS["accent_blue"], height=3).pack(fill="x")
        tk.Label(self, text="👤  Tài khoản người dùng", font=FONTS["heading_md"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(pady=12, padx=20, anchor="w")

        card = tk.Frame(self, bg=COLORS["bg_card"],
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="x", padx=20)
        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=16, pady=12, fill="x")

        self.v_username = tk.StringVar()
        self.v_fullname = tk.StringVar()
        self.v_password = tk.StringVar()
        self.v_role = tk.StringVar(value="staff")

        self._field(inner, "Tên đăng nhập *", self.v_username)
        self._field(inner, "Họ và tên", self.v_fullname)
        if not self.user_id: # only show password field when creating new user
            self._field(inner, "Mật khẩu *", self.v_password, show="•")

        tk.Label(inner, text="Vai trò", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 4))
        role_frame = tk.Frame(inner, bg=COLORS["bg_card"])
        role_frame.pack(anchor="w")
        for val, label in [("admin", "🔑 Admin"), ("staff", "👤 Staff")]:
            tk.Radiobutton(role_frame, text=label, variable=self.v_role, value=val,
                           bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                           selectcolor=COLORS["bg_input"], activebackground=COLORS["bg_card"],
                           font=FONTS["body"]).pack(side="left", padx=(0, 20))

        btn = tk.Frame(self, bg=COLORS["bg_dark"])
        btn.pack(fill="x", padx=20, pady=12)
        PrimaryButton(btn, "Lưu", command=self._save, icon="💾").pack(side="right", padx=(6, 0))
        SecondaryButton(btn, "Hủy", command=self.destroy).pack(side="right")

    def _populate(self):
        conn = get_connection()
        u = conn.execute("SELECT * FROM users WHERE id=?", (self.user_id,)).fetchone()
        conn.close()
        if u:
            self.v_username.set(u["username"])
            self.v_fullname.set(u["full_name"] or "")
            self.v_role.set(u["role"])

    def _save(self):
        username = self.v_username.get().strip()
        if not username:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập!", parent=self)
            return
        conn = get_connection()
        try:
            if self.user_id:
                conn.execute("UPDATE users SET username=?, full_name=?, role=? WHERE id=?",
                             (username, self.v_fullname.get(), self.v_role.get(), self.user_id))
            else:
                pw = self.v_password.get()
                if not pw:
                    messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu!", parent=self)
                    conn.close(); return
                conn.execute("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                             (username, hash_password(pw), self.v_fullname.get(), self.v_role.get()))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=self)
            conn.close(); return
        conn.close()
        self.on_save()
        self.destroy()


class ChangePasswordDialog(tk.Toplevel):
    def __init__(self, parent, user_id, on_save):
        super().__init__(parent)
        self.user_id = user_id
        self.on_save = on_save
        self.title("Đổi mật khẩu")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("400x280")
        self.resizable(False, False)
        self.grab_set()
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        self.geometry(f"400x280+{pw - 200}+{ph - 140}")
        self._build()

    def _field(self, parent, label, var):
        tk.Label(parent, text=label, font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(8, 2))
        frame = tk.Frame(parent, bg=COLORS["bg_input"],
                         highlightthickness=1, highlightbackground=COLORS["border"])
        frame.pack(fill="x")
        e = tk.Entry(frame, textvariable=var, show="•",
                     bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                     insertbackground=COLORS["text_primary"],
                     relief="flat", bd=0, font=FONTS["body"])
        e.pack(fill="x", ipady=8, padx=10)

    def _build(self):
        tk.Frame(self, bg=COLORS["accent_yellow"], height=3).pack(fill="x")
        tk.Label(self, text="🔑  Đổi mật khẩu", font=FONTS["heading_md"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(pady=12, padx=20, anchor="w")

        card = tk.Frame(self, bg=COLORS["bg_card"],
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="x", padx=20)
        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=16, pady=12, fill="x")

        self.v_new = tk.StringVar()
        self.v_confirm = tk.StringVar()
        self._field(inner, "Mật khẩu mới *", self.v_new)
        self._field(inner, "Xác nhận mật khẩu *", self.v_confirm)

        btn = tk.Frame(self, bg=COLORS["bg_dark"])
        btn.pack(fill="x", padx=20, pady=12)
        PrimaryButton(btn, "Đổi mật khẩu", command=self._save, icon="🔑").pack(side="right", padx=(6, 0))
        SecondaryButton(btn, "Hủy", command=self.destroy).pack(side="right")

    def _save(self):
        new_pw = self.v_new.get()
        if not new_pw:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu mới!", parent=self)
            return
        if new_pw != self.v_confirm.get():
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!", parent=self)
            return
        if len(new_pw) < 6:
            messagebox.showwarning("Cảnh báo", "Mật khẩu nên có ít nhất 6 ký tự!", parent=self)
        conn = get_connection()
        conn.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_pw), self.user_id))
        conn.commit()
        conn.close()
        self.on_save()
        self.destroy()
        messagebox.showinfo("Thành công", "Đã đổi mật khẩu!")