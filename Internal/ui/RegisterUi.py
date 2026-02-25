import tkinter as tk
from tkinter import filedialog
from Internal.entity.User import User
from Internal.service.UserService import UserService
from Internal.service.LanguageService import LanguageService


class RegisterUi:
    def __init__(self, root, user_service: UserService, on_back, settings_service, lang_service: LanguageService):
        self.root = root
        self.user_service = user_service
        self.on_back = on_back
        self.settings_service = settings_service
        self.lang_service = lang_service  # Injectăm serviciul de limbă

        # Preluăm tema și culoarea de contrast
        self.colors = self.settings_service.get_colors("global")
        self.txt_color = self.colors.get("schedule_text", "#FFFFFF")

        # Titlu fereastră tradus
        self.root.title(f"{self.lang_service.get_text('global', 'reg_title')} - ClassMaster")

        # Centrare fereastră
        self.setup_window(600, 750)
        self.root.configure(bg=self.colors["bg"])

        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(expand=True, fill="both", padx=50, pady=20)

        # Titlu modernizat tradus
        tk.Label(self.container, text=self.lang_service.get_text("global", "reg_header"),
                 font=("Segoe UI", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Stiluri Entry folosind culorile din SettingsService
        self.lbl_style = {"bg": self.colors["bg"], "fg": self.txt_color, "font": ("Segoe UI", 9, "bold")}
        self.ent_style = {"font": ("Segoe UI", 11), "relief": "flat", "bg": self.colors["input_bg"],
                          "fg": self.txt_color, "insertbackground": self.txt_color}

        # Câmpuri traduse prin LanguageService
        self.add_field(self.lang_service.get_text("global", "reg_last_name"), "entry_ln", 1, 0)
        self.add_field(self.lang_service.get_text("global", "reg_first_name"), "entry_fn", 1, 1)
        self.add_field(self.lang_service.get_text("global", "user_identifier1"), "entry_uname", 2, 0)
        self.add_field(self.lang_service.get_text("global", "reg_email"), "entry_email", 2, 1)
        self.add_field(self.lang_service.get_text("global", "password"), "entry_pass", 3, 0, show="*")
        self.add_field(self.lang_service.get_text("global", "reg_confirm_pass"), "entry_confirm_pass", 3, 1, show="*")
        self.add_field(self.lang_service.get_text("global", "reg_address"), "entry_street", 4, 0, columnspan=2)
        self.add_field(self.lang_service.get_text("global", "reg_city"), "entry_city", 5, 0)
        self.add_field(self.lang_service.get_text("global", "reg_state"), "entry_state", 5, 1)
        self.add_field(self.lang_service.get_text("global", "reg_birthday"), "entry_birth", 6, 0, columnspan=2)

        # Locație stocare tradusă
        tk.Label(self.container, text=self.lang_service.get_text("global", "data_location"),
                 **self.lbl_style).grid(row=14, column=0, sticky="w", pady=(10, 0))

        path_frame = tk.Frame(self.container, bg=self.colors["bg"])
        path_frame.grid(row=15, column=0, columnspan=2, sticky="ew")

        self.entry_path = tk.Entry(path_frame, **self.ent_style)
        self.entry_path.pack(side="left", expand=True, fill="x", ipady=4)

        # Buton Răsfoiește tradus
        tk.Button(path_frame, text=self.lang_service.get_text("global", "browse"), command=self.browse_folder,
                  bg=self.colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="right", padx=(5, 0))

        # Buton Finalizare tradus
        tk.Button(self.container, text=self.lang_service.get_text("global", "btn_register_submit"),
                  command=self.handle_register,
                  font=("Segoe UI", 12, "bold"), bg=self.colors.get("success", "#2ECC71"),
                  fg="white", relief="flat", pady=10, cursor="hand2").grid(row=16, column=0, columnspan=2, sticky="ew",
                                                                           pady=(25, 10))

        # Buton Înapoi tradus
        tk.Button(self.container, text=self.lang_service.get_text("global", "btn_back"),
                  command=on_back, bg=self.colors["bg"],
                  fg="#888", relief="flat", cursor="hand2").grid(row=17, column=0, columnspan=2)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

    def show_toast(self, message, color="#2ECC71"):
        """Implementare locală de Toast pentru ecranul de înregistrare."""
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)

        lbl = tk.Label(toast, text=message, bg=color, fg="white", padx=20, pady=10, font=("Segoe UI", 10, "bold"))
        lbl.pack()

        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (lbl.winfo_reqwidth() // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        toast.geometry(f"+{int(x)}+{int(y)}")

        self.root.after(3000, toast.destroy)

    def handle_register(self):
        """Procesează datele și înregistrează utilizatorul folosind mesaje traduse."""
        username = self.entry_uname.get().strip()
        password = self.entry_pass.get()
        confirm_pass = self.entry_confirm_pass.get()
        data_path = self.entry_path.get()

        # Verificare parole
        if password != confirm_pass:
            self.show_toast(self.lang_service.get_text("global", "err_pass_mismatch"), "#E74C3C")
            return

        # Verificare câmpuri obligatorii
        if not all([username, password, data_path]):
            self.show_toast(self.lang_service.get_text("global", "error_fill_fields"), "#F1C40F")
            return

        try:
            new_user = User(username=username, first_name=self.entry_fn.get(), last_name=self.entry_ln.get(),
                            email=self.entry_email.get(), password=password, data_path=data_path,
                            street_address=self.entry_street.get(), city=self.entry_city.get(),
                            state=self.entry_state.get(), birthday=self.entry_birth.get())

            result = self.user_service.add_user(new_user)

            if result and result[0] == 201:
                # Mesaj de succes tradus
                self.show_toast(f"✅ {self.lang_service.get_text('global', 'msg_reg_success')}")
                self.root.after(2000, self.on_back)
            else:
                self.show_toast(f"❌ {result[1]}", "#E74C3C")

        except Exception as e:
            self.show_toast(f"❌ Eroare: {str(e)}", "#E74C3C")

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 50
        self.root.geometry(f'{int(w)}x{int(h)}+{int(x)}+{int(y)}')

    def add_field(self, label_text, attr_name, row, col, columnspan=1, show=None):
        r = row * 2
        tk.Label(self.container, text=label_text, **self.lbl_style).grid(row=r, column=col, columnspan=columnspan,
                                                                         sticky="w", pady=(10, 2))
        entry = tk.Entry(self.container, show=show, **self.ent_style)
        entry.grid(row=r + 1, column=col, columnspan=columnspan, sticky="ew",
                   padx=(0, 10 if col == 0 and columnspan == 1 else 0), ipady=5)
        setattr(self, attr_name, entry)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder)
