import tkinter as tk
from tkinter import messagebox

from Internal.service.SettingsService import SettingsService
from Internal.service.StudentService import StudentService


class StudentAddUi(tk.Toplevel):
    def __init__(self, parent, theme, user_id, student_service: StudentService, on_success,
                 settings_service: SettingsService):
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        self.student_service = student_service
        self.on_success = on_success
        self.settings_service = settings_service

        # Preluăm setul complet de culori și culoarea de contrast dedicată
        self.colors = self.settings_service.get_colors(self.user_id)
        self.txt_color = self.colors.get("schedule_text", self.colors["fg"])

        self.configure(bg=self.colors["bg"])

        # Înregistrăm funcția de validare pentru caractere romane
        self.vcmd_roman = (self.register(self.validate_roman_entry), '%S')

        self.title("Adaugă Student Nou")
        self.setup_modal(350, 520)
        self.configure(padx=25, pady=25)
        self.grab_set()

        # Titlu - Folosim culoarea de accent pentru consistență vizuală
        tk.Label(self, text="👤 Student Nou", font=("Segoe UI", 16, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=(0, 20))

        # Câmpuri
        self.entries = {}

        # Câmpul Nume
        self.create_field("Nume", "ln")

        # Câmpul Prenume
        self.create_field("Prenume", "fn")

        # Câmpul Clasă cu validare ROMANĂ
        tk.Label(self, text="Clasă (Cifre Romane: I, V, X...)", bg=self.colors["bg"],
                 fg=self.txt_color, font=("Segoe UI", 9, "bold")).pack(anchor="w")

        # REPARARE FUNDAL: Folosim input_bg din temă și culoarea forțată de text
        grade_ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                             bg=self.colors["input_bg"],
                             fg=self.txt_color,
                             insertbackground=self.txt_color,
                             validate='key', validatecommand=self.vcmd_roman)
        grade_ent.pack(fill="x", pady=(5, 15), ipady=5)

        # Transformăm automat în majuscule
        grade_ent.bind("<KeyRelease>", lambda e: self.to_uppercase(grade_ent))
        self.entries["gr"] = grade_ent

        # Câmpul Preț
        self.create_field("Preț Ședință (RON)", "pr")

        # Buton Salvare - Folosim culoarea success din temă
        tk.Button(self, text="Salvează Student", command=self.handle_save,
                  bg=self.colors.get("success", "#2ECC71"), fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(15, 0))

    def create_field(self, label_text, key):
        """Helper pentru crearea câmpurilor cu contrast corect."""
        tk.Label(self, text=label_text, bg=self.colors["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        # Eliminăm culorile hardcoded (#E8F0FE / #333)
        ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                       bg=self.colors["input_bg"],
                       fg=self.txt_color,
                       insertbackground=self.txt_color)
        ent.pack(fill="x", pady=(5, 15), ipady=5)
        self.entries[key] = ent

    def validate_roman_entry(self, char):
        """Permite doar caracterele romane valide."""
        allowed_chars = "IVXLCDMivxlcdm"
        return char in allowed_chars

    def to_uppercase(self, widget):
        """Transformă textul în majuscule în timp real."""
        pos = widget.index(tk.INSERT)
        current_text = widget.get().upper()
        widget.delete(0, tk.END)
        widget.insert(0, current_text)
        widget.icursor(pos)

    def setup_modal(self, w, h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def handle_save(self):
        fn = self.entries['fn'].get().strip()
        ln = self.entries['ln'].get().strip()
        gr = self.entries['gr'].get().strip()
        pr = self.entries['pr'].get().strip()

        if not all([gr, pr]):
            messagebox.showwarning("Atenție", "Toate câmpurile sunt obligatorii!")
            return

        res = self.student_service.add_student(fn, ln, gr, pr, self.user_id)

        if res[0] == 201:
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Eroare", res[1])
