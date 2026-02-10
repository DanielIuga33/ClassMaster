import tkinter as tk
import json
import os


class UserUi:
    def __init__(self, root):
        self.root = root
        self.root.title("Manager Meditații v1.0")
        self.root.geometry("400x300")

        # Încărcăm datele la pornire
        self.date = self.incarca_date()

        # Interfața Simplă
        tk.Label(root, text="Nume Elev:").pack()
        self.entry_nume = tk.Entry(root)
        self.entry_nume.pack()

        tk.Label(root, text="Suma (RON):").pack()
        self.entry_suma = tk.Entry(root)
        self.entry_suma.pack()

        tk.Button(root, text="Salvează Ședința", command=self.salveaza).pack(pady=10)

        self.label_status = tk.Label(root, text=f"Total acumulat: {self.date.get('total', 0)} RON")
        self.label_status.pack()
