import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from Internal.service.GroupService import GroupService
from Internal.service.LanguageService import LanguageService
from Internal.service.PresetService import PresetService
from Internal.service.ScheduleService import ScheduleService
from Internal.service.SettingsService import SettingsService
from Internal.service.StudentService import StudentService
from Internal.service.UserService import UserService
from Internal.ui.ScheduleEditUi import ScheduleEditUi
from Internal.ui.StudentAddUi import StudentAddUi
from Internal.ui.GroupAddUi import GroupAddUi
from Internal.ui.PresetSaveUi import PresetSaveUi
from Internal.ui.components.ScheduleView import ScheduleView
from Internal.ui.components.StudentsView import StudentsView
from Internal.ui.components.GroupsView import GroupsView
from Internal.ui.components.DashboardView import DashboardView
from Internal.ui.components.SettingsView import SettingsView


class UserUi:
    def __init__(self, root, user, on_logout, settings_service: SettingsService, user_service: UserService,
                 student_service: StudentService, group_service: GroupService, preset_service: PresetService,
                 schedule_service: ScheduleService, language_service: LanguageService):
        self.rows_var = 0
        self.root = root
        self.user = user
        self.on_logout = on_logout
        self.settings_service = settings_service
        self.user_service = user_service
        self.student_service = student_service
        self.group_service = group_service
        self.preset_service = preset_service
        self.schedule_service = schedule_service
        self.language_service = language_service
        self.colors = self.settings_service.get_colors(user.get_id_entity())

        self.current_date = datetime.now()
        uid = self.user.get_id_entity()
        app_title = self.language_service.get_text(uid, "app_title")
        self.root.title(f"{app_title} - {user.get_first_name()}")
        self.setup_window(1725, 800)
        self.root.configure(bg=self.colors["bg"])
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar_bg"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.main_content = tk.Frame(self.root, bg=self.colors["bg"], padx=40, pady=40)
        self.main_content.pack(side="right", expand=True, fill="both")
        self.dashboard_component = DashboardView(self.main_content, self)
        self.schedule_component = ScheduleView(self.main_content, self)
        self.students_component = StudentsView(self.main_content, self)
        self.groups_component = GroupsView(self.main_content, self)
        self.settings_component = SettingsView(self.main_content, self)
        self.setup_sidebar_content(user)
        self.show_dashboard()

    def setup_window(self, w, h):
        self.root.state('zoomed')
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 20
        self.root.geometry(f'{int(w)}x{int(h)}+{int(x)}+{int(y)}')

    def setup_sidebar_content(self, user):
        """Configurează elementele vizuale din sidebar cu traduceri."""
        uid = user.get_id_entity()

        if self.schedule_service.get_schedule_data():
            current_rows = self.schedule_service.get_schedule_data().get("total_rows", 5)
            self.rows_var = tk.IntVar(value=max(2, current_rows))
        profile_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"], pady=30)
        profile_frame.pack(fill="x")
        initials = f"{user.get_first_name()[0]}{user.get_last_name()[0]}".upper()
        tk.Label(profile_frame, text=initials, font=("Segoe UI", 22, "bold"),
                 bg="#4A90E2", fg="white", width=3, height=1).pack()
        tk.Label(profile_frame, text=f"{user.get_first_name()} {user.get_last_name()}",
                 font=("Segoe UI", 11, "bold"), bg=self.colors["sidebar_bg"], fg=self.colors["fg"]).pack(pady=10)

        self.create_menu_button(f"🏠 {self.language_service.get_text(uid, 'menu_dashboard')}",
                                self.show_dashboard)
        self.create_menu_button(f"📅 {self.language_service.get_text(uid, 'menu_schedule')}",
                                self.show_schedule)
        self.create_menu_button(f"🏫 {self.language_service.get_text(uid, 'menu_groups')}", self.show_groups)
        self.create_menu_button(f"👥 {self.language_service.get_text(uid, 'menu_students')}",
                                lambda: self.show_students("grade"))
        self.create_menu_button(f"⚙️ {self.language_service.get_text(uid, 'menu_settings')}", self.show_settings)

        # Deconectare tradus
        logout_text = self.language_service.get_text(uid, "btn_logout")
        tk.Button(self.sidebar, text=f"🚪 {logout_text}", command=self.on_logout,
                  font=("Segoe UI", 11), bg="#E74C3C", fg="white", relief="flat",
                  cursor="hand2", pady=10).pack(side="bottom", fill="x", padx=20, pady=20)

    def create_menu_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, command=command, font=("Segoe UI", 11),
                        bg=self.colors["sidebar_bg"], fg=self.colors["fg"], relief="flat",
                        anchor="w", padx=30, pady=15, cursor="hand2",
                        activebackground=self.colors["hover"], activeforeground=self.colors["fg"])
        btn.pack(fill="x")

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_schedule(self):
        self.clear_content()
        self.schedule_component.render()

    def save_as_preset(self):
        PresetSaveUi(self.root, self.colors, self.process_preset_creation,
                     self.language_service, self.user.get_id_entity())

    def process_preset_creation(self, name):
        uid = self.user.get_id_entity()
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
        data_to_save = {}

        for row in range(1, self.rows_var.get() + 1):
            for col in range(6):
                date_str = (start_of_week + timedelta(days=col)).strftime('%Y-%m-%d')
                cell_key = f"{uid}_{date_str}_R{row}_raw"
                if cell_key in self.schedule_service.get_schedule_data():
                    data_to_save[f"D{col}_R{row}"] = self.schedule_service.get_schedule_data()[cell_key]

        if data_to_save:
            status = self.preset_service.create_preset(uid, name, data_to_save)
            if status[0] == 201:
                msg = self.language_service.get_text(uid, "msg_preset_saved").replace("{name}", name)
                self.show_toast(f"✅ {msg}")
            else:
                err = self.language_service.get_text(uid, "err_preset_exists")
                self.show_toast(f"❌ {err}", "#E74C3C")

    def open_presets_manager(self):
        uid = self.user.get_id_entity()
        presets = self.preset_service.get_all_presets_for_teacher(uid)

        if not presets:
            info_msg = self.language_service.get_text(uid, "msg_no_presets")
            messagebox.showinfo("Info", info_msg)
            return

        manager = tk.Toplevel(self.root)
        manager_title = self.language_service.get_text(uid, "title_preset_manager")
        manager.title(manager_title)

        w, h = 450, 550
        ws, hs = manager.winfo_screenwidth(), manager.winfo_screenheight()
        manager.geometry(f'{w}x{h}+{int((ws / 2) - (w / 2))}+{int((hs / 2) - (h / 2))}')
        manager.configure(bg=self.colors["bg"], padx=25, pady=25)
        manager.grab_set()

        tk.Label(manager, text=f"📋 {manager_title}", font=("Segoe UI", 14, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=(0, 20))

        container = tk.Frame(manager, bg=self.colors["bg"])
        container.pack(fill="both", expand=True)

        apply_text = self.language_service.get_text(uid, "btn_apply")

        for p in presets:
            row = tk.Frame(container, bg=self.colors["card_bg"], pady=12, padx=15,
                           highlightthickness=1, highlightbackground=self.colors["grid_line"])
            row.pack(fill="x", pady=5)

            tk.Label(row, text=p.get_name(), bg=self.colors["card_bg"],
                     fg=self.colors.get("schedule_text", "#FFFFFF"),
                     font=("Segoe UI", 11, "bold")).pack(side="left")

            tk.Button(row, text="🗑️", bg="#E74C3C", fg="white", relief="flat",
                      command=lambda po=p: [
                          self.preset_service.delete_preset(po),
                          manager.destroy(),
                          self.show_toast(f"🗑️ {self.language_service.get_text(uid, 'msg_preset_deleted')}", "#34495E"),
                          self.open_presets_manager()
                      ]).pack(side="right", padx=5)

            tk.Button(row, text=f"📋 {apply_text}", bg="#8E44AD", fg="white", relief="flat",
                      font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10,
                      command=lambda po=p: [self.apply_preset_logic(po), manager.destroy()]).pack(side="right", padx=5)

    def apply_preset_logic(self, preset_obj):
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
        uid = self.user.get_id_entity()

        for key, data in preset_obj.get_data().items():
            parts = key.split('_')
            day_idx = int(parts[0][1:])
            row_num = parts[1][1:]
            target_date = (start_of_week + timedelta(days=day_idx)).strftime('%Y-%m-%d')

            new_data = data.copy()
            new_data['absentees'] = []
            self.schedule_service.get_schedule_data()[f"{uid}_{target_date}_R{row_num}_raw"] = new_data

        self.schedule_service.save_schedule_data()
        self.show_schedule()

    def on_date_selected(self):
        selected_date = self.schedule_component.cal_select.get_date()
        self.current_date = datetime.combine(selected_date, datetime.min.time())
        self.root.after(100, self.show_schedule)

    def prev_week(self):
        self.current_date -= timedelta(days=7)
        self.show_schedule()

    def next_week(self):
        self.current_date += timedelta(days=7)
        self.show_schedule()

    def update_rows_count(self):
        new_count = self.rows_var.get()
        self.schedule_service.get_schedule_data()["total_rows"] = new_count
        self.schedule_service.save_schedule_data()
        self.show_schedule()

    def show_students(self, sort_by="grade"):
        self.students_component.render(sort_by)

    def show_groups(self):
        if self.student_service.size_for_user(self.user.get_id_entity()) > 0:
            self.groups_component.render()
        else:
            self.show_toast(f"❌ {self.language_service.get_text(self.user.get_id_entity(),
                                                                'no_students')}","#E74C3C")

    def go_to_today(self):
        self.current_date = datetime.now()
        msg = self.language_service.get_text(self.user.get_id_entity(), "msg_returned_today")
        self.show_toast(f"🏠 {msg}")
        self.show_schedule()

    def open_group_assignment_modal(self, cell_id):
        if self.group_service.size_for_user(self.user.get_id_entity()) == 0:
            self.show_toast(f"❌ {self.language_service.get_text(self.user.get_id_entity(),
                                                                'no_groups')}", "#E74C3C")
            return
        uid = self.user.get_id_entity()
        unique_key = f"{uid}_{cell_id}"
        current_data = self.schedule_service.get_schedule_data().get(f"{unique_key}_raw", None)
        user_colors = self.settings_service.get_colors(uid)

        ScheduleEditUi(parent=self.root, theme=user_colors, cell_id=cell_id,
                       day=cell_id.split('_')[0], current_data=current_data,
                       on_save=self.process_schedule_save, on_delete=self.process_schedule_delete,
                       group_service=self.group_service, user_id=uid, lang_service=self.language_service)

    def get_formatted_students(self, data):
        group_id = data.get('group_id')
        if not group_id:
            return ""
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

    def open_add_student_modal(self):
        StudentAddUi(parent=self.root, theme=self.colors, user_id=self.user.get_id_entity(),
                     student_service=self.student_service, on_success=self.show_students,
                     settings_service=self.settings_service, lang_service=self.language_service)

    def handle_delete_student(self, student):
        uid = self.user.get_id_entity()
        ls = self.language_service

        # Construim mesajul de confirmare dinamic
        title = ls.get_text(uid, "confirmation")
        # Folosim placeholder-ul {name} definit anterior în JSON pentru consistență
        question = ls.get_text(uid, "msg_delete_student_confirm").replace("{name}",
                                                                          f"{student.get_last_name()}"
                                                                          f" {student.get_first_name()}")

        if messagebox.askyesno(title, question):
            self.student_service.delete_student(student)
            self.show_students()

    def open_add_group_modal(self):
        GroupAddUi(parent=self.root, theme=self.colors, user_id=self.user.get_id_entity(),
                   group_service=self.group_service, student_service=self.student_service, on_success=self.show_groups,
                   lang_service=self.language_service)

    def handle_delete_group(self, group):
        uid = self.user.get_id_entity()
        ls = self.language_service

        # Construim mesajul de confirmare tradus
        title = ls.get_text(uid, "confirmation")
        question = ls.get_text(uid, "msg_delete_group_confirm").replace("{name}", group.get_group_name())

        if messagebox.askyesno(title, question):
            self.group_service.delete_group(group.get_id_entity())
            self.schedule_service.delete_cascade(group.get_id_entity())
            self.preset_service.delete_cascade(group.get_id_entity(), uid)
            self.show_groups()

    def toggle_absentee(self, cell_id, student_id):
        """Gestionează prezența elevilor și actualizează veniturile zilnice."""
        uid = self.user.get_id_entity()
        unique_key_raw = f"{uid}_{cell_id}_raw"

        if unique_key_raw in self.schedule_service.get_schedule_data():
            absentees = self.schedule_service.get_schedule_data()[unique_key_raw].get('absentees', [])

            if student_id in absentees:
                absentees.remove(student_id)
            else:
                absentees.append(student_id)

            self.schedule_service.get_schedule_data()[unique_key_raw]['absentees'] = absentees

            # REPARARE: Folosim metoda internă a clasei în loc de un serviciu inexistent
            self.schedule_service.save_schedule_data()

            # Reîmprospătăm ecranul
            self.show_schedule()

    def process_schedule_save(self, cell_id, data):
        unique_key = f"{self.user.get_id_entity()}_{cell_id}"
        self.schedule_service.get_schedule_data()[f"{unique_key}_raw"] = data
        self.schedule_service.save_schedule_data()
        self.show_schedule()

    def process_schedule_delete(self, cell_id):
        unique_key = f"{self.user.get_id_entity()}_{cell_id}"
        full_key = f"{unique_key}_raw"
        if full_key in self.schedule_service.get_schedule_data():
            del self.schedule_service.get_schedule_data()[full_key]
            self.schedule_service.save_schedule_data()
            self.show_schedule()

    def show_dashboard(self):
        self.clear_content()
        self.dashboard_component.render()

    def show_settings(self):
        self.clear_content()
        self.settings_component.render()

    def toggle_theme_ui(self):
        """Reîmprospătează culorile și randează interfața."""
        uid = self.user.get_id_entity()
        self.colors = self.settings_service.get_colors(uid)

        # Update UI title (could have changed with language)
        app_title = self.language_service.get_text(uid, "app_title")
        self.root.title(f"{app_title} - {self.user.get_first_name()}")

        self.root.configure(bg=self.colors["bg"])
        self.main_content.configure(bg=self.colors["bg"])

        for widget in self.sidebar.winfo_children():
            widget.destroy()
        self.sidebar.configure(bg=self.colors["sidebar_bg"])
        self.setup_sidebar_content(self.user)
        self.show_settings()

    def show_toast(self, message, color="#2ECC71"):
        """Afișează o notificare discretă."""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.attributes("-alpha", 0.0)

        label = tk.Label(toast, text=message, bg=color, fg="white",
                         padx=20, pady=10, font=("Segoe UI", 10, "bold"))
        label.pack()

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (label.winfo_reqwidth() // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - 70
        toast.geometry(f"+{int(x)}+{int(y)}")

        def fade_in():
            if toast.winfo_exists():
                alpha = toast.attributes("-alpha")
                if alpha < 0.9:
                    toast.attributes("-alpha", alpha + 0.1)
                    self.root.after(30, fade_in)
                else:
                    self.root.after(3000, lambda: self.fade_out(toast))

        fade_in()

    def fade_out(self, window):
        if window.winfo_exists():
            alpha = window.attributes("-alpha")
            if alpha > 0.0:
                window.attributes("-alpha", alpha - 0.1)
                self.root.after(30, lambda: self.fade_out(window))
            else:
                window.destroy()
