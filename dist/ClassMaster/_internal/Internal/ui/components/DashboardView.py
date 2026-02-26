import tkinter as tk
from datetime import datetime


class DashboardView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller
        self.target_percent_var = tk.StringVar(value="0.0%")
        self.main_container = None
        self.target_title_var = tk.StringVar()

    def render(self):
        self.master.clear_content()
        uid = self.master.user.get_id_entity()
        colors = self.master.settings_service.get_colors(uid)
        ls = self.master.language_service

        self.main_container = tk.Frame(self.parent, bg=colors["bg"])
        self.main_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(self.main_container, bg=colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        scrollable_content = tk.Frame(canvas, bg=colors["bg"], padx=40, pady=20)
        canvas_window = canvas.create_window((0, 0), window=scrollable_content, anchor="nw")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _configure_window(event):
            canvas.itemconfig(canvas_window, width=event.width)

        def _update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", _configure_window)
        scrollable_content.bind("<Configure>", _update_scrollregion)

        # --- CALCULE DATE ---
        students = self.master.student_service.get_students_for_teacher(uid)
        num_students = len(students)
        total_income = sum(float(s.get_price()) for s in students)

        dist = {}
        for s in students:
            g_name = s.get_grade()
            dist[g_name] = dist.get(g_name, 0) + 1

        v8_count = dist.get("VIII", 0)
        initial_target = (v8_count / num_students * 100) if num_students > 0 else 0
        self.target_percent_var.set(f"{initial_target:.1f}%")
        self.target_title_var.set(f"{ls.get_text(uid, 'dash_target_title')} VIII")

        # --- CONSTRUIRE INTERFAȚĂ ---
        # Salutare tradusă
        welcome_text = ls.get_text(uid, "dash_welcome").replace("{name}", self.master.user.get_first_name())
        tk.Label(scrollable_content, text=welcome_text,
                 font=("Segoe UI", 28, "bold"), bg=colors["bg"], fg=colors["fg"]).pack(anchor="w", pady=(0, 30))

        cards_frame = tk.Frame(scrollable_content, bg=colors["bg"])
        cards_frame.pack(fill="x", pady=10)

        # Carduri de statistici traduse
        self.create_stat_card(cards_frame, ls.get_text(uid, "dash_active_students"), str(num_students),
                              colors["accent"], 0)
        self.create_stat_card(cards_frame, ls.get_text(uid, "dash_est_income"), f"{total_income} RON", "#27AE60", 1)
        self.create_target_card(cards_frame, self.target_title_var, self.target_percent_var, "#E67E22", 2)

        self.create_distribution_chart(scrollable_content, dist, num_students, colors)

        # --- AGENDA ---
        tk.Label(scrollable_content, text=f"📅 {ls.get_text(uid, 'dash_agenda_today')}", font=("Segoe UI", 18, "bold"),
                 bg=colors["bg"], fg=colors["fg"]).pack(anchor="w", pady=(30, 15))

        agenda_container = tk.Frame(scrollable_content, bg=colors["card_bg"], padx=20, pady=20,
                                    highlightthickness=1, highlightbackground=colors["grid_line"])
        agenda_container.pack(fill="x", pady=(0, 40))

        now = datetime.now()
        today_date_str = now.strftime("%Y-%m-%d")
        today_day_idx = now.weekday()
        current_time = now.strftime("%H:%M")

        sessions_today = []
        for key, data in self.master.schedule_service.get_schedule_data().items():
            if key.startswith(uid) and "_raw" in key:
                if today_date_str in key or f"_D{today_day_idx}_" in key:
                    sessions_today.append(data)

        if not sessions_today:
            tk.Label(agenda_container, text=ls.get_text(uid, "dash_no_sessions"),
                     font=("Segoe UI", 11, "italic"), bg=colors["card_bg"], fg="#888").pack(pady=10)
        else:
            sessions_today.sort(key=lambda x: x.get("time", "00:00"))
            for session in sessions_today:
                start_time = session.get("time", "00:00-00:00").split("-")[0]
                is_passed = current_time > start_time
                status_color = "#27AE60" if is_passed else colors["fg"]
                bg_row = colors["input_bg"] if not is_passed else colors["card_bg"]

                row = tk.Frame(agenda_container, bg=bg_row, pady=8, padx=10)
                row.pack(fill="x", pady=2)

                tk.Label(row, text=start_time, font=("Segoe UI", 11, "bold"), bg=bg_row, fg=status_color, width=8).pack(
                    side="left")
                tk.Label(row, text=session.get("group_name", ls.get_text(uid, "session_generic")),
                         font=("Segoe UI", 11), bg=bg_row, fg=status_color).pack(side="left", padx=20)

                status_text = ls.get_text(uid, "session_done") if is_passed else ls.get_text(uid, "session_pending")
                tk.Label(row, text=status_text, font=("Segoe UI", 9, "italic"),
                         bg=bg_row, fg=status_color).pack(side="right")

        # Buton rapid tradus
        tk.Button(scrollable_content, text=f"{ls.get_text(uid, 'dash_btn_full_schedule')} →",
                  font=("Segoe UI", 10, "bold"),
                  bg=colors["accent"], fg="white", relief="flat", padx=20, pady=10,
                  command=self.master.show_schedule, cursor="hand2").pack(anchor="e", pady=(0, 20))

    def create_target_card(self, parent, title_var, val_var, color, col):
        uid = self.master.user.get_id_entity()
        colors = self.master.settings_service.get_colors(uid)
        card = tk.Frame(parent, bg=colors["card_bg"], highlightthickness=1,
                        highlightbackground=colors["grid_line"], padx=25, pady=25)
        card.grid(row=0, column=col, padx=(0, 20), sticky="nw")
        tk.Label(card, textvariable=title_var, font=("Segoe UI", 8, "bold"), bg=colors["card_bg"], fg="#888").pack(
            anchor="w")
        tk.Label(card, textvariable=val_var, font=("Segoe UI", 28, "bold"), bg=colors["card_bg"], fg=color).pack(
            anchor="w", pady=(5, 0))

    def update_target(self, grade, count, total):
        uid = self.master.user.get_id_entity()
        ls = self.master.language_service
        percent = (count / total * 100) if total > 0 else 0
        self.target_title_var.set(f"{ls.get_text(uid, 'dash_target_title')} {grade}")
        self.target_percent_var.set(f"{percent:.1f}%")

    def create_distribution_chart(self, parent, distribution, total_students, colors):
        uid = self.master.user.get_id_entity()
        ls = self.master.language_service
        chart_frame = tk.Frame(parent, bg=colors["card_bg"], padx=25, pady=25,
                               highlightthickness=1, highlightbackground=colors["grid_line"])
        chart_frame.pack(fill="x", pady=25)

        tk.Label(chart_frame, text=ls.get_text(uid, "dash_dist_header"),
                 font=("Segoe UI", 10, "bold"), bg=colors["card_bg"], fg="#888").pack(anchor="w", pady=(0, 20))

        if not distribution:
            return
        max_val = max(distribution.values())
        class_text = ls.get_text(uid, "dash_class_label")
        students_text = ls.get_text(uid, "dash_students_label")

        for grade in sorted(distribution.keys()):
            count = distribution[grade]
            row = tk.Frame(chart_frame, bg=colors["card_bg"], cursor="hand2")
            row.pack(fill="x", pady=5)
            row.bind("<Button-1>", lambda e, g=grade, c=count: self.update_target(g, c, total_students))
            lbl = tk.Label(row, text=f"{class_text} {grade}", width=15, anchor="w", bg=colors["card_bg"],
                           fg=colors["fg"])
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda e, g=grade, c=count: self.update_target(g, c, total_students))
            bar_bg = tk.Frame(row, bg=colors["input_bg"], height=18, width=400)
            bar_bg.pack(side="left", padx=10)
            bar_bg.pack_propagate(False)
            bar_bg.bind("<Button-1>", lambda e, g=grade, c=count: self.update_target(g, c, total_students))
            bar = tk.Frame(bar_bg, bg=colors["accent"], height=18, width=(count / max_val) * 400)
            bar.pack(side="left")
            bar.bind("<Button-1>", lambda e, g=grade, c=count: self.update_target(g, c, total_students))
            txt = tk.Label(row, text=f"{count} {students_text}", bg=colors["card_bg"], fg=colors["fg"],
                           font=("Segoe UI", 10, "bold"))
            txt.pack(side="left", padx=5)
            txt.bind("<Button-1>", lambda e, g=grade, c=count: self.update_target(g, c, total_students))

    def create_stat_card(self, parent, title, value, color, col):
        uid = self.master.user.get_id_entity()
        colors = self.master.settings_service.get_colors(uid)
        card = tk.Frame(parent, bg=colors["card_bg"], highlightthickness=1,
                        highlightbackground=colors["grid_line"], padx=25, pady=25)
        card.grid(row=0, column=col, padx=(0, 20), sticky="nw")
        tk.Label(card, text=title.upper(), font=("Segoe UI", 8, "bold"), bg=colors["card_bg"], fg="#888").pack(
            anchor="w")
        tk.Label(card, text=value, font=("Segoe UI", 28, "bold"), bg=colors["card_bg"], fg=color).pack(anchor="w",
                                                                                                       pady=(5, 0))
