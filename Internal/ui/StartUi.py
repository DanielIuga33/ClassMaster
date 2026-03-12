import tkinter as tk
from Internal.service.SettingsService import SettingsService
from Internal.service.LanguageService import LanguageService
import pywinstyles


class StartUi:
    def __init__(self, root, on_login_click, on_register_click, settings_service: SettingsService,
                 lang_service: LanguageService):
        self.root = root
        self.root.title("ClassMaster")
        self.settings_service = settings_service
        self.lang_service = lang_service

        self.on_login_click = on_login_click
        self.on_register_click = on_register_click
        self.ui_themes = {
            "light": {
                "bg": "#F0F2F5", "fg": "#333", "sub": "#666",
                "btn_log": "#007BFF", "btn_reg": "#28A745", "icon": "🌙"
            },
            "dark": {
                "bg": "#18191A", "fg": "#E4E6EB", "sub": "#B0B3B8",
                "btn_log": "#374151", "btn_reg": "#059669", "icon": "☀️"
            }
        }
        self.current_theme_name = self.settings_service.get_theme("global")
        try:
            # Aplicăm stilul de bază imediat, înainte de orice widget
            pywinstyles.apply_style(self.root, self.current_theme_name)
        except Exception as e:
            print(e)
            pass
        self.theme_button = tk.Button(self.root, command=self.toggle_theme,
                                      font=("Segoe UI", 12), relief="flat", cursor="hand2")
        self.theme_button.place(x=350, y=10)
        self.lang_button = tk.Button(self.root, command=self.toggle_language,
                                     font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2")
        self.lang_button.place(x=310, y=12)

        self.lbl_title = tk.Label(self.root, font=("Segoe UI", 28, "bold"))
        self.lbl_title.pack(pady=(60, 10))

        self.lbl_subtitle = tk.Label(self.root, font=("Segoe UI", 12))
        self.lbl_subtitle.pack(pady=(0, 40))

        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 20, "pady": 10, "relief": "flat", "cursor": "hand2"}
        self.btn_login = tk.Button(self.root, command=self.on_login_click, fg="white", **btn_style)
        self.btn_login.pack(pady=10)

        self.btn_reg = tk.Button(self.root, command=self.on_register_click, fg="white", **btn_style)
        self.btn_reg.pack(pady=10)

        self.setup_window(400, 500)
        self.update_ui_content()
        self.root.after(200, self.apply_system_theme)

    def setup_window(self, w, h):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def toggle_theme(self):
        new_theme = "dark" if self.current_theme_name == "light" else "light"
        self.current_theme_name = new_theme
        self.settings_service.save_for_global("tema", new_theme)
        self.update_ui_content()
        self.apply_system_theme()

    def toggle_language(self):
        """Schimbă limba și salvează în profilul global."""
        current_lang = self.settings_service.get_user_settings("global").get("language", "ro")
        new_lang = "en" if current_lang == "ro" else "ro"

        self.settings_service.save_for_global("language", new_lang)
        self.update_ui_content()

    def update_ui_content(self):
        """Actualizează culorile, traducerile și textul butonului de limbă."""
        theme = self.ui_themes[self.current_theme_name]
        current_lang = self.settings_service.get_user_settings("global").get("language")
        self.lbl_title.configure(text=self.lang_service.get_text("global", "app_title"))
        self.lbl_subtitle.configure(text=self.lang_service.get_text("global", "app_subtitle"))
        self.btn_login.configure(text=self.lang_service.get_text("global", "btn_login"))
        self.btn_reg.configure(text=self.lang_service.get_text("global", "btn_register"))
        lang_btn_text = "EN" if current_lang == "ro" else "RO"
        self.lang_button.configure(text=lang_btn_text, bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"])

        # --- CULORI ---
        self.root.configure(bg=theme["bg"])
        self.theme_button.configure(text=theme["icon"], bg=theme["bg"], fg=theme["fg"], activebackground=theme["bg"])
        self.lbl_title.configure(bg=theme["bg"], fg=theme["fg"])
        self.lbl_subtitle.configure(bg=theme["bg"], fg=theme["sub"])
        self.btn_login.configure(bg=theme["btn_log"])
        self.btn_reg.configure(bg=theme["btn_reg"])

    def apply_system_theme(self):
        """Sincronizează bara nativă folosind un 'Silent Refresh' prin transparență."""
        try:
            self.root.attributes("-alpha", 0.0)

            # 2. APLICĂM STILURILE
            pywinstyles.apply_style(self.root, self.current_theme_name)

            # Folosim o nuanță de gri cărbune pentru dark mode (mai bine acceptată de Windows)
            header_color = "#1F1F1F" if self.current_theme_name == "dark" else "#F0F2F5"
            pywinstyles.change_header_color(self.root, color=header_color)

            title_fg = "#FFFFFF" if self.current_theme_name == "dark" else "#000000"
            pywinstyles.change_title_color(self.root, color=title_fg)

            # 3. REFRESH-UL DE SISTEM (Singurul care pare să funcționeze la tine)
            # Acesta forțează Windows să re-mapeze fereastra în Task Manager și DWM
            self.root.withdraw()
            self.root.deiconify()

            # 4. REVENIM LA OPACITATE MAXIMĂ
            # Adăugăm un delay minuscul pentru a lăsa Windows să termine 'vopsirea' bării
            self.root.after(10, lambda: self.root.attributes("-alpha", 1.0))

            # Refresh titlu (Double check)
            t = self.root.title()
            self.root.title(t + " ")
            self.root.title(t.strip())

        except Exception as e:
            print(f"Eroare DWM: {e}")
            self.root.attributes("-alpha", 1.0)
