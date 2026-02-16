import tkinter as tk


class DashboardView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller

    def render(self):
        """Randarea paginii de start cu spațiere corectă."""
        self.master.clear_content()

        uid = self.master.user.get_id_entity()
        colors = self.master.settings_service.get_colors(uid)

        # Titlu principal cu spațiu generos dedesubt
        welcome_text = f"Salutare, {self.master.user.get_first_name()}!"
        tk.Label(self.parent, text=welcome_text,
                 font=("Segoe UI", 26, "bold"), bg=colors["bg"],
                 fg=colors["fg"]).pack(anchor="w", pady=(0, 20))

        # Containerul pentru carduri
        cards_frame = tk.Frame(self.parent, bg=colors["bg"])
        cards_frame.pack(fill="x", pady=10)

        # Calcul date
        num_students = len(self.master.student_service.get_students_for_teacher(uid))

        # Titlu card - dacă nu vrei să folosești LanguageService încă,
        # poți pune text direct: "Studenți Activi"
        card_title = self.master.language_service.get_text(uid, "stat_active_students")

        self.create_stat_card(cards_frame, card_title, str(num_students), colors["accent"], 0)

    def create_stat_card(self, parent, title, value, color, col):
        """Creează un card cu padding intern mai mare pentru aspect modern."""
        uid = self.master.user.get_id_entity()
        colors = self.master.settings_service.get_colors(uid)

        # Cardul în sine cu padding generos
        card = tk.Frame(parent, bg=colors["card_bg"], highlightthickness=1,
                        highlightbackground=colors["grid_line"], padx=30, pady=30)
        card.grid(row=0, column=col, padx=(0, 20), sticky="nw")

        # Titlul cardului - mai vizibil
        tk.Label(card, text=title.upper(), font=("Segoe UI", 9, "bold"),
                 bg=colors["card_bg"], fg="#888").pack(anchor="w")

        # Valoarea principală - mare și clară
        tk.Label(card, text=value, font=("Segoe UI", 36, "bold"),
                 bg=colors["card_bg"], fg=color).pack(anchor="w", pady=(10, 0))