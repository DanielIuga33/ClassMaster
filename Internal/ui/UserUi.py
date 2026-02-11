import tkinter as tk
from tkinter import messagebox
import json
import os

from Internal.service.GroupService import GroupService
from Internal.service.SettingsService import SettingsService
from Internal.service.StudentService import StudentService
from Internal.ui.ScheduleEditUi import ScheduleEditUi
from Internal.ui.StudentAddUi import StudentAddUi
from Internal.ui.GroupAddUi import GroupAddUi


class UserUi:
    def __init__(self, root, user, user_service, on_logout,
                 settings_service: SettingsService, student_service: StudentService, group_service: GroupService):
        self.root = root
        self.user = user
        self.user_service = user_service
        self.student_service = student_service
        self.group_service = group_service
        self.on_logout = on_logout
        self.settings_service = settings_service

        self.schedule_file = os.path.join("Data", "Schedule.json")
        self.schedule_data = self.load_schedule_data()

        self.colors = self.settings_service.get_colors()

        self.root.title(f"ClassMaster - Panou Control: {user.get_first_name()}")
        self.setup_window(1725, 800)
        self.root.configure(bg=self.colors["bg"])

        # --- Sidebar ---
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar_bg"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        current_rows = self.schedule_data.get("total_rows", 5)
        self.rows_var = tk.IntVar(value=max(2, current_rows))

        # Profil
        profile_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"], pady=30)
        profile_frame.pack(fill="x")
        initials = f"{user.get_first_name()[0]}{user.get_last_name()[0]}".upper()
        tk.Label(profile_frame, text=initials, font=("Segoe UI", 22, "bold"),
                 bg="#4A90E2", fg="white", width=3, height=1).pack()
        tk.Label(profile_frame, text=f"{user.get_first_name()} {user.get_last_name()}",
                 font=("Segoe UI", 11, "bold"), bg=self.colors["sidebar_bg"], fg=self.colors["fg"]).pack(pady=10)

        self.create_menu_button("🏠 Dashboard", self.show_dashboard)
        self.create_menu_button("📅 Orar Interactiv", self.show_schedule)
        self.create_menu_button("👥 Gestiune Studenți", lambda: self.show_students("grade"))
        self.create_menu_button("🏫 Gestiune Grupe", self.show_groups)
        self.create_menu_button("⚙️ Setări Profil", self.show_settings)

        tk.Button(self.sidebar, text="🚪 Deconectare", command=on_logout,
                  font=("Segoe UI", 11), bg="#E74C3C", fg="white", relief="flat",
                  cursor="hand2", pady=10).pack(side="bottom", fill="x", padx=20, pady=20)

        self.main_content = tk.Frame(self.root, bg=self.colors["bg"], padx=40, pady=40)
        self.main_content.pack(side="right", expand=True, fill="both")

        self.show_dashboard()

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 20
        self.root.geometry(f'{int(w)}x{int(h)}+{int(x)}+{int(y)}')

    def create_menu_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, command=command, font=("Segoe UI", 11),
                        bg=self.colors["sidebar_bg"], fg=self.colors["fg"], relief="flat",
                        anchor="w", padx=30, pady=15, cursor="hand2",
                        activebackground=self.colors["hover"], activeforeground=self.colors["fg"])
        btn.pack(fill="x")

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def load_schedule_data(self):
        if os.path.exists(self.schedule_file):
            try:
                with open(self.schedule_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_schedule_data(self):
        os.makedirs("Data", exist_ok=True)
        with open(self.schedule_file, "w") as f: json.dump(self.schedule_data, f, indent=4)

    # --- REPARARE: Funcții de procesare orar ---
    def process_schedule_save(self, cell_id, data):
        """Salvează datele din modalul de orar și reîmprospătează grid-ul."""
        self.schedule_data[f"{cell_id}_raw"] = data
        self.save_schedule_data()
        self.show_schedule()

    def process_schedule_delete(self, cell_id):
        """Șterge o programare din orar."""
        if f"{cell_id}_raw" in self.schedule_data:
            del self.schedule_data[f"{cell_id}_raw"]
            self.save_schedule_data()
            self.show_schedule()

    # --- Secțiunea ORAR ---
    def show_schedule(self):
        self.clear_content()
        header_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="📅 Planificare Orar", font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(side="left")

        rows_control = tk.Frame(header_frame, bg=self.colors["bg"])
        rows_control.pack(side="right")
        tk.Label(rows_control, text="Rânduri:", bg=self.colors["bg"], fg=self.colors["fg"]).pack(side="left", padx=5)

        spin = tk.Spinbox(rows_control, from_=2, to=20, textvariable=self.rows_var,
                          width=5, command=self.update_rows_count,
                          bg=self.colors["input_bg"], fg=self.colors["fg"], relief="flat")
        spin.pack(side="left")

        canvas_container = tk.Frame(self.main_content, bg=self.colors["bg"])
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)

        self.table_container = tk.Frame(self.canvas, bg=self.colors["bg"])
        self.canvas.create_window((0, 0), window=self.table_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.table_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.draw_schedule_grid()

    def update_rows_count(self):
        new_count = self.rows_var.get()
        self.schedule_data["total_rows"] = new_count
        self.save_schedule_data()
        self.draw_schedule_grid()

    def draw_schedule_grid(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        zile = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă"]
        num_rows = self.rows_var.get()

        for i, zi in enumerate(zile):
            self.table_container.grid_columnconfigure(i, weight=1, minsize=180)
            tk.Label(self.table_container, text=zi, font=("Segoe UI", 10, "bold"),
                     bg="#4A90E2", fg="white", pady=10).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row in range(1, num_rows + 1):
            self.table_container.grid_rowconfigure(row, weight=0, minsize=120)
            for col in range(len(zile)):
                zi = zile[col]
                cell_id = f"{zi}_{row}"
                self.render_interactive_cell(self.table_container, row, col, cell_id)

    def render_interactive_cell(self, parent, row, col, cell_id):
        raw_data = self.schedule_data.get(f"{cell_id}_raw", {})
        group_name = raw_data.get('group_name', "")
        time_val = raw_data.get('time', "")

        if group_name:
            bg_color = "#1B2631" if self.settings_service.get_theme() == "dark" else "#EBF5FB"
        else:
            bg_color = self.colors["card_bg"]

        cell_frame = tk.Frame(parent, bg=bg_color, highlightthickness=1,
                              highlightbackground=self.colors["grid_line"])
        cell_frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        time_lbl = tk.Label(cell_frame, text=time_val, font=("Segoe UI", 9, "bold"),
                            bg=bg_color, fg=self.colors["fg"], width=10, anchor="center")
        time_lbl.pack(side="left", fill="y", padx=(5, 0))

        if group_name:
            tk.Frame(cell_frame, width=1, bg=self.colors["grid_line"]).pack(side="left", fill="y", padx=5)
            details_frame = tk.Frame(cell_frame, bg=bg_color)
            details_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)

            tk.Label(details_frame, text=group_name, font=("Segoe UI", 11, "bold"),
                     bg=bg_color, fg=self.colors["fg"], anchor="nw").pack(fill="x")

            students_text = self.get_formatted_students(raw_data)
            tk.Label(details_frame, text=students_text, font=("Segoe UI", 9),
                     bg=bg_color, fg=self.colors["fg"], justify="left",
                     anchor="nw", wraplength=150).pack(fill="both", expand=True)

        for widget in [cell_frame, time_lbl]:
            widget.bind("<Button-1>", lambda e, cid=cell_id: self.open_group_assignment_modal(cid))

    def get_formatted_students(self, data):
        group_id = data.get('group_id')
        if not group_id: return ""
        selected_group = self.group_service.get_group_by_id(group_id)
        student_list_text = ""
        if selected_group:
            ids = selected_group.get_student_ids()
            for s_id in ids[:4]:
                student = self.student_service.get_student_by_id(s_id)
                if student:
                    student_list_text += f"• {student.get_last_name()} {student.get_first_name()}\n"
            if len(ids) > 4:
                student_list_text += f"... și încă {len(ids) - 4}"
        return student_list_text

    def open_group_assignment_modal(self, cell_id):
        current_data = self.schedule_data.get(f"{cell_id}_raw", None)
        ScheduleEditUi(parent=self.root, theme=self.colors, cell_id=cell_id,
                       day=cell_id.split('_')[0], current_data=current_data,
                       on_save=self.process_schedule_save, on_delete=self.process_schedule_delete,
                       group_service=self.group_service, user_id=self.user.get_id_entity())

    # --- Gestiune Studenți & Grupe ---
    def show_students(self, sort_by="grade"):
        self.clear_content()
        header_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 10))
        tk.Label(header_frame, text="👥 Gestiune Studenți", font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(side="left")

        tk.Button(header_frame, text="+ Student Nou", command=self.open_add_student_modal,
                  bg="#2ECC71", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=10, cursor="hand2").pack(side="right")

        sort_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        sort_frame.pack(fill="x", pady=(0, 20))
        for label, criteria in [("Clasă", "grade"), ("Nume", "name"), ("Preț", "price")]:
            tk.Button(sort_frame, text=label, command=lambda c=criteria: self.show_students(c),
                      bg=self.colors["sidebar_bg"], fg=self.colors["fg"], relief="flat", padx=12).pack(side="left",
                                                                                                       padx=5)

        table_frame = tk.Frame(self.main_content, bg=self.colors["card_bg"],
                               highlightthickness=1, highlightbackground=self.colors["grid_line"])
        table_frame.pack(fill="x")

        headers = ["Nume și Prenume", "Clasă", "Preț / h", "Acțiuni"]
        for i, h in enumerate(headers):
            table_frame.grid_columnconfigure(i, weight=1)
            tk.Label(table_frame, text=h, font=("Segoe UI", 11, "bold"),
                     bg=self.colors["input_bg"], fg=self.colors["fg"], pady=15).grid(row=0, column=i, sticky="nsew")

        students = self.student_service.get_sorted_students(self.user.get_id_entity(), sort_by)
        for idx, s in enumerate(students):
            row_idx = idx + 2
            bg_color = self.colors["card_bg"] if idx % 2 == 0 else (
                "#1B1B1B" if self.settings_service.get_theme() == "dark" else "#F1F2F6")

            tk.Label(table_frame, text=f"{s.get_last_name()} {s.get_first_name()}", font=("Segoe UI", 11),
                     bg=bg_color, fg=self.colors["fg"], pady=15, padx=15, anchor="w").grid(row=row_idx, column=0,
                                                                                           sticky="nsew")
            tk.Label(table_frame, text=s.get_grade(), font=("Segoe UI", 11), bg=bg_color, fg=self.colors["fg"]).grid(
                row=row_idx, column=1, sticky="nsew")
            tk.Label(table_frame, text=f"{s.get_price()} RON", font=("Segoe UI", 11, "bold"), bg=bg_color,
                     fg="#27AE60").grid(row=row_idx, column=2, sticky="nsew")

            act_f = tk.Frame(table_frame, bg=bg_color)
            act_f.grid(row=row_idx, column=3, sticky="nsew")
            btns = tk.Frame(act_f, bg=bg_color)
            btns.place(relx=0.5, rely=0.5, anchor="center")
            tk.Button(btns, text=" ✏️ ", bg="#F1C40F", relief="flat",
                      command=lambda st=s: self.open_edit_student_modal(st)).pack(side="left", padx=2)
            tk.Button(btns, text=" 🗑️ ", bg="#E74C3C", relief="flat",
                      command=lambda st=s: self.handle_delete_student(st)).pack(side="left", padx=2)

    def show_groups(self):
        self.clear_content()
        header_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="🏫 Gestiune Grupe", font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(side="left")

        tk.Button(header_frame, text="+ Grupă Nouă", command=self.open_add_group_modal,
                  bg="#9B59B6", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=20, pady=10).pack(side="right")

        table_frame = tk.Frame(self.main_content, bg=self.colors["card_bg"],
                               highlightthickness=1, highlightbackground=self.colors["grid_line"])
        table_frame.pack(fill="x")

        headers = ["Nume Grupă", "Membri & Tarife", "Total / Ședință", "Acțiuni"]
        for i, h in enumerate(headers):
            table_frame.grid_columnconfigure(i, weight=1)
            tk.Label(table_frame, text=h, font=("Segoe UI", 11, "bold"),
                     bg=self.colors["input_bg"], fg=self.colors["fg"], pady=15).grid(row=0, column=i, sticky="nsew")

        groups = self.group_service.get_groups_for_teacher(self.user.get_id_entity())
        for idx, g in enumerate(groups):
            row_idx = idx + 2
            bg_color = self.colors["card_bg"] if idx % 2 == 0 else (
                "#1B1B1B" if self.settings_service.get_theme() == "dark" else "#FBFCFD")
            tk.Label(table_frame, text=g.get_group_name(), font=("Segoe UI", 11, "bold"),
                     bg=bg_color, fg=self.colors["fg"], pady=20).grid(row=row_idx, column=0, sticky="nsew")

            members_info = ""
            total_p = 0
            for s_id in g.get_student_ids():
                s = self.student_service.get_student_by_id(s_id)
                if s:
                    members_info += f"• {s.get_last_name()} ({s.get_price()} RON)\n"
                    total_p += s.get_price()

            tk.Label(table_frame, text=members_info.strip(), font=("Segoe UI", 10), bg=bg_color,
                     fg=self.colors["fg"]).grid(row=row_idx, column=1)
            tk.Label(table_frame, text=f"{total_p} RON", font=("Segoe UI", 11, "bold"), bg=bg_color, fg="#27AE60").grid(
                row=row_idx, column=2)

            act_f = tk.Frame(table_frame, bg=bg_color)
            act_f.grid(row=row_idx, column=3, sticky="nsew")
            btns = tk.Frame(act_f, bg=bg_color)
            btns.place(relx=0.5, rely=0.5, anchor="center")
            tk.Button(btns, text=" ✏️ ", bg="#F1C40F", relief="flat",
                      command=lambda gr=g: self.open_edit_group_modal(gr)).pack(side="left", padx=2)
            tk.Button(btns, text=" 🗑️ ", bg="#E74C3C", relief="flat",
                      command=lambda gr=g: self.handle_delete_group(gr)).pack(side="left", padx=2)

    def open_add_student_modal(self):
        StudentAddUi(parent=self.root, theme=self.colors, user_id=self.user.get_id_entity(),
                     student_service=self.student_service, on_success=self.show_students)

    def open_edit_student_modal(self, student):
        messagebox.showinfo("Editare", f"Vei edita datele lui {student.get_last_name()} {student.get_first_name()}")

    def handle_delete_student(self, student):
        if messagebox.askyesno("Confirmare", f"Ștergi studentul {student.get_last_name()} {student.get_first_name()}?"):
            self.student_service.delete_student(student)
            self.show_students()

    def open_add_group_modal(self):
        GroupAddUi(parent=self.root, theme=self.colors, user_id=self.user.get_id_entity(),
                   group_service=self.group_service, student_service=self.student_service, on_success=self.show_groups)

    def open_edit_group_modal(self, group):
        messagebox.showinfo("Info", f"Editare grupa: {group.get_group_name()}")

    def handle_delete_group(self, group):
        if messagebox.askyesno("Confirmare", f"Ștergi grupa {group.get_group_name()}?"):
            self.group_service.delete_group(group.get_id_entity())
            self.show_groups()

    # --- Dashboard & Alte secțiuni ---
    def show_dashboard(self):
        self.clear_content()
        tk.Label(self.main_content, text=f"Salutare, {self.user.get_first_name()}!", font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(anchor="w")
        cards_frame = tk.Frame(self.main_content, bg=self.colors["bg"])
        cards_frame.pack(fill="x", pady=30)
        self.create_stat_card(cards_frame, "Studenți Activi",
                              str(len(self.student_service.get_students_for_teacher(self.user.get_id_entity()))),
                              "#4A90E2", 0)

    def create_stat_card(self, parent, title, value, color, col):
        card = tk.Frame(parent, bg=self.colors["card_bg"], highlightthickness=1,
                        highlightbackground=self.colors["grid_line"], padx=20, pady=20)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        tk.Label(card, text=title, font=("Segoe UI", 10), bg=self.colors["card_bg"], fg="#888").pack()
        tk.Label(card, text=value, font=("Segoe UI", 22, "bold"), bg=self.colors["card_bg"], fg=color).pack()

    def show_settings(self):
        self.clear_content()
        tk.Label(self.main_content, text="⚙️ Setări Profil", font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(anchor="w")