import tkinter as tk
from tkinter import messagebox
from theme import COLORS, FONTS



class UsersPage(tk.Frame):
    def __init__(self, master, current_user, **kw):
        super().__init__(master, bg=COLORS["bg_dark"], **kw)
        self.current_user = current_user
