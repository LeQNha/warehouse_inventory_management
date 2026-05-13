import tkinter as tk
from tkinter import ttk
from theme import COLORS, FONTS

class SearchPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user