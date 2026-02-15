import tkinter as tk
from tkinter import messagebox, filedialog

from Internal.service.GroupService import GroupService
from Internal.service.PresetService import PresetService
from Internal.service.StudentService import StudentService
from Internal.service.UserService import UserService


class LoginUi:
    def __init__(self, root, user_service: UserService, student_service: StudentService,
                 group_service: GroupService, preset_service: PresetService,
                 on_success, settings_service, on_back):
        self.root = root
        self.user_service = user_service
        self.student_service = student_service
        self.group_service = group_service
        self.preset_service = preset_service
        self.on_success = on_success
        self.settings_service = settings_service
        self.on_back = on_back

        # REPARARE: Preluăm culorile centralizate din SettingsService
        self.colors = self.settings_service.get_colors()

        self.root.title("Autentificare - ClassMaster")
        self.setup_window(400, 600)
        self.root.configure(bg=self.colors["bg"])

        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # REPARARE: Folosim input_bg pentru vizibilitate
        lbl_style = {"bg": self.colors["bg"], "fg": self.colors["fg"], "font": ("Segoe UI", 10, "bold")}
        ent_style = {
            "font": ("Segoe UI", 12),
            "relief": "flat",
            "bg": self.colors["input_bg"],  # Aici este griul deschis care se vede acum
            "fg": self.colors["fg"],
            "insertbackground": self.colors["fg"]
        }

        # Titlu
        tk.Label(self.container, text="Autentificare", font=("Segoe UI", 24, "bold"),
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=(0, 20))

        # --- Locație stocare date ---
        tk.Label(self.container, text="Locație stocare date", **lbl_style).pack(anchor="w", pady=(10, 0))

        path_frame = tk.Frame(self.container, bg=self.colors["bg"])
        path_frame.pack(fill="x", pady=5)

        self.entry_path = tk.Entry(path_frame, **ent_style)
        self.entry_path.pack(side="left", expand=True, fill="x", ipady=5)

        last_path = self.settings_service.settings.get("last_data_path", "")
        self.entry_path.insert(0, last_path)

        tk.Button(path_frame, text="Răsfoiește", command=self.browse_folder,
                  bg=self.colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="right", padx=(5, 0))

        # --- Identificator ---
        tk.Label(self.container, text="Username sau Email", **lbl_style).pack(anchor="w", pady=(10, 0))
        self.entry_identifier = tk.Entry(self.container, width=30, **ent_style)
        self.entry_identifier.pack(pady=5, ipady=5)

        last_user = self.settings_service.settings.get("last_user", "")
        if last_user:
            self.entry_identifier.insert(0, last_user)

        # --- Parolă ---
        tk.Label(self.container, text="Parolă", **lbl_style).pack(anchor="w", pady=(10, 0))
        self.entry_password = tk.Entry(self.container, width=30, show="*", **ent_style)
        self.entry_password.pack(pady=(5, 30), ipady=5)

        # --- Butoane ---
        login_btn = tk.Button(self.container, text="Intră în cont", command=self.handle_login,
                              font=("Segoe UI", 12, "bold"), bg="#007BFF", fg="white",
                              relief="flat", width=25, cursor="hand2")
        login_btn.pack(pady=10, ipady=5)

        # Efect de hover pentru butonul principal
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#0056b3"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#007BFF"))

        tk.Button(self.container, text="Înapoi", command=self.on_back,
                  font=("Segoe UI", 10), bg=self.colors["bg"], fg="#888",
                  relief="flat", cursor="hand2").pack()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder)
            self.settings_service.save_settings({"last_data_path": folder})

    def handle_login(self):
        identifier = self.entry_identifier.get().strip()
        password = self.entry_password.get().strip()
        data_path = self.entry_path.get().strip()

        if not identifier or not password or not data_path:
            messagebox.showwarning("Atenție", "Te rugăm să completezi toate câmpurile!")
            return

        self.user_service.set_repository_path(data_path)
        self.group_service.set_repository_path(data_path)
        self.student_service.set_repository_path(data_path)
        self.preset_service.set_repository_path(data_path)

        user = self.user_service.authenticate(identifier, password)
        if user:
            self.settings_service.save_settings({"last_user": identifier})
            messagebox.showinfo("Succes", f"Bine ai venit!")
            self.on_success(user)
        else:
            messagebox.showerror("Eroare", "Date incorecte!")

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f'{w}x{h}+{int(x)}+{int(y)}')