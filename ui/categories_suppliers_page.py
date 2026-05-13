
import tkinter as tk
from theme import COLORS, FONTS


class CategoriesPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user


class CategoryDialog(tk.Toplevel):
    def __init__(self, parent, cat_id, on_save):
        super().__init__(parent)
        self.cat_id = cat_id
        self.on_save = on_save
    
class SuppliersPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
        
