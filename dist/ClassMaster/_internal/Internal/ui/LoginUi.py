import tkinter as tk
from tkinter import filedialog

from Internal.service.GroupService import GroupService
from Internal.service.PresetService import PresetService
from Internal.service.ScheduleService import ScheduleService
from Internal.service.SettingsService import SettingsService
from Internal.service.StudentService import StudentService
from Internal.service.UserService import UserService
from Internal.service.LanguageService import LanguageService


class LoginUi:
    def __init__(self, root, user_service: UserService, student_service: StudentService,
                 group_service: GroupService, preset_service: PresetService,
                 on_success, settings_service: SettingsService, schedule_service: ScheduleService,
                 on_back, lang_service: LanguageService):
        self.root = root
        self.user_service = user_service
        self.student_service = student_service
        self.group_service = group_service
        self.preset_service = preset_service
        self.on_success = on_success
        self.settings_service = settings_service
        self.schedule_service = schedule_service
        self.on_back = on_back
        self.lang_service = lang_service

        global_settings = self.settings_service.get_user_settings("global")
        self.colors = self.settings_service.get_colors("global")

        if self.colors is None:
            self.colors = {"bg": "#18191A", "fg": "#E4E6EB", "input_bg": "#3A3B3C", "accent": "#007BFF",
                           "success": "#059669"}
        self.root.title(f"{self.lang_service.get_text('global', 'login_title')} - ClassMaster")
        self.setup_window(400, 600)
        self.root.configure(bg=self.colors["bg"])

        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        lbl_style = {"bg": self.colors["bg"], "fg": self.colors["fg"], "font": ("Segoe UI", 10, "bold")}
        ent_style = {
            "font": ("Segoe UI", 12),
            "relief": "flat",
            "bg": self.colors["input_bg"],
            "fg": self.colors["fg"],
            "insertbackground": self.colors["fg"]
        }

        tk.Label(self.container, text=self.lang_service.get_text("global", "login_title"),
                 font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=(0, 20))
        tk.Label(self.container, text=self.lang_service.get_text("global", "data_location"),
                 **lbl_style).pack(anchor="w", pady=(10, 0))
        path_frame = tk.Frame(self.container, bg=self.colors["bg"])
        path_frame.pack(fill="x", pady=5)

        self.entry_path = tk.Entry(path_frame, **ent_style)
        self.entry_path.pack(side="left", expand=True, fill="x", ipady=5)
        self.entry_path.insert(0, global_settings.get("last_data_path", ""))
        tk.Button(path_frame, text=self.lang_service.get_text("global", "browse"), command=self.browse_folder,
                  bg=self.colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="right", padx=(5, 0))
        tk.Label(self.container, text=self.lang_service.get_text("global", "user_identifier"),
                 **lbl_style).pack(anchor="w", pady=(10, 0))
        self.entry_identifier = tk.Entry(self.container, width=30, **ent_style)
        self.entry_identifier.pack(pady=5, ipady=5)

        last_user = global_settings.get("last_user", "")
        if last_user:
            self.entry_identifier.insert(0, last_user)
        tk.Label(self.container, text=self.lang_service.get_text("global", "password"),
                 **lbl_style).pack(anchor="w", pady=(10, 0))
        self.entry_password = tk.Entry(self.container, width=30, show="*", **ent_style)
        self.entry_password.pack(pady=(5, 30), ipady=5)
        login_btn = tk.Button(self.container, text=self.lang_service.get_text("global", "btn_login_submit"),
                              command=self.handle_login,
                              font=("Segoe UI", 12, "bold"), bg=self.colors["accent"], fg="white",
                              relief="flat", width=25, cursor="hand2")
        login_btn.pack(pady=10, ipady=5)
        tk.Button(self.container, text=self.lang_service.get_text("global", "btn_back"),
                  command=self.on_back,
                  font=("Segoe UI", 10), bg=self.colors["bg"], fg="#888",
                  relief="flat", cursor="hand2").pack()

        self.root.bind('<Return>', lambda event: self.handle_login())

    def show_toast(self, message, is_error=False, duration=2500):
        """Creează o notificare silențioasă care dispare singură."""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)

        bg_color = self.colors["bg"]
        border_color = "#E74C3C" if is_error else self.colors.get("success", "#059669")

        toast.configure(bg=bg_color, highlightthickness=2, highlightbackground=border_color)

        toast.update_idletasks()
        w, h = 250, 50
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - 120
        toast.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(toast, text=message, bg=bg_color, fg=border_color,
                 font=("Segoe UI", 11, "bold")).pack(expand=True, fill="both")

        toast.after(duration, toast.destroy)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder)
            self.settings_service.save_for_global("last_data_path", folder)

    def handle_login(self):
        self.root.unbind('<Return>')

        if not self.entry_identifier.winfo_exists():
            return

        identifier = self.entry_identifier.get().strip()
        password = self.entry_password.get().strip()
        data_path = self.entry_path.get().strip()

        if not identifier or not password or not data_path:
            self.show_toast(self.lang_service.get_text("global", "error_fill_fields"), is_error=True)
            self.root.bind('<Return>', lambda event: self.handle_login())
            return

        if self.user_service.set_repository_path(data_path)[0] == 404:
            self.show_toast(self.lang_service.get_text("global", "error_invalid_path"), is_error=True)
            self.root.bind('<Return>', lambda event: self.handle_login())
            return

        user = self.user_service.authenticate(identifier, password)

        if user:
            self.group_service.set_repository_path(data_path, password)
            self.student_service.set_repository_path(data_path, password)
            self.preset_service.set_repository_path(data_path, password)

            self.schedule_service.set_schedule_path(data_path, password)
            self.settings_service.set_settings_path(data_path)

            self.settings_service.get_colors(user.get_id_entity())
            self.settings_service.save_for_global("last_user", identifier)
            self.settings_service.save_for_global("last_data_path", data_path)

            welcome_msg = self.lang_service.get_text("global", "msg_welcome")
            self.show_toast(f"✅ {welcome_msg}, {user.get_username() or user.get_first_name()}!")

            self.root.after(1200, lambda: self.on_success(user))
        else:
            self.show_toast(self.lang_service.get_text("global", "error_invalid_credentials"), is_error=True)
            self.root.bind('<Return>', lambda event: self.handle_login())

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
