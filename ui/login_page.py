import tkinter as tk
from tkinter import messagebox
from theme import COLORS, FONTS


class LoginPage(tk.Toplevel):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.title("Warehouse Management System – Đăng nhập")
        self.geometry("480x580")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg_dark"])
        self.grab_set()

        # Center window
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 480) // 2
        y = (sh - 580) // 2
        self.geometry(f"480x580+{x}+{y}")

        self._build()

    def _build(self):
        # Top accent bar
        tk.Frame(self, bg=COLORS["accent"], height=4).pack(fill="x")

        wrapper = tk.Frame(self, bg=COLORS["bg_dark"])
        wrapper.pack(expand=True, fill="both", padx=48)

        # Logo / icon
        tk.Label(wrapper, text="📦", font=("Segoe UI", 52),
                 bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(pady=(40, 8))

        tk.Label(wrapper, text="Warehouse Management",
                 font=FONTS["heading_lg"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_white"]).pack()
        tk.Label(wrapper, text="Hệ thống quản lý kho hàng",
                 font=FONTS["body"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"]).pack(pady=(2, 32))

        # Form card
        card = tk.Frame(wrapper, bg=COLORS["bg_card"],
                        highlightthickness=1, highlightbackground=COLORS["border"])
        card.pack(fill="x", pady=(0, 20))

        inner = tk.Frame(card, bg=COLORS["bg_card"])
        inner.pack(padx=28, pady=28, fill="x")

        # Username
        tk.Label(inner, text="Tên đăng nhập", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")
        self.username_var = tk.StringVar(value="admin")
        user_frame = tk.Frame(inner, bg=COLORS["bg_input"],
                              highlightthickness=1, highlightbackground=COLORS["border"])
        user_frame.pack(fill="x", pady=(4, 16))
        tk.Label(user_frame, text="👤", bg=COLORS["bg_input"],
                 fg=COLORS["text_muted"], font=FONTS["body"], padx=8).pack(side="left")
        self.username_entry = tk.Entry(user_frame, textvariable=self.username_var,
                                      bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                                      insertbackground=COLORS["text_primary"],
                                      relief="flat", bd=0, font=FONTS["body"])
        self.username_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.username_entry.bind("<FocusIn>",
            lambda e: user_frame.config(highlightbackground=COLORS["border_focus"]))
        self.username_entry.bind("<FocusOut>",
            lambda e: user_frame.config(highlightbackground=COLORS["border"]))

        # Password
        tk.Label(inner, text="Mật khẩu", font=FONTS["body_bold"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")
        self.password_var = tk.StringVar(value="admin123")
        pw_frame = tk.Frame(inner, bg=COLORS["bg_input"],
                            highlightthickness=1, highlightbackground=COLORS["border"])
        pw_frame.pack(fill="x", pady=(4, 20))
        tk.Label(pw_frame, text="🔒", bg=COLORS["bg_input"],
                 fg=COLORS["text_muted"], font=FONTS["body"], padx=8).pack(side="left")
        self.password_entry = tk.Entry(pw_frame, textvariable=self.password_var,
                                       show="•", bg=COLORS["bg_input"],
                                       fg=COLORS["text_primary"],
                                       insertbackground=COLORS["text_primary"],
                                       relief="flat", bd=0, font=FONTS["body"])
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.password_entry.bind("<FocusIn>",
            lambda e: pw_frame.config(highlightbackground=COLORS["border_focus"]))
        self.password_entry.bind("<FocusOut>",
            lambda e: pw_frame.config(highlightbackground=COLORS["border"]))
        self.password_entry.bind("<Return>", lambda e: self._login())

        # Login button
        login_btn = tk.Button(inner, text="Đăng nhập",
                              bg=COLORS["accent"], fg="white",
                              activebackground=COLORS["accent_hover"],
                              activeforeground="white",
                              relief="flat", bd=0, padx=0, pady=12,
                              cursor="hand2", font=FONTS["heading_sm"])
        login_btn.pack(fill="x")

        # Hint
        hint = tk.Frame(wrapper, bg=COLORS["bg_dark"])
        hint.pack()
        tk.Label(hint, text="Demo: admin/admin123  |  staff/staff123",
                 font=FONTS["small"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"]).pack()

        
