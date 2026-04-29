import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Internal.service.SettingsService import SettingsService
from Internal.service.StudentService import StudentService
from Internal.service.LanguageService import LanguageService
from Internal.utils.utils import to_uppercase, validate_roman_entry


class StudentAddUi(tk.Toplevel):
    def __init__(self, parent, theme, user_id, student_service: StudentService, on_success,
                 settings_service: SettingsService, lang_service: LanguageService):
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        self.student_service = student_service
        self.on_success = on_success
        self.settings_service = settings_service
        self.lang_service = lang_service

        uid = self.user_id
        ls = self.lang_service

        self.colors = self.settings_service.get_colors(uid)
        self.txt_color = self.colors.get("schedule_text", self.colors["fg"])

        self.configure(bg=self.colors["bg"])

        self.vcmd_roman = (self.register(validate_roman_entry), '%S')

        # Titlu fereastră tradus
        self.title(ls.get_text(uid, "student_add_title"))
        self.setup_modal(350, 520)
        self.configure(padx=25, pady=25)
        self.grab_set()

        # Titlu Header tradus
        tk.Label(self, text=f"👤 {ls.get_text(uid, 'student_add_header')}", font=("Segoe UI", 16, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=(0, 20))

        # Câmpuri
        self.entries = {}

        # Nume și Prenume traduse
        self.create_field(ls.get_text(uid, "reg_last_name"), "ln")
        self.create_field(ls.get_text(uid, "reg_first_name"), "fn")

        # Câmpul Clasă cu validare ROMANĂ și instrucțiuni traduse
        tk.Label(self, text=ls.get_text(uid, "student_grade_label"), bg=self.colors["bg"],
                 fg=self.txt_color, font=("Segoe UI", 9, "bold")).pack(anchor="w")

        t_controls = tk.Frame(self, relief="flat",
                             bg=self.colors["input_bg"])
        t_controls.pack(fill="x", pady=(0, 15))

        self.grade_combo = ttk.Combobox(t_controls, values=[
            "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
        ], state="readonly", width=100, font=("Segoe UI", 11))
        self.grade_combo.pack(side="left")#, padx=20)
        self.grade_combo.bind("<<ComboboxSelected>>", self.update_grade_preview)

        # Câmpul Preț tradus
        self.create_field(ls.get_text(uid, "col_price_h"), "pr")

        # Buton Salvare tradus
        tk.Button(self, text=ls.get_text(uid, "btn_save_student"), command=self.handle_save,
                  bg=self.colors.get("success", "#2ECC71"), fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(15, 0))

    def create_field(self, label_text, key):
        """Helper pentru crearea câmpurilor cu contrast corect."""
        tk.Label(self, text=label_text, bg=self.colors["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                       bg=self.colors["input_bg"],
                       fg=self.txt_color,
                       insertbackground=self.txt_color)
        ent.pack(fill="x", pady=(5, 15), ipady=5)
        self.entries[key] = ent

    def update_grade_preview(self, event=None):
        c = self.grade_combo.get()
        self.entries["gr"] = c
        if not c:
            return
        print(c)

    def setup_modal(self, w, h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def handle_save(self):
        uid = self.user_id
        ls = self.lang_service
        fn = self.entries['fn'].get().strip()
        ln = self.entries['ln'].get().strip()
        gr = self.entries['gr']
        pr = self.entries['pr'].get().strip()

        if not all([gr, pr]):
            messagebox.showwarning(ls.get_text(uid, "warning"), ls.get_text(uid, "err_fill_fields"))
            return

        res = self.student_service.add_student(fn, ln, gr, pr, uid)

        if res[0] == 201:
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror(ls.get_text(uid, "error"), res[1])
