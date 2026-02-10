import tkinter as tk
from tkinter import messagebox, filedialog

from Internal.service.UserService import UserService


class LoginUi:
    def __init__(self, root, user_service: UserService, on_success, settings_service, on_back):
        self.root = root
        self.user_service = user_service
        self.on_success = on_success
        self.settings_service = settings_service
        self.on_back = on_back

        self.theme = self.get_theme_colors()
        self.root.title("Autentificare - ClassMaster")
        self.setup_window(400, 600)
        self.root.configure(bg=self.theme["bg"])

        self.container = tk.Frame(self.root, bg=self.theme["bg"])
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Stiluri
        lbl_style = {"bg": self.theme["bg"], "fg": self.theme["fg"], "font": ("Segoe UI", 10, "bold")}
        ent_style = {"font": ("Segoe UI", 12), "relief": "flat", "bg": self.theme["ent_bg"], "fg": self.theme["fg"],
                     "insertbackground": self.theme["fg"]}

        # Titlu - folosim PACK peste tot în container
        tk.Label(self.container, text="Autentificare", font=("Segoe UI", 24, "bold"),
                 bg=self.theme["bg"], fg=self.theme["fg"]).pack(pady=(0, 20))

        # --- Locație stocare date ---
        tk.Label(self.container, text="Locație stocare date", **lbl_style).pack(anchor="w", pady=(10, 0))

        # Creăm un sub-frame special pentru a pune Entry și Buton pe același rând
        path_frame = tk.Frame(self.container, bg=self.theme["bg"])
        path_frame.pack(fill="x", pady=5)

        self.entry_path = tk.Entry(path_frame, **ent_style)
        self.entry_path.pack(side="left", expand=True, fill="x", ipady=5)

        # Punem și calea salvată anterior dacă există
        last_path = self.settings_service.settings.get("last_data_path", "")
        self.entry_path.insert(0, last_path)

        tk.Button(path_frame, text="Răsfoiește", command=self.browse_folder,
                  bg="#4A90E2", fg="white", relief="flat", cursor="hand2").pack(side="right", padx=(5, 0))

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
        tk.Button(self.container, text="Intră în cont", command=self.handle_login,
                  font=("Segoe UI", 12, "bold"), bg="#007BFF", fg="white",
                  relief="flat", width=25, cursor="hand2").pack(pady=10, ipady=5)

        tk.Button(self.container, text="Înapoi", command=self.on_back,
                  font=("Segoe UI", 10), bg=self.theme["bg"], fg="#888",
                  relief="flat", cursor="hand2").pack()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder)
            # Salvăm calea aleasă pentru a nu o cere de fiecare dată
            self.settings_service.save_settings({"last_data_path": folder})

    def handle_login(self):
        identifier = self.entry_identifier.get().strip()
        password = self.entry_password.get().strip()
        data_path = self.entry_path.get().strip()

        if not identifier or not password or not data_path:
            messagebox.showwarning("Atenție", "Te rugăm să completezi toate câmpurile, inclusiv calea datelor!")
            return

        # Spunem repository-ului unde să caute fișierul Users.json ales de utilizator
        self.user_service.set_repository_path(data_path)

        user = self.user_service.authenticate(identifier, password)
        if user:
            self.settings_service.save_settings({"last_user": identifier})
            messagebox.showinfo("Succes", f"Bine ai venit!")
            self.on_success(user)
        else:
            messagebox.showerror("Eroare", "Date incorecte sau utilizator negăsit în această locație!")

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def get_theme_colors(self):
        if self.settings_service.get_theme() == "dark":
            return {"bg": "#18191A", "fg": "#E4E6EB", "ent_bg": "#3A3B3C"}
        return {"bg": "#F0F2F5", "fg": "#333", "ent_bg": "#FFFFFF"}