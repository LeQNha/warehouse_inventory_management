import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from theme import COLORS, FONTS
from widgets import PrimaryButton, DangerButton, SecondaryButton, SearchBar, make_table, page_header, Card

class ProductsPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user


    