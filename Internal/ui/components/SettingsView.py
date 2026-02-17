import tkinter as tk
from tkinter import ttk
import hashlib


class SettingsView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller
        self.entries = {}
        self.pass_entries = {}
        self.theme_combo = None
        self.lang_combo = None

    def render(self):
        """Randare cu contrast forțat și notificări moderne."""
        self.master.clear_content()
        uid = self.master.user.get_id_entity()
        colors = self.master.settings_service.get_colors(uid)

        # Preluăm culoarea de contrast dedicată temei
        txt_color = colors.get("schedule_text", colors["fg"])

        # Header pagină
        tk.Label(self.parent, text="⚙️ Setări Aplicație", font=("Segoe UI", 28, "bold"),
                 bg=colors["bg"], fg=colors["accent"]).pack(anchor="w", pady=(0, 30))

        # --- Secțiune 1: PROFIL & SECURITATE ---
        main_profile_frame = tk.Frame(self.parent, bg=colors["bg"])
        main_profile_frame.pack(fill="x", pady=(0, 20))

        # COLOANA STÂNGA: Date Personale
        left_col = tk.LabelFrame(main_profile_frame, text=" 👤 Date Personale ", font=("Segoe UI", 13, "bold"),
                                 bg=colors["bg"], fg=txt_color, padx=20, pady=20, relief="flat",
                                 highlightthickness=1, highlightbackground=colors["grid_line"])
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        fields = [
            ("Prenume:", self.master.user.get_first_name(), "first_name"),
            ("Nume:", self.master.user.get_last_name(), "last_name"),
            ("Email:", self.master.user.get_email(), "email"),
            ("Username:", self.master.user.get_username(), "username"),
            ("Adresă:", self.master.user.get_street_address(), "street"),
            ("Oraș:", self.master.user.get_city(), "city"),
            ("Județ/Stat:", self.master.user.get_state(), "state"),
            ("Zi Naștere:", self.master.user.get_birthday(), "birthday")
        ]

        for label, value, key in fields:
            f = tk.Frame(left_col, bg=colors["bg"])
            f.pack(fill="x", pady=6)
            tk.Label(f, text=label, font=("Segoe UI", 10, "bold"), bg=colors["bg"], fg=txt_color, width=12,
                     anchor="w").pack(side="left")

            # Entry-uri cu contrast forțat
            ent = tk.Entry(f, bg=colors["input_bg"], fg=txt_color, relief="flat", font=("Segoe UI", 10),
                           insertbackground=txt_color)
            ent.insert(0, value if value else "")
            ent.pack(side="right", expand=True, fill="x", padx=(10, 0), ipady=3)
            self.entries[key] = ent

        tk.Button(left_col, text="💾 Salvează Profil", command=self.save_profile_data,
                  bg=colors.get("success", "#2ECC71"), fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(anchor="e", pady=(15, 0))

        # COLOANA DREAPTĂ: Schimbare Parolă
        right_col = tk.LabelFrame(main_profile_frame, text=" 🔒 Securitate ", font=("Segoe UI", 13, "bold"),
                                  bg=colors["bg"], fg=txt_color, padx=20, pady=20, relief="flat",
                                  highlightthickness=1, highlightbackground=colors["grid_line"])
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))

        pass_fields = [
            ("Parolă Veche:", "old_pass"),
            ("Parolă Nouă:", "new_pass"),
            ("Confirmă Parolă:", "confirm_pass")
        ]

        for label, key in pass_fields:
            f = tk.Frame(right_col, bg=colors["bg"])
            f.pack(fill="x", pady=10)
            tk.Label(f, text=label, font=("Segoe UI", 10, "bold"), bg=colors["bg"], fg=txt_color, width=15,
                     anchor="w").pack(side="left")
            ent = tk.Entry(f, show="*", bg=colors["input_bg"], fg=txt_color, relief="flat", font=("Segoe UI", 10),
                           insertbackground=txt_color)
            ent.pack(side="right", expand=True, fill="x", padx=(10, 0), ipady=3)
            self.pass_entries[key] = ent

        tk.Button(right_col, text="🔑 Schimbă Parola", command=self.handle_password_change,
                  bg=colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=15, pady=6, cursor="hand2").pack(anchor="e", pady=(20, 0))

        # --- Secțiune 2: ASPECT & TEMĂ ---
        aspect_frame = tk.LabelFrame(self.parent, text=" 🎨 Personalizare Aspect ", font=("Segoe UI", 13, "bold"),
                                     bg=colors["bg"], fg=txt_color, padx=25, pady=20, relief="flat",
                                     highlightthickness=1, highlightbackground=colors["grid_line"])
        aspect_frame.pack(fill="x", pady=(0, 20))

        t_controls = tk.Frame(aspect_frame, bg=colors["bg"])
        t_controls.pack(fill="x")

        tk.Label(t_controls, text="Variantă Temă:", font=("Segoe UI", 11, "bold"), bg=colors["bg"],
                 fg=txt_color).pack(side="left")

        self.theme_combo = ttk.Combobox(t_controls, values= sorted([
            "classic_dark", "classic_light", "dark_emerald", "dark_start", "midnight_blue", "forest_dark", "dracula",
            "cyberpunk",
            "material_ocean", "dark_oled", "nordic_frost", "light_soft", "github_light", "tokyo_night",
            "solarized_light", "sakura_blossom", "rosea_dark", "lavender_mist", "cotton_candy", "retro_terminal",
            "ocean_sunset", "nord_deep", "coffee_shop"
        ]), state="readonly", width=25, font=("Segoe UI", 11))
        self.theme_combo.set(self.master.settings_service.get_theme(uid))
        self.theme_combo.pack(side="left", padx=15)
        self.theme_combo.bind("<<ComboboxSelected>>", self.update_theme_preview)

        self.preview_canvas = tk.Canvas(t_controls, width=120, height=30, bg=colors["bg"], highlightthickness=0)
        self.preview_canvas.pack(side="left", padx=10)
        self.update_theme_preview()

        tk.Button(t_controls, text="Aplică Temă", command=self.apply_theme_change,
                  bg=colors["accent"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=5,
                  cursor="hand2").pack(side="right")

    def handle_password_change(self):
        old = self.pass_entries["old_pass"].get()
        new = self.pass_entries["new_pass"].get()
        confirm = self.pass_entries["confirm_pass"].get()

        if not old or not new:
            self.master.show_toast("⚠️ Completează parolele!", "#F1C40F")
            return

        if new != confirm:
            self.master.show_toast("❌ Parolele noi nu coincid!", "#E74C3C")
            return

        if hashlib.sha256(old.encode()).hexdigest() == self.master.user.get_password():
            new_user = self.master.user
            new_user.set_password(hashlib.sha256(new.encode()).hexdigest())
            self.master.user_service.modify_user(self.master.user, new_user)
            self.master.show_toast("✅ Parola a fost schimbată!")
            for e in self.pass_entries.values(): e.delete(0, tk.END)
        else:
            self.master.show_toast("❌ Parola actuală incorectă!", "#E74C3C")

    def save_profile_data(self):
        u = self.master.user
        # Actualizăm datele
        u.set_first_name(self.entries["first_name"].get())
        u.set_last_name(self.entries["last_name"].get())
        u.set_email(self.entries["email"].get())
        u.set_username(self.entries["username"].get())
        u.set_street_address(self.entries["street"].get())
        u.set_city(self.entries["city"].get())
        u.set_state(self.entries["state"].get())
        u.set_birthday(self.entries["birthday"].get())

        self.master.user_service.modify_user(self.master.user, u)
        self.master.show_toast("✅ Profil actualizat cu succes!")

    def update_theme_preview(self, event=None):
        selected = self.theme_combo.get()
        c = self.master.settings_service.get_colors_by_name(selected)
        if not c: return
        self.preview_canvas.delete("all")
        self.preview_canvas.create_oval(5, 5, 25, 25, fill=c["bg"], outline=c["fg"])
        self.preview_canvas.create_oval(35, 5, 55, 25, fill=c["accent"], outline=c["fg"])
        self.preview_canvas.create_oval(65, 5, 85, 25, fill=c.get("success", "#2ECC71"), outline=c["fg"])

    def apply_theme_change(self):
        uid = self.master.user.get_id_entity()
        self.master.settings_service.save_user_setting(uid, "tema", self.theme_combo.get())
        self.master.toggle_theme_ui()
        self.master.show_toast(f"🎨 Temă schimbată în {self.theme_combo.get()}")