import tkinter as tk


class PresetSaveUi(tk.Toplevel):
    def __init__(self, parent, colors, callback):
        super().__init__(parent)
        self.colors = colors
        self.callback = callback
        # Preluăm culoarea de contrast (Alb pe Dark / Negru pe Light)
        self.txt_color = colors.get("schedule_text", "#FFFFFF")

        self.title("Salvare Preset")
        self.setup_modal(380, 240)
        self.configure(bg=colors["bg"], padx=30, pady=25)
        self.grab_set()

        # Titlu stilizat cu culoarea de accent a temei
        tk.Label(self, text="💾 Salvare Preset Nou", font=("Segoe UI", 14, "bold"),
                 bg=colors["bg"], fg=colors["accent"]).pack(pady=(0, 15))

        tk.Label(self, text="Introdu numele presetului:", font=("Segoe UI", 10),
                 bg=colors["bg"], fg=self.txt_color).pack(anchor="w")

        # Input modern care folosește culorile temei tale
        self.entry_name = tk.Entry(self, font=("Segoe UI", 12), relief="flat",
                                   bg=colors["input_bg"], fg=self.txt_color,
                                   insertbackground=self.txt_color)
        self.entry_name.pack(fill="x", pady=15, ipady=7)
        self.entry_name.focus_set()

        # Container Butoane
        btn_frame = tk.Frame(self, bg=colors["bg"])
        btn_frame.pack(fill="x", pady=(10, 0))

        # Buton Confirmare - Folosește culoarea de succes din SettingsService
        tk.Button(btn_frame, text="Confirmă", font=("Segoe UI", 10, "bold"),
                  bg=colors.get("success", "#2ECC71"), fg="white", relief="flat",
                  command=self.confirm, width=12, cursor="hand2").pack(side="right", padx=(10, 0))

        tk.Button(btn_frame, text="Anulează", font=("Segoe UI", 10),
                  bg=colors["card_bg"], fg=self.txt_color, relief="flat",
                  command=self.destroy, width=10, cursor="hand2").pack(side="right")

        # Scurtături de la tastatură pentru viteză
        self.bind('<Return>', lambda e: self.confirm())
        self.bind('<Escape>', lambda e: self.destroy())

    def confirm(self):
        name = self.entry_name.get().strip()
        if name:
            self.callback(name)
            self.destroy()

    def setup_modal(self, w, h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')