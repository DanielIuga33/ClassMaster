import tkinter as tk

from Internal.repository.RepositoryGroup import RepositoryGroup
from Internal.repository.RepositoryUser import RepositoryUser
from Internal.repository.RepositoryStudent import RepositoryStudent
from Internal.repository.RepositoryPreset import RepositoryPreset
from Internal.service.LanguageService import LanguageService
from Internal.service.PresetService import PresetService
from Internal.service.ScheduleService import ScheduleService
from Internal.service.StudentService import StudentService
from Internal.service.UserService import UserService
from Internal.service.GroupService import GroupService
from Internal.service.SettingsService import SettingsService
from Internal.ui.LoginUi import LoginUi
from Internal.ui.UserUi import UserUi
from Internal.ui.StartUi import StartUi
from Internal.ui.RegisterUi import RegisterUi


class MainController:
    def __init__(self):
        self.root = tk.Tk()
        self.settings_service = SettingsService()
        self.language_service = LanguageService(self.settings_service)
        self.current_theme = self.settings_service.get_theme(user_id="global")
        self.user_service = UserService(RepositoryUser(""))
        self.student_service = StudentService(RepositoryStudent(""))
        self.group_service = GroupService(RepositoryGroup(""))
        self.preset_service = PresetService(RepositoryPreset(""))
        self.schedule_service = ScheduleService()
        self.show_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_screen()
        StartUi(self.root, self.show_login, self.show_register, self.settings_service)

    def show_login(self):
        self.clear_screen()
        LoginUi(
            self.root,
            self.user_service,
            self.student_service,
            self.group_service,
            self.preset_service,
            self.login_success,
            self.settings_service,
            self.schedule_service,
            self.show_start_screen
        )

    def show_register(self):
        self.clear_screen()
        RegisterUi(
            self.root,
            self.user_service,
            self.show_start_screen,
            self.settings_service
        )

    def login_success(self, user):
        self.clear_screen()
        # Deschide interfața principală cu elevii
        # UserUi(self.root, user)
        UserUi(
            self.root,
            user,
            self.show_start_screen,
            self.settings_service,
            self.user_service,
            self.student_service,
            self.group_service,
            self.preset_service,
            self.schedule_service,
            self.language_service
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainController()
    app.run()
