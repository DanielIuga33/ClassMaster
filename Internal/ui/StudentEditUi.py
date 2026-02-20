import tkinter as tk
from Internal.entity.Student import Student
from Internal.service.StudentService import StudentService
from Internal.service.LanguageService import LanguageService  # Import necesar pentru localizare


class StudentEditUi(tk.Toplevel):
    def __init__(self, parent, theme, student: Student, student_service: StudentService, on_success,
                 lang_service: LanguageService):
        super().__init__(parent)
        self.student = student
        self.theme = theme
        self.student_service = student_service
        self.on_success = on_success
        self.lang_service = lang_service  # Injectăm serviciul de limbă

        uid = student.get_teacher_id()
        ls = self.lang_service
        self.txt_color = theme.get("schedule_text", "#FFFFFF")

        # Titlu fereastră tradus dinamic
        win_title = ls.get_text(uid, "student_edit_window_title").replace("{name}", student.get_first_name())
        self.title(win_title)

        self.setup_modal(400, 600)
        self.configure(bg=theme["bg"], padx=30, pady=25)
        self.grab_set()

        # Titlu Header tradus
        tk.Label(self, text=f"📝 {ls.get_text(uid, 'student_edit_header')}", font=("Segoe UI", 16, "bold"),
                 bg=theme["bg"], fg=theme["accent"]).pack(pady=(0, 20))

        self.entries = {}

        # 1. NUME & PRENUME traduse
        self.create_field(ls.get_text(uid, "reg_last_name"), str(student.get_last_name()), "ln")
        self.create_field(ls.get_text(uid, "reg_first_name"), str(student.get_first_name()), "fn")

        # 3. CLASĂ tradusă
        tk.Label(self, text=ls.get_text(uid, "student_grade_label"), bg=theme["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        ent_gr = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                          bg=theme["input_bg"], fg=self.txt_color,
                          insertbackground=self.txt_color)

        # Extragem valoarea prin scanare sigură a obiectului
        val_clasa = ""
        try:
            val_clasa = student.get_grade()
            if not val_clasa:
                for attr, value in student.__dict__.items():
                    if "grade" in attr:
                        val_clasa = value
                        break
        except:
            pass

        ent_gr.insert(0, str(val_clasa) if val_clasa else "")
        ent_gr.pack(fill="x", pady=(5, 15), ipady=5)
        ent_gr.bind("<KeyRelease>", lambda e: self.to_uppercase(ent_gr))
        self.entries["gr"] = ent_gr

        # 4. PREȚ tradus
        self.create_field(ls.get_text(uid, "col_price_h"), str(student.get_price()), "pr")

        # Buton Salvare tradus
        tk.Button(self, text=ls.get_text(uid, "btn_save_changes"), command=self.handle_save,
                  bg=theme.get("success", "#2ECC71"), fg="white",
                  font=("Segoe UI", 11, "bold"), relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(15, 0))

    def create_field(self, label, value, key):
        tk.Label(self, text=label, bg=self.theme["bg"], fg=self.txt_color, font=("Segoe UI", 9, "bold")).pack(
            anchor="w")
        ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat", bg=self.theme["input_bg"],
                       fg=self.txt_color, insertbackground=self.txt_color)
        ent.insert(0, value)
        ent.pack(fill="x", pady=(5, 15), ipady=5)
        self.entries[key] = ent

    def to_uppercase(self, widget):
        pos = widget.index(tk.INSERT)
        current_text = widget.get().upper()
        widget.delete(0, tk.END)
        widget.insert(0, current_text)
        widget.icursor(pos)

    def handle_save(self):
        """Validăm datele și salvăm folosind mesaje traduse."""
        uid = self.student.get_teacher_id()
        ls = self.lang_service
        new_gr = self.entries["gr"].get().strip().upper()

        # Validare cifre romane cu mesaj tradus
        if new_gr and not all(c in "IVXLCDM" for c in new_gr):
            if hasattr(self.master, 'show_toast'):
                err_msg = ls.get_text(uid, "err_roman_only")
                self.master.show_toast(f"⚠️ {err_msg}", "#E74C3C")
            return

        self.student.set_last_name(self.entries["ln"].get().strip())
        self.student.set_first_name(self.entries["fn"].get().strip())
        self.student.set_grade(new_gr)
        self.student.set_price(int(self.entries["pr"].get().strip()))

        res = self.student_service.modify_student(self.student, self.student)
        if res[0] == 200:
            self.on_success()
            self.destroy()

    def setup_modal(self, w, h):
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{w}x{h}+{int((ws / 2) - (w / 2))}+{int((hs / 2) - (h / 2))}'
                      )