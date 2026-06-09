import tkinter as tk
from theme import COLORS, FONTS
from widgets import StatCard, Card, page_header
from database import get_connection


class DashboardPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self._build()
        self.refresh()

    def _build(self):
        page_header(self, "📊  Tổng quan", "Theo dõi toàn bộ hoạt động kho hàng")

        # ── Stat cards row ──────────────────────────────────
        stats_row = tk.Frame(self, bg=COLORS["bg_dark"])
        stats_row.pack(fill="x", pady=(0, 20))

        self.sc_products = StatCard(stats_row, "Tổng sản phẩm", "–", "📦", COLORS["accent_blue"])
        self.sc_products.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.sc_stock = StatCard(stats_row, "Tổng tồn kho", "–", "🏪", COLORS["accent"])
        self.sc_stock.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.sc_low = StatCard(stats_row, "Sắp hết hàng", "–", "⚠️", COLORS["accent_orange"])
        self.sc_low.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.sc_value = StatCard(stats_row, "Giá trị kho (VNĐ)", "–", "💰", COLORS["accent_yellow"])
        self.sc_value.pack(side="left", expand=True, fill="both")

        # ── Second row ──────────────────────────────────────
        stats_row2 = tk.Frame(self, bg=COLORS["bg_dark"])
        stats_row2.pack(fill="x", pady=(0, 20))

        self.sc_stockin = StatCard(stats_row2, "Phiếu nhập hôm nay", "–", "📥", COLORS["accent"])
        self.sc_stockin.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.sc_stockout = StatCard(stats_row2, "Phiếu xuất hôm nay", "–", "📤", COLORS["accent_purple"])
        self.sc_stockout.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.sc_suppliers = StatCard(stats_row2, "Nhà cung cấp", "–", "🏭", COLORS["accent_blue"])
        self.sc_suppliers.pack(side="left", expand=True, fill="both", padx=(0, 10))

        self.sc_users = StatCard(stats_row2, "Tài khoản", "–", "👥", COLORS["info"])
        self.sc_users.pack(side="left", expand=True, fill="both")

        # ── Bottom panels ────────────────────────────────────
        bottom = tk.Frame(self, bg=COLORS["bg_dark"])
        bottom.pack(fill="both", expand=True)

        # Low stock panel
        left_card = Card(bottom)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(left_card, text="⚠️  Hàng sắp hết", font=FONTS["heading_sm"],
                 bg=COLORS["bg_card"], fg=COLORS["accent_orange"]).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Frame(left_card, bg=COLORS["border"], height=1).pack(fill="x", padx=16)

        self.low_frame = tk.Frame(left_card, bg=COLORS["bg_card"])
        self.low_frame.pack(fill="both", expand=True, padx=16, pady=8)

        # Recent activity panel
        right_card = Card(bottom)
        right_card.pack(side="left", fill="both", expand=True)
        tk.Label(right_card, text="🕐  Hoạt động gần đây", font=FONTS["heading_sm"],
                 bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack(anchor="w", padx=16, pady=(12, 4))
        tk.Frame(right_card, bg=COLORS["border"], height=1).pack(fill="x", padx=16)

        self.activity_frame = tk.Frame(right_card, bg=COLORS["bg_card"])
        self.activity_frame.pack(fill="both", expand=True, padx=16, pady=8)

    def refresh(self):
        conn = get_connection()

        total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        total_stock = conn.execute("SELECT SUM(quantity) FROM products").fetchone()[0] or 0 # do sum có thể trả về None nếu không có sản phẩm nào, nên dùng `or 0` để tránh lỗi hiển thị.
        low_stock = conn.execute("SELECT COUNT(*) FROM products WHERE quantity <= min_quantity").fetchone()[0]
        total_value = conn.execute("SELECT SUM(quantity * import_price) FROM products").fetchone()[0] or 0
        today_in = conn.execute("SELECT COUNT(*) FROM stock_in WHERE date(import_date)=date('now','localtime')").fetchone()[0]
        today_out = conn.execute("SELECT COUNT(*) FROM stock_out WHERE date(export_date)=date('now','localtime')").fetchone()[0]
        n_suppliers = conn.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0]
        n_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

        self.sc_products.update_value(total_products)
        self.sc_stock.update_value(f"{total_stock:,}")
        self.sc_low.update_value(low_stock)
        self.sc_value.update_value(f"{total_value:,.0f}")
        self.sc_stockin.update_value(today_in)
        self.sc_stockout.update_value(today_out)
        self.sc_suppliers.update_value(n_suppliers)
        self.sc_users.update_value(n_users)

        # Low-stock list
        for w in self.low_frame.winfo_children():
            w.destroy()
        low_items = conn.execute("""
            SELECT p.name, p.quantity, p.min_quantity, c.name as cat
            FROM products p
            LEFT JOIN categories c ON p.category_id=c.id
            WHERE p.quantity <= p.min_quantity
            ORDER BY p.quantity ASC LIMIT 8
        """).fetchall()

        if not low_items:
            tk.Label(self.low_frame, text="✅ Tất cả hàng đủ số lượng",
                     font=FONTS["body"], bg=COLORS["bg_card"],
                     fg=COLORS["success"]).pack(pady=20)
        else:
            for item in low_items:
                row = tk.Frame(self.low_frame, bg=COLORS["bg_card"])
                row.pack(fill="x", pady=2)
                tk.Label(row, text=f"• {item['name'][:28]}",
                         font=FONTS["body"], bg=COLORS["bg_card"],
                         fg=COLORS["text_primary"], anchor="w").pack(side="left")
                color = COLORS["danger"] if item["quantity"] == 0 else COLORS["accent_orange"]
                tk.Label(row, text=f"{item['quantity']} / {item['min_quantity']}",
                         font=FONTS["body_bold"], bg=COLORS["bg_card"],
                         fg=color).pack(side="right")

        # Recent activity
        for w in self.activity_frame.winfo_children():
            w.destroy()

        activities = []
        ins = conn.execute("""
            SELECT 'Nhập' as type, p.name, si.quantity, si.import_date as dt 
            FROM stock_in si JOIN products p ON si.product_id=p.id
            ORDER BY si.import_date DESC LIMIT 5
        """).fetchall()
        outs = conn.execute("""
            SELECT 'Xuất' as type, p.name, so.quantity, so.export_date as dt
            FROM stock_out so JOIN products p ON so.product_id=p.id
            ORDER BY so.export_date DESC LIMIT 5
        """).fetchall()

        all_acts = list(ins) + list(outs)
        all_acts.sort(key=lambda x: x["dt"] or "", reverse=True) # sắp xếp theo ngày, nếu dt là None thì trả về "" và cho về cuối cùng

        if not all_acts:
            tk.Label(self.activity_frame, text="Chưa có hoạt động nào",
                     font=FONTS["body"], bg=COLORS["bg_card"],
                     fg=COLORS["text_muted"]).pack(pady=20)
        else:
            for act in all_acts[:8]:
                row = tk.Frame(self.activity_frame, bg=COLORS["bg_card"])
                row.pack(fill="x", pady=3)

                badge_color = COLORS["accent"] if act["type"] == "Nhập" else COLORS["accent_purple"]
                tk.Label(row, text=f" {act['type']} ",
                         font=FONTS["small"], bg=badge_color,
                         fg="white").pack(side="left", padx=(0, 8))
                tk.Label(row, text=f"{act['name'][:22]}",
                         font=FONTS["body"], bg=COLORS["bg_card"],
                         fg=COLORS["text_primary"]).pack(side="left")
                tk.Label(row, text=f"×{act['quantity']}",
                         font=FONTS["body_bold"], bg=COLORS["bg_card"],
                         fg=COLORS["text_secondary"]).pack(side="right")

        conn.close()
