import tkinter as tk
from tkinter import ttk, messagebox
from theme import COLORS, FONTS

class StockInPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self.products  = {}
        self.suppliers = {}
        
class StockOutPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        self.products = {}
        