import tkinter as tk
from tkinter import messagebox


class StudentAddUi(tk.Toplevel):
    def __init__(self, parent, theme, user_id, student_service, on_success):
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        self.student_service = student_service
        self.on_success = on_success

        elf.colors = settings_service.get_colors()  # Iei tot setul de culori
        self.configure(bg=self.colors["bg"])

        # Aplicarea culorii gri la input
        self.entry = tk.Entry(self, bg=self.colors["input_bg"], fg=self.colors["fg"])

        # Înregistrăm funcția de validare pentru caractere romane
        self.vcmd_roman = (self.register(self.validate_roman_entry), '%S')

        self.title("Adaugă Student Nou")
        self.setup_modal(350, 520)
        self.configure(bg=theme["bg"], padx=25, pady=25)
        self.grab_set()

        # Titlu
        tk.Label(self, text="👤 Student Nou", font=("Segoe UI", 16, "bold"),
                 bg=theme["bg"], fg="#4A90E2").pack(pady=(0, 20))

        # Câmpuri
        self.entries = {}

        # Câmpul Nume
        self.create_field("Nume", "ln")

        # Câmpul Prenume
        self.create_field("Prenume", "fn")

        # Câmpul Clasă cu validare ROMANĂ
        tk.Label(self, text="Clasă (Cifre Romane: I, V, X...)", bg=theme["bg"],
                 fg=theme["fg"], font=("Segoe UI", 9, "bold")).pack(anchor="w")

        grade_ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                             bg="#E8F0FE" if theme["bg"] != "#121212" else "#333",
                             fg=theme["fg"], insertbackground=theme["fg"],
                             validate='key', validatecommand=self.vcmd_roman)
        grade_ent.pack(fill="x", pady=(5, 15), ipady=5)

        # Transformăm automat în majuscule
        grade_ent.bind("<KeyRelease>", lambda e: self.to_uppercase(grade_ent))
        self.entries["gr"] = grade_ent

        # Câmpul Preț
        self.create_field("Preț Ședință (RON)", "pr")

        # Buton Salvare
        tk.Button(self, text="Salvează Student", command=self.handle_save,
                  bg="#2ECC71", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(15, 0))

    def create_field(self, label_text, key):
        """Helper pentru crearea câmpurilor standard."""
        tk.Label(self, text=label_text, bg=self.theme["bg"], fg=self.theme["fg"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                       bg="#E8F0FE" if self.theme["bg"] != "#121212" else "#333",
                       fg=self.theme["fg"], insertbackground=self.theme["fg"])
        ent.pack(fill="x", pady=(5, 15), ipady=5)
        self.entries[key] = ent

    def validate_roman_entry(self, char):
        """Permite doar caracterele romane valide."""
        allowed_chars = "IVXLCDMivxlcdm"
        if char in allowed_chars:
            return True
        return False

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

        if not all([fn, ln, gr, pr]):
            messagebox.showwarning("Atenție", "Toate câmpurile sunt obligatorii!")
            return

        res = self.student_service.add_student(fn, ln, gr, pr, self.user_id)

        if res[0] == 201:
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Eroare", res[1])