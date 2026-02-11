import tkinter as tk
from tkinter import messagebox, ttk

from Internal.service.GroupService import GroupService
from Internal.service.StudentService import StudentService


class GroupAddUi(tk.Toplevel):
    def __init__(self, parent, theme, user_id, group_service: GroupService, student_service: StudentService,
                 on_success):
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        self.group_service = group_service
        self.student_service = student_service
        self.on_success = on_success

        self.title("Creare Grupă Nouă")
        self.setup_modal(450, 650)
        self.configure(bg=theme["bg"], padx=25, pady=25)
        self.grab_set()

        # Titlu
        tk.Label(self, text="🏫 Grupă Nouă", font=("Segoe UI", 16, "bold"),
                 bg=theme["bg"], fg="#9B59B6").pack(pady=(0, 20))

        # Câmpuri text
        self.entries = {}
        fields = [("Nume Grupă", "name")]

        for label_text, key in fields:
            tk.Label(self, text=label_text, bg=theme["bg"], fg=theme["fg"],
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                           bg="#F0F2F5" if theme["bg"] != "#121212" else "#333",
                           fg=theme["fg"], insertbackground=theme["fg"])
            ent.pack(fill="x", pady=(5, 10), ipady=5)
            self.entries[key] = ent

        # Secțiune Selecție Studenți
        tk.Label(self, text="Selectează Studenții (doar cei nealocați):", bg=theme["bg"], fg=theme["fg"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 5))

        # Listbox cu Scrollbar pentru studenți
        list_frame = tk.Frame(self, bg=theme["bg"])
        list_frame.pack(fill="both", expand=True)

        self.student_listbox = tk.Listbox(list_frame, selectmode="multiple", font=("Segoe UI", 10),
                                          bg=self.entries["name"]["bg"], fg=theme["fg"],
                                          relief="flat", highlightthickness=0)
        self.student_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.student_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.student_listbox.yview)

        # REPARARE: Populăm lista doar cu studenții disponibili (nealocați)
        self.all_students = self.load_available_students()

        for s in self.all_students:
            self.student_listbox.insert(tk.END, f" {s.get_last_name()} {s.get_first_name()} ({s.get_grade()})")

        # Buton Salvare
        tk.Button(self, text="Salvează Grupa", command=self.handle_save,
                  bg="#9B59B6", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(20, 0))

    def load_available_students(self):
        """Filtrează studenții pentru a returna doar pe cei care nu sunt în nicio grupă."""
        all_students = self.student_service.get_students_for_teacher(self.user_id)
        all_groups = self.group_service.get_groups_for_teacher(self.user_id)

        # Colectăm ID-urile studenților deja alocați
        assigned_student_ids = set()
        for group in all_groups:
            assigned_student_ids.update(group.get_student_ids())

        # Păstrăm doar studenții care NU sunt în nicio grupă
        available_students = [
            s for s in all_students
            if s.get_id_entity() not in assigned_student_ids
        ]

        # Îi sortăm alfabetic pentru o experiență mai bună
        return sorted(available_students, key=lambda s: (s.get_last_name(), s.get_first_name()))

    def handle_save(self):
        name = self.entries['name'].get().strip()

        # Obținem ID-urile studenților selectați
        selected_indices = self.student_listbox.curselection()
        student_ids = [self.all_students[i].get_id_entity() for i in selected_indices]

        if not name:
            messagebox.showwarning("Atenție", "Numele grupei este obligatoriu!")
            return

        if not student_ids:
            if not messagebox.askyesno("Confirmare", "Vrei să creezi grupa fără niciun student?"):
                return

        res = self.group_service.add_group(name, student_ids, self.user_id)

        if res[0] == 201:
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Eroare", res[1])

    def setup_modal(self, w, h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')