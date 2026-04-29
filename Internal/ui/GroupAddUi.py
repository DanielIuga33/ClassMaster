import tkinter as tk
from tkinter import messagebox
from Internal.service.GroupService import GroupService
from Internal.service.StudentService import StudentService
from Internal.service.LanguageService import LanguageService


class GroupAddUi(tk.Toplevel):
    def __init__(self, parent, theme, user_id, group_service: GroupService, student_service: StudentService,
                 on_success, lang_service: LanguageService):
        super().__init__(parent)
        self.theme = theme
        self.user_id = user_id
        self.group_service = group_service
        self.student_service = student_service
        self.lang_service = lang_service
        self.on_success = on_success

        uid = self.user_id
        ls = self.lang_service
        self.txt_color = theme.get("schedule_text", theme["fg"])

        # Titlu fereastră tradus
        self.title(ls.get_text(uid, "group_add_title"))
        self.setup_modal(450, 650)
        self.configure(bg=theme["bg"], padx=25, pady=25)
        self.grab_set()

        # Titlu Header tradus
        tk.Label(self, text=f"🏫 {ls.get_text(uid, 'group_add_header')}", font=("Segoe UI", 16, "bold"),
                 bg=theme["bg"], fg="#9B59B6").pack(pady=(0, 20))

        # Câmpuri text
        self.entries = {}
        # Eticheta "Nume Grupă" tradusă prin cheia col_group_name
        fields = [(ls.get_text(uid, "col_group_name"), "name")]

        for label_text, key in fields:
            tk.Label(self, text=label_text, bg=theme["bg"], fg=self.txt_color,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")

            ent = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                           bg=theme["input_bg"],
                           fg=self.txt_color,
                           insertbackground=self.txt_color)
            ent.pack(fill="x", pady=(5, 10), ipady=5)
            self.entries[key] = ent

        # Secțiune Selecție Studenți tradusă
        tk.Label(self, text=ls.get_text(uid, "group_select_students"), bg=theme["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 5))

        # Listbox cu Scrollbar
        list_frame = tk.Frame(self, bg=theme["bg"])
        list_frame.pack(fill="both", expand=True)

        self.student_listbox = tk.Listbox(list_frame, selectmode="multiple", font=("Segoe UI", 10),
                                          bg=theme["input_bg"],
                                          fg=self.txt_color,
                                          selectbackground=theme["accent"],
                                          selectforeground="white",
                                          relief="flat", highlightthickness=0)
        self.student_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.student_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.student_listbox.yview)

        self.all_students = self.load_available_students()

        for s in self.all_students:
            self.student_listbox.insert(tk.END, f"  {s.get_last_name()} {s.get_first_name()} ({s.get_grade()})")


        self.all_students = self.load_available_students()
        # Salvăm copia originală pentru resetare
        self.original_students = list(self.all_students)

        # Inserăm elevii inițiali
        self.refresh_listbox(self.all_students)

        # Legăm evenimentul de selecție
        self.student_listbox.bind("<<ListboxSelect>>", self.handle_filter_logic)


        # Buton Salvare tradus
        tk.Button(self, text=ls.get_text(uid, "btn_save_group"), command=self.handle_save,
                  bg="#9B59B6", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", pady=12, cursor="hand2").pack(fill="x", pady=(20, 0))

    def handle_filter_logic(self, event):
        selected_indices = self.student_listbox.curselection()

        # Dacă nu mai e nimic selectat, resetăm lista la toți elevii disponibili
        if not selected_indices:
            self.all_students = list(self.original_students)
            self.refresh_listbox(self.all_students)
            return

        # Dacă avem cel puțin un element selectat, filtrăm după clasa primului
        # Luăm primul index selectat
        first_selected_index = selected_indices[0]
        selected_grade = self.all_students[first_selected_index].get_grade()

        # Filtrăm: păstrăm elevii care au aceeași clasă SAU care sunt deja selectați
        # (pentru a nu-i pierde din selecție în timpul procesării)
        selected_ids = [self.all_students[i].get_id_entity() for i in selected_indices]

        filtered_students = [
            s for s in self.original_students
            if s.get_grade() == selected_grade or s.get_id_entity() in selected_ids
        ]

        # Dacă lista filtrată e diferită de cea curentă, actualizăm
        if len(filtered_students) != len(self.all_students):
            self.all_students = filtered_students
            self.refresh_listbox(self.all_students, selected_ids)

    def refresh_listbox(self, students_to_show, ids_to_reselect=None):
        """Reîmprospătează elementele din Listbox."""
        self.student_listbox.delete(0, tk.END)
        for s in students_to_show:
            self.student_listbox.insert(tk.END, f"  {s.get_last_name()} {s.get_first_name()} ({s.get_grade()})")

        # Re-selectăm elevii care erau deja bifați
        if ids_to_reselect:
            for i, s in enumerate(students_to_show):
                if s.get_id_entity() in ids_to_reselect:
                    self.student_listbox.selection_set(i)

    def handle_save(self):
        uid = self.user_id
        ls = self.lang_service
        name = self.entries['name'].get().strip()
        selected_indices = self.student_listbox.curselection()
        student_ids = [self.all_students[i].get_id_entity() for i in selected_indices]
        grade = self.all_students[selected_indices[0]].get_grade()

        if not name:
            # Mesaj avertisment tradus
            messagebox.showwarning(ls.get_text(uid, "warning"), ls.get_text(uid, "err_group_name_req"))
            return

        if not student_ids:
            # Întrebare confirmare tradusă
            if not messagebox.askyesno(ls.get_text(uid, "confirmation"), ls.get_text(uid, "msg_empty_group_confirm")):
                return

        res = self.group_service.add_group(name, grade, student_ids, self.user_id)

        if res[0] == 201:
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror(ls.get_text(uid, "error"), res[1])

    def load_available_students(self):
        all_students = self.student_service.get_students_for_teacher(self.user_id)
        all_groups = self.group_service.get_groups_for_teacher(self.user_id)
        assigned_student_ids = set()
        for group in all_groups:
            assigned_student_ids.update(group.get_student_ids())
        available_students = [s for s in all_students if s.get_id_entity() not in assigned_student_ids]
        return sorted(available_students, key=lambda s: (s.get_grade(), s.get_last_name(), s.get_first_name()))

    def setup_modal(self, w, h):
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
