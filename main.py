import tkinter as tk
from tkinter import messagebox
import sys, os

# Allow imports from parent
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from theme import COLORS, FONTS
from database import init_db
from ui.login_page import LoginPage
from ui.dashboard_page import DashboardPage
from ui.products_page import ProductsPage
from ui.categories_suppliers_page import CategoriesPage, SuppliersPage
from ui.stockio_page import StockInPage, StockOutPage
from ui.search_page import SearchPage
from ui.reports_page import ReportsPage
from ui.users_page import UsersPage


NAV_ITEMS = [
    ("dashboard",   "📊", "Tổng quan"),
    ("products",    "📦", "Sản phẩm"),
    ("categories",  "🏷️", "Danh mục"),
    ("suppliers",   "🏭", "Nhà cung cấp"),
    ("stockin",     "📥", "Nhập kho"),
    ("stockout",    "📤", "Xuất kho"),
    ("search",      "🔍", "Tìm kiếm"),
    ("reports",     "📈", "Báo cáo"),
    ("users",       "👥", "Tài khoản"),
]


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()         # hide until login done
        self.title("Warehouse Management System")
        self.geometry("1280x760")
        self.minsize(1024, 640)
        self.configure(bg=COLORS["bg_dark"])

        self.current_user = None
        self.pages = {}
        self.active_page = None
        self.nav_buttons = {}

        init_db()
        self._show_login()

    # ── Login ────────────────────────────────────────────
    def _show_login(self):
        LoginPage(on_success=self._on_login)

    def _on_login(self, user):
        self.current_user = user
        self.title(f"Warehouse Management System  –  {user['full_name'] or user['username']}")
        self._build_main_ui()
        self.deiconify()
        self._center_window()
        self.navigate("dashboard")

    def _center_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = 1280, 760
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # ── Main layout ──────────────────────────────────────
    def _build_main_ui(self):
        self.main_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        self.main_frame.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_content_area()

    def _build_sidebar(self):
        self.sidebar = tk.Frame(self.main_frame, bg=COLORS["bg_sidebar"], width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo area
        logo = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"], pady=20)
        logo.pack(fill="x")
        tk.Label(logo, text="📦", font=("Segoe UI", 28),
                 bg=COLORS["bg_sidebar"], fg=COLORS["text_white"]).pack()
        tk.Label(logo, text="WareHub", font=FONTS["heading_md"],
                 bg=COLORS["bg_sidebar"], fg=COLORS["text_white"]).pack()
        tk.Label(logo, text="Quản lý kho hàng", font=FONTS["small"],
                 bg=COLORS["bg_sidebar"], fg=COLORS["text_muted"]).pack()

        # Divider
        tk.Frame(self.sidebar, bg=COLORS["border"], height=1).pack(fill="x", padx=12, pady=4)

        # Nav buttons
        nav_frame = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        nav_frame.pack(fill="x", pady=4)

        for key, icon, label in NAV_ITEMS:
            # Skip users page for non-admin
            if key == "users" and self.current_user.get("role") != "admin":
                continue
            btn = tk.Button(
                nav_frame,
                text=f"  {icon}  {label}",
                anchor="w",
                command=lambda k=key: self.navigate(k),
                bg=COLORS["bg_sidebar"],
                fg=COLORS["text_secondary"],
                activebackground=COLORS["bg_hover"],
                activeforeground=COLORS["text_white"],
                relief="flat", bd=0,
                pady=10, padx=10,
                cursor="hand2",
                font=FONTS["nav"],
                width=22,
            )
            btn.pack(fill="x", padx=6, pady=1)
            self.nav_buttons[key] = btn

        # Bottom: user info + logout
        bottom = tk.Frame(self.sidebar, bg=COLORS["bg_sidebar"])
        bottom.pack(side="bottom", fill="x", pady=8)
        tk.Frame(bottom, bg=COLORS["border"], height=1).pack(fill="x", padx=12, pady=(0, 8))

        role_color = COLORS["accent"] if self.current_user["role"] == "admin" else COLORS["accent_blue"]
        tk.Label(bottom, text=self.current_user.get("full_name") or self.current_user["username"],
                 font=FONTS["body_bold"], bg=COLORS["bg_sidebar"],
                 fg=COLORS["text_primary"]).pack(padx=12, anchor="w")
        tk.Label(bottom,
                 text=f"{'🔑 Admin' if self.current_user['role']=='admin' else '👤 Staff'}",
                 font=FONTS["small"], bg=COLORS["bg_sidebar"], fg=role_color).pack(padx=12, anchor="w")

        logout_btn = tk.Button(bottom, text="⏻  Đăng xuất", command=self._logout,
                               bg=COLORS["bg_input"], fg=COLORS["text_secondary"],
                               activebackground=COLORS["danger"], activeforeground="white",
                               relief="flat", bd=0, padx=14, pady=6,
                               cursor="hand2", font=FONTS["nav"])
        logout_btn.pack(fill="x", padx=8, pady=(6, 0))

    def _build_content_area(self):
        self.content_area = tk.Frame(self.main_frame, bg=COLORS["bg_dark"])
        self.content_area.pack(side="left", fill="both", expand=True)

        self.page_container = tk.Frame(self.content_area, bg=COLORS["bg_dark"])
        self.page_container.pack(fill="both", expand=True, padx=20, pady=20)

    # ── Navigation ───────────────────────────────────────
    def navigate(self, key):
        # Highlight nav button
        for k, btn in self.nav_buttons.items():
            btn.config(
                bg=COLORS["bg_selected"] if k == key else COLORS["bg_sidebar"],
                fg=COLORS["text_white"]  if k == key else COLORS["text_secondary"],
            )

        # Destroy ALL old pages, create fresh each time
        for p in list(self.pages.values()):
            p.destroy()
        self.pages.clear()
        self.active_page = key

        page_cls = {
            "dashboard":  DashboardPage,
            "products":   ProductsPage,
            "categories": CategoriesPage,
            "suppliers":  SuppliersPage,
            "stockin":    StockInPage,
            "stockout":   StockOutPage,
            "search":     SearchPage,
            "reports":    ReportsPage,
            "users":      UsersPage,
        }.get(key)

        if page_cls:
            try:
                page = page_cls(self.page_container, self.current_user)
                page.pack(fill="both", expand=True)
                self.pages[key] = page
            except Exception as e:
                import traceback
                traceback.print_exc()
                import tkinter.messagebox as mb
                mb.showerror("Lỗi trang", f"Không thể tải trang '{key}':\n{e}")

    def _logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có muốn đăng xuất?"):
            self.current_user = None
            self.pages.clear()
            for w in self.main_frame.winfo_children():
                w.destroy()
            self.main_frame.destroy()
            self.withdraw()
            self._show_login()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
