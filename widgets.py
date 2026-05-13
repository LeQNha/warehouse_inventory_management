import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS, PADDING


def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Custom.Treeview",
        background=COLORS["table_bg"],
        foreground=COLORS["text_primary"],
        fieldbackground=COLORS["table_bg"],
        borderwidth=0,
        rowheight=32,
        font=FONTS["body"],
    )
    style.configure("Custom.Treeview.Heading",
        background=COLORS["table_header"],
        foreground=COLORS["text_secondary"],
        relief="flat",
        font=FONTS["heading_sm"],
        padding=(8, 6),
    )
    style.map("Custom.Treeview",
        background=[("selected", COLORS["bg_selected"])],
        foreground=[("selected", COLORS["text_white"])],
    )
    style.map("Custom.Treeview.Heading",
        background=[("active", COLORS["bg_hover"])],
    )

    style.configure("TScrollbar",
        background=COLORS["bg_input"],
        troughcolor=COLORS["bg_dark"],
        borderwidth=0,
        relief="flat",
    )
    style.configure("TCombobox",
        fieldbackground=COLORS["bg_input"],
        background=COLORS["bg_input"],
        foreground=COLORS["text_primary"],
        selectbackground=COLORS["accent"],
        borderwidth=1,
        relief="flat",
    )
    style.map("TCombobox",
        fieldbackground=[("readonly", COLORS["bg_input"])],
        foreground=[("readonly", COLORS["text_primary"])],
    )


class PrimaryButton(tk.Button):
    def __init__(self, master, text, command=None, icon="", color=None, **kw):
        bg = color or COLORS["accent"]
        super().__init__(
            master,
            text=f"{icon}  {text}" if icon else text,
            command=command,
            bg=bg,
            fg=COLORS["text_white"],
            activebackground=COLORS["accent_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            font=FONTS["body_bold"],
            **kw
        )
        self.bind("<Enter>", lambda e: self.config(bg=COLORS["accent_hover"] if not color else bg))
        self.bind("<Leave>", lambda e: self.config(bg=bg))


class DangerButton(PrimaryButton):
    def __init__(self, master, text, command=None, icon="", **kw):
        super().__init__(master, text, command, icon, color=COLORS["danger"], **kw)


class SecondaryButton(tk.Button):
    def __init__(self, master, text, command=None, icon="", **kw):
        super().__init__(
            master,
            text=f"{icon}  {text}" if icon else text,
            command=command,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            font=FONTS["body_bold"],
            **kw
        )


class StyledEntry(tk.Entry):
    def __init__(self, master, placeholder="", **kw):
        super().__init__(
            master,
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            relief="flat",
            bd=0,
            font=FONTS["body"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["border_focus"],
            **kw
        )
        self._placeholder = placeholder
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg=COLORS["text_muted"])
            self.bind("<FocusIn>", self._on_focus_in)
            self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, e):
        if self.get() == self._placeholder:
            self.delete(0, "end")
            self.config(fg=COLORS["text_primary"])

    def _on_focus_out(self, e):
        if not self.get():
            self.insert(0, self._placeholder)
            self.config(fg=COLORS["text_muted"])

    def get_value(self):
        val = self.get()
        return "" if val == self._placeholder else val


class StyledLabel(tk.Label):
    def __init__(self, master, text, size="body", color=None, **kw):
        super().__init__(
            master,
            text=text,
            bg=kw.pop("bg", COLORS["bg_card"]),
            fg=color or COLORS["text_primary"],
            font=FONTS.get(size, FONTS["body"]),
            **kw
        )


class Card(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(
            master,
            bg=COLORS["bg_card"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            **kw
        )


class StatCard(tk.Frame):
    def __init__(self, master, label, value, icon, color, **kw):
        super().__init__(master, bg=COLORS["bg_card"],
                         highlightthickness=1,
                         highlightbackground=COLORS["border"], **kw)
        self.config(padx=20, pady=16)

        top = tk.Frame(self, bg=COLORS["bg_card"])
        top.pack(fill="x")

        tk.Label(top, text=icon, font=("Segoe UI", 22), bg=color,
                 fg="white", width=3, pady=4).pack(side="left", padx=(0, 12))

        right = tk.Frame(top, bg=COLORS["bg_card"])
        right.pack(side="left", fill="both")

        self.val_label = tk.Label(right, text=str(value),
                                  font=FONTS["heading_lg"],
                                  bg=COLORS["bg_card"], fg=COLORS["text_white"])
        self.val_label.pack(anchor="w")
        tk.Label(right, text=label, font=FONTS["small"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"]).pack(anchor="w")

    def update_value(self, value):
        self.val_label.config(text=str(value))


class SearchBar(tk.Frame):
    def __init__(self, master, on_search=None, placeholder="Tìm kiếm...", **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.on_search = on_search

        container = tk.Frame(self, bg=COLORS["bg_input"],
                              highlightthickness=1, highlightbackground=COLORS["border"])
        container.pack(fill="x")

        tk.Label(container, text="🔍", bg=COLORS["bg_input"],
                 fg=COLORS["text_muted"], font=FONTS["body"], padx=8).pack(side="left")

        self.entry = StyledEntry(container, placeholder=placeholder)
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.entry.bind("<KeyRelease>", self._on_key)

        if on_search:
            PrimaryButton(container, "Tìm", command=self._do_search).pack(side="right", padx=4, pady=4)

    def _on_key(self, e):
        if self.on_search:
            self.on_search(self.entry.get_value())

    def _do_search(self):
        if self.on_search:
            self.on_search(self.entry.get_value())

    def get(self):
        return self.entry.get_value()


def make_table(parent, columns, show="headings"):
    apply_treeview_style()

    frame = tk.Frame(parent, bg=COLORS["bg_dark"])
    frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame, columns=columns, show=show, style="Custom.Treeview")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    # Alternating row colors
    tree.tag_configure("odd",  background=COLORS["table_bg"])
    tree.tag_configure("even", background=COLORS["table_row_alt"])
    tree.tag_configure("low",  background="#2A1A1A", foreground=COLORS["accent_orange"])
    tree.tag_configure("ok",   background=COLORS["table_bg"])

    return tree


def page_header(parent, title, subtitle=""):
    hdr = tk.Frame(parent, bg=COLORS["bg_dark"])
    hdr.pack(fill="x", pady=(0, 16))
    tk.Label(hdr, text=title, font=FONTS["heading_xl"],
             bg=COLORS["bg_dark"], fg=COLORS["text_white"]).pack(anchor="w")
    if subtitle:
        tk.Label(hdr, text=subtitle, font=FONTS["body"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_secondary"]).pack(anchor="w")
    tk.Frame(hdr, bg=COLORS["border"], height=1).pack(fill="x", pady=(8, 0))
