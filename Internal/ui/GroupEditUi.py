import tkinter as tk
from tkinter import messagebox
from Internal.entity.Group import Group
from Internal.service.GroupService import GroupService
from Internal.service.StudentService import StudentService
from Internal.service.LanguageService import LanguageService


class GroupEditUi(tk.Toplevel):
    def __init__(self, parent, theme, group: Group, group_service: GroupService, student_service: StudentService,
                 on_success, lang_service: LanguageService):
        super().__init__(parent)
        self.group = group
        self.theme = theme
        self.group_service = group_service
        self.student_service = student_service
        self.lang_service = lang_service
        self.on_success = on_success

        uid = group.get_teacher_id()
        ls = self.lang_service
        self.txt_color = theme.get("schedule_text", "#FFFFFF")
        self.accent_color = theme.get("accent", "#9B59B6")
        win_title = ls.get_text(uid, "group_edit_window_title").replace("{name}", group.get_group_name())
        self.title(win_title)

        self.setup_modal(450, 650)
        self.configure(bg=theme["bg"], padx=30, pady=25)
        self.grab_set()
        tk.Label(self, text=f"📝 {ls.get_text(uid, 'group_edit_header')}", font=("Segoe UI", 18, "bold"),
                 bg=theme["bg"], fg=self.accent_color).pack(pady=(0, 20))
        tk.Label(self, text=ls.get_text(uid, "col_group_name"), bg=theme["bg"], fg=self.txt_color,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.name_entry = tk.Entry(self, font=("Segoe UI", 11), relief="flat",
                                   bg=theme["input_bg"], fg=self.txt_color,
                                   insertbackground=self.txt_color)
        self.name_entry.insert(0, group.get_group_name())
        self.name_entry.pack(fill="x", pady=(5, 20), ipady=8)
        tk.Label(self, text=ls.get_text(uid, "group_select_members_hint"),
                 bg=theme["bg"], fg=self.txt_color, font=("Segoe UI", 10, "bold")).pack(anchor="w")

        list_container = tk.Frame(self, bg=theme["input_bg"])
        list_container.pack(fill="both", expand=True, pady=5)

        self.student_listbox = tk.Listbox(list_container, selectmode="multiple",
                                          font=("Segoe UI", 10), relief="flat",
                                          bg=theme["input_bg"], fg=self.txt_color,
                                          selectbackground=self.accent_color,
                                          highlightthickness=0)

        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.student_listbox.yview)
        self.student_listbox.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.student_listbox.pack(side="left", fill="both", expand=True)

        self.all_students = self.load_available_students()
        current_members = group.get_student_ids()

        for idx, student in enumerate(self.all_students):
            display_name = f"{student.get_last_name()} {student.get_first_name()} ({student.get_grade()})"
            self.student_listbox.insert(tk.END, display_name)

            if student.get_id_entity() in current_members:
                self.student_listbox.select_set(idx)
        tk.Button(self, text=ls.get_text(uid, "btn_save_changes"), command=self.handle_save,
                  bg=theme.get("success", "#2ECC71"), fg="white",
                  font=("Segoe UI", 12, "bold"), relief="flat",
                  pady=12, cursor="hand2").pack(fill="x", pady=(25, 0))

    def handle_save(self):
        """Salvează modificările și afișează mesaje traduse."""
        uid = self.group.get_teacher_id()
        ls = self.lang_service
        new_name = self.name_entry.get().strip()
        selected_indices = self.student_listbox.curselection()

        if not new_name:
            messagebox.showwarning(ls.get_text(uid, "warning"), ls.get_text(uid, "err_group_name_req"))
            return

        new_student_ids = [self.all_students[i].get_id_entity() for i in selected_indices]

        self.group.set_group_name(new_name)
        self.group.set_student_ids(new_student_ids)

        res = self.group_service.modify_group(self.group, self.group)

        if res[0] == 200:
            self.on_success()
            self.destroy()

    def setup_modal(self, w, h):
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def load_available_students(self):
        uid = self.group.get_teacher_id()
        all_students = self.student_service.get_students_for_teacher(uid)
        all_groups = self.group_service.get_groups_for_teacher(uid)

        assigned_student_ids = set()
        for group in all_groups:
            assigned_student_ids.update(group.get_student_ids())

        available_students = [
            s for s in all_students
            if s.get_id_entity() not in assigned_student_ids
        ]
        for s in all_students:
            if s.get_id_entity() in self.group.get_student_ids() and s not in available_students:
                available_students.append(s)

        return sorted(available_students, key=lambda s: (s.get_grade(), s.get_last_name(), s.get_first_name()))
