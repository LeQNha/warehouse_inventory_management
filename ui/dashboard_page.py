import tkinter as tk
from theme import COLORS, FONTS
from widgets import StatCard, Card, page_header


class DashboardPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        