import tkinter as tk


class StartUi:
    def __init__(self, root, on_login_click, on_register_click, settings_service):
        self.root = root
        self.root.title("ClassMaster")
        self.settings_service = settings_service
        self.on_login_click = on_login_click
        self.on_register_click = on_register_click

        # Definire Teme
        self.themes = {
            "light": {
                "bg": "#F0F2F5", "fg": "#333", "sub": "#666",
                "btn_log": "#007BFF", "btn_reg": "#28A745", "icon": "🌙"
            },
            "dark": {
                "bg": "#18191A", "fg": "#E4E6EB", "sub": "#B0B3B8",
                "btn_log": "#374151", "btn_reg": "#059669", "icon": "☀️"
            }
        }

        # Încărcăm tema din setări
        self.current_theme_name = self.settings_service.get_theme()

        # Centrare fereastră
        self.setup_window(400, 500)

        # Construim interfața
        self.create_widgets()

        # Aplicăm tema inițială
        self.update_ui_colors()

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def create_widgets(self):
        # Buton temă (sus-dreapta)
        self.theme_button = tk.Button(
            self.root, command=self.toggle_theme,
            font=("Segoe UI", 12), relief="flat", cursor="hand2"
        )
        self.theme_button.place(x=350, y=10)

        # Titluri
        self.lbl_title = tk.Label(self.root, text="ClassMaster", font=("Segoe UI", 28, "bold"))
        self.lbl_title.pack(pady=(60, 10))

        self.lbl_subtitle = tk.Label(self.root, text="Managementul meditațiilor tale", font=("Segoe UI", 12))
        self.lbl_subtitle.pack(pady=(0, 40))

        # Butoane
        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 20, "pady": 10, "relief": "flat", "cursor": "hand2"}

        self.btn_login = tk.Button(self.root, text="Autentificare", command=self.on_login_click, fg="white",
                                   **btn_style)
        self.btn_login.pack(pady=10)

        self.btn_reg = tk.Button(self.root, text="Cont Nou", command=self.on_register_click, fg="white", **btn_style)
        self.btn_reg.pack(pady=10)

    def set_theme(self, theme_name):
        """Aceasta este metoda care lipsea și cauza eroarea!"""
        self.current_theme_name = theme_name
        self.settings_service.save_settings({"tema": theme_name})
        self.update_ui_colors()

    def toggle_theme(self):
        new_theme = "dark" if self.current_theme_name == "light" else "light"
        self.set_theme(new_theme)

    def update_ui_colors(self):
        theme = self.themes[self.current_theme_name]

        # Fundal
        self.root.configure(bg=theme["bg"])

        # Widget-uri
        self.theme_button.configure(text=theme["icon"], bg=theme["bg"], fg=theme["fg"])
        self.lbl_title.configure(bg=theme["bg"], fg=theme["fg"])
        self.lbl_subtitle.configure(bg=theme["bg"], fg=theme["sub"])

        # Butoane (le schimbăm și lor culorile să se potrivească)
        self.btn_login.configure(bg=theme["btn_log"])
        self.btn_reg.configure(bg=theme["btn_reg"])