import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry


class ScheduleView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller
        self.table_container = None
        self.canvas = None
        self.cal_select = None

        # --- LOGICĂ ZILE SELECTATE ---
        # Inițializăm cu Luni-Sâmbătă bifate (0-5), Duminică debifată (6)
        user_settings = self.master.settings_service.get_user_settings(self.master.user.get_id_entity())
        saved_days = user_settings.get("active_days", [0, 1, 2, 3, 4, 5])

        self.days_map = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
        self.selected_days = [tk.BooleanVar(value=(i in saved_days)) for i in range(7)]

    def render(self):
        """Metoda de randare cu contrast optimizat, selecție de zile și butoane preset."""
        uid = self.master.user.get_id_entity()
        self.master.colors = self.master.settings_service.get_colors(uid)
        colors = self.master.colors

        header_frame = tk.Frame(self.parent, bg=colors["bg"])
        header_frame.pack(fill="x", pady=(0, 10))

        # --- Navigare și Calendar ---
        nav_frame = tk.Frame(header_frame, bg=colors["bg"])
        nav_frame.pack(side="left")

        tk.Button(nav_frame, text="◀", command=self.master.prev_week,
                  bg=colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="left", padx=5)

        tk.Button(nav_frame, text="📅 Astăzi", command=self.master.go_to_today,
                  bg=colors["card_bg"], fg=colors.get("schedule_text", "#FFFFFF"),
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                  padx=10).pack(side="left", padx=5)

        self.cal_select = DateEntry(nav_frame, width=15, background=colors["accent"],
                                    foreground='white', headersbackground=colors["sidebar_bg"],
                                    headersforeground="white", borderwidth=2, font=("Segoe UI", 11, "bold"),
                                    date_pattern='dd/mm/yyyy', locale='ro_RO')
        self.cal_select.set_date(self.master.current_date)
        self.cal_select.pack(side="left", padx=10)
        self.cal_select.bind("<<DateEntrySelected>>", self.master.on_date_selected)

        tk.Button(nav_frame, text="▶", command=self.master.next_week,
                  bg=colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="left", padx=5)

        # --- BUTOANE PRESET (REPARAT) ---
        tk.Button(nav_frame, text="💾 Salvează Preset", command=self.master.save_as_preset,
                  bg=colors.get("success", "#27AE60"), fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=10, cursor="hand2").pack(side="left", padx=(25, 5))

        # ACESTA ESTE BUTONUL CARE LIPSEA:
        tk.Button(nav_frame, text="📋 Aplică Preset", command=self.master.open_presets_manager,
                  bg="#8E44AD", fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=10, cursor="hand2").pack(side="left", padx=5)

        # --- Panou Selecție Zile ---
        days_selection_frame = tk.Frame(self.parent, bg=colors["bg"])
        days_selection_frame.pack(fill="x", pady=(0, 15))

        tk.Label(days_selection_frame, text="Afișează zilele:", font=("Segoe UI", 9, "bold"),
                 bg=colors["bg"], fg=colors["fg"]).pack(side="left", padx=(0, 10))

        for i, day_name in enumerate(self.days_map):
            cb = tk.Checkbutton(days_selection_frame, text=day_name, variable=self.selected_days[i],
                                bg=colors["bg"], fg=colors["fg"], selectcolor=colors["card_bg"],
                                activebackground=colors["bg"], activeforeground=colors["accent"],
                                font=("Segoe UI", 9),
                                command=self.update_days_persistence)
            cb.pack(side="left", padx=5)

        # --- Control Rânduri (Spinbox) ---
        rows_control = tk.Frame(header_frame, bg=colors["bg"])
        rows_control.pack(side="right")

        tk.Spinbox(rows_control, from_=2, to=20, textvariable=self.master.rows_var, width=5,
                   command=self.master.update_rows_count, bg=colors["input_bg"],
                   fg=colors["fg"], buttonbackground=colors["input_bg"]).pack(side="right", padx=10)

        # --- Container Tabel (Scrollable) ---
        canvas_container = tk.Frame(self.parent, bg=colors["bg"])
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg=colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)

        self.table_container = tk.Frame(self.canvas, bg=colors["bg"])
        self.canvas.create_window((0, 0), window=self.table_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.table_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.draw_grid()
        self.render_stats_panel(colors)

    def update_days_persistence(self):
        """Salvează starea curentă a bifelor în setări și re-randează grid-ul."""
        uid = self.master.user.get_id_entity()
        # Colectăm indicii zilelor bifate
        active_indices = [i for i, var in enumerate(self.selected_days) if var.get()]

        # Salvăm în serviciul de setări
        self.master.settings_service.save_active_days(uid, active_indices)

        # Re-desenăm grid-ul pentru a reflecta schimbarea
        self.draw_grid()

    def draw_grid(self):
        """Desenarea dinamică a grid-ului cu lățime adaptivă."""
        for widget in self.table_container.winfo_children():
            widget.destroy()

        colors = self.master.colors
        start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())
        num_rows = self.master.rows_var.get()

        # Filtrăm zilele care trebuie afișate
        active_days_indices = [i for i, var in enumerate(self.selected_days) if var.get()]
        num_active_days = len(active_days_indices)

        if num_active_days == 0:
            tk.Label(self.table_container, text="Vă rugăm selectați cel puțin o zi.",
                     bg=colors["bg"], fg=colors["fg"], font=("Segoe UI", 12)).pack(pady=50)
            return

        # --- CALCUL LĂȚIME ADAPTIVĂ ---
        # Dacă avem multe zile (ex: 7), scădem minsize pentru a forța încadrarea în ecran
        dynamic_minsize = 140 if num_active_days > 5 else 180

        # Randare Headere Coloane
        for col_idx, day_idx in enumerate(active_days_indices):
            data_zi = start_of_week + timedelta(days=day_idx)
            data_str = data_zi.strftime('%Y-%m-%d')
            total_venit = self.calculate_daily_total(data_str)

            nume = self.days_map[day_idx]
            text_header = f"{nume} ({data_zi.strftime('%d.%m')})\n{total_venit} RON"

            # Setăm weight=1 pentru ca spațiul să se distribuie egal
            self.table_container.grid_columnconfigure(col_idx, weight=1, minsize=dynamic_minsize)

            tk.Label(self.table_container, text=text_header, font=("Segoe UI", 9, "bold"),
                     bg=colors["accent"], fg="white", pady=10).grid(row=0, column=col_idx, sticky="nsew", padx=1,
                                                                    pady=1)

        # Randare Celule Date
        for row in range(1, num_rows + 1):
            self.table_container.grid_rowconfigure(row, weight=0, minsize=120)
            for col_idx, day_idx in enumerate(active_days_indices):
                data_zi = start_of_week + timedelta(days=day_idx)
                cell_id = f"{data_zi.strftime('%Y-%m-%d')}_R{row}"
                self.render_cell(row, col_idx, cell_id)

        # Randare Celule Date
        for row in range(1, num_rows + 1):
            self.table_container.grid_rowconfigure(row, weight=0, minsize=120)
            for col_idx, day_idx in enumerate(active_days_indices):
                data_zi = start_of_week + timedelta(days=day_idx)
                cell_id = f"{data_zi.strftime('%Y-%m-%d')}_R{row}"
                self.render_cell(row, col_idx, cell_id)

    # ... (Metodele render_cell, calculate_weekly_stats, etc. rămân neschimbate) ...

    def render_cell(self, row, col, cell_id):
        """Randarea unei celule (Neschimbată, dar primește coordonate dinamice)."""
        uid = self.master.user.get_id_entity()
        unique_key = f"{uid}_{cell_id}"
        raw_data = self.master.schedule_data.get(f"{unique_key}_raw", {})

        group_name = raw_data.get('group_name', "")
        time_val = raw_data.get('time', "")
        colors = self.master.colors

        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        today_str = now.strftime("%Y-%m-%d")
        end_of_current_week = (now + timedelta(days=(6 - now.weekday()))).strftime("%Y-%m-%d")
        cell_date = cell_id.split('_')[0]

        bg_color = colors["card_bg"]
        text_color = colors.get("schedule_text", colors["fg"])

        if group_name and time_val and "-" in time_val:
            try:
                start_t, end_t = time_val.split("-")
                soft_green_bg, soft_green_fg = "#1B3D2F", "#A5D6A7"
                soft_yellow_bg, soft_yellow_fg = "#3D3A1B", "#FFF59D"

                if colors.get("theme") == "light":
                    soft_green_bg, soft_green_fg = "#F1F8E9", "#2E7D32"
                    soft_yellow_bg, soft_yellow_fg = "#FFFDE7", "#F9A825"

                if cell_date < today_str:
                    bg_color, text_color = soft_green_bg, soft_green_fg
                elif today_str <= cell_date <= end_of_current_week:
                    if cell_date == today_str:
                        if current_time_str > end_t:
                            bg_color, text_color = soft_green_bg, soft_green_fg
                        elif current_time_str < start_t:
                            bg_color, text_color = soft_yellow_bg, soft_yellow_fg
                        else:
                            bg_color, text_color = colors["accent"], "white"
                    else:
                        bg_color, text_color = soft_yellow_bg, soft_yellow_fg
                else:
                    bg_color = colors["card_bg"]
                    text_color = colors.get("schedule_text", colors["fg"])
            except:
                pass

        cell_frame = tk.Frame(self.table_container, bg=bg_color, highlightthickness=1,
                              highlightbackground=colors["grid_line"])
        cell_frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # (Restul logicii de populare a celulei cu label-uri student rămâne la fel)
        cell_frame.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))
        time_lbl = tk.Label(cell_frame, text=time_val, font=("Segoe UI", 10, "bold"),
                            bg=bg_color, fg=text_color, width=10, anchor="center")
        time_lbl.pack(side="left", fill="y", padx=(2, 0))
        time_lbl.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))

        if group_name:
            tk.Frame(cell_frame, width=1, bg=colors["grid_line"]).pack(side="left", fill="y", padx=2)
            details = tk.Frame(cell_frame, bg=bg_color)
            details.pack(side="left", fill="both", expand=True, padx=2, pady=5)
            tk.Label(details, text=group_name, font=("Segoe UI", 10, "bold"),
                     bg=bg_color, fg=text_color, anchor="nw").pack(fill="x")

            group_id = raw_data.get('group_id')
            students = self.master.student_service.get_students_by_id_list(
                self.master.group_service.get_group_students(group_id))
            absentees = raw_data.get('absentees', [])

            for s in students:
                sid = s.get_id_entity()
                is_absent = sid in absentees
                lbl_color = "#E57373" if is_absent else text_color
                lbl_font = ("Segoe UI", 9, "overstrike") if is_absent else ("Segoe UI", 9)
                s_lbl = tk.Label(details, text=f"• {s.get_first_name()}", font=lbl_font,
                                 bg=bg_color, fg=lbl_color, anchor="w", cursor="hand2")
                s_lbl.pack(fill="x")
                s_lbl.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))
                s_lbl.bind("<Button-3>", lambda e, cid=cell_id, stid=sid: self.master.toggle_absentee(cid, stid))

    def calculate_weekly_stats(self):
        """Calcul financiar extins la 7 zile dacă sunt selectate."""
        v_maxim, v_actual = 0, 0
        uid = self.master.user.get_id_entity()
        num_rows = self.master.rows_var.get()
        now = datetime.now()
        today_str, current_time_str = now.strftime('%Y-%m-%d'), now.strftime('%H:%M')
        start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())

        for i in range(7):  # Verificăm toate cele 7 zile
            data_zi = start_of_week + timedelta(days=i)
            data_str = data_zi.strftime('%Y-%m-%d')
            for r in range(1, num_rows + 1):
                cell_key = f"{uid}_{data_str}_R{r}"
                raw_data = self.master.schedule_data.get(f"{cell_key}_raw", {})
                if raw_data:
                    group_id = raw_data.get('group_id')
                    try:
                        end_t = raw_data.get('time', "00:00-00:00").split("-")[1]
                    except:
                        end_t = "00:00"

                    students = self.master.student_service.get_students_by_id_list(
                        self.master.group_service.get_group_students(group_id))
                    absentees = raw_data.get('absentees', [])
                    is_past = (data_str < today_str) or (data_str == today_str and current_time_str > end_t)

                    for s in students:
                        try:
                            price = float(s.get_price())
                            v_maxim += price
                            if is_past and s.get_id_entity() not in absentees: v_actual += price
                        except:
                            continue
        return int(v_maxim), int(v_actual)

    def render_stats_panel(self, colors):
        """Panou financiar complet cu Potențial și Încasat."""
        v_maxim, v_actual = self.calculate_weekly_stats()

        # Container principal
        stats_frame = tk.Frame(self.parent, bg=colors["card_bg"],
                               highlightthickness=2, highlightbackground=colors["grid_line"],
                               padx=20, pady=15)
        stats_frame.place(relx=0.97, rely=0.94, anchor="se")

        tk.Label(stats_frame, text="REZUMAT FINANCIAR", font=("Segoe UI", 8, "bold"),
                 bg=colors["card_bg"], fg=colors.get("sub", "#888")).pack(anchor="e", pady=(0, 10))

        # Divider orizontal
        tk.Frame(stats_frame, height=1, bg=colors["grid_line"]).pack(fill="x", pady=(0, 10))

        # --- Zona Venit Potențial (Maxim) ---
        max_container = tk.Frame(stats_frame, bg=colors["card_bg"])
        max_container.pack(fill="x", anchor="e")

        tk.Label(max_container, text="Potențial:", font=("Segoe UI", 11),
                 bg=colors["card_bg"], fg=colors.get("sub", "#888")).pack(side="left")
        tk.Label(max_container, text=f"{v_maxim} RON", font=("Segoe UI", 16, "bold"),
                 bg=colors["card_bg"], fg=colors["accent"]).pack(side="right", padx=(10, 0))

        # --- Zona Venit Încasat (Realizat până acum) ---
        real_container = tk.Frame(stats_frame, bg=colors["card_bg"])
        real_container.pack(fill="x", anchor="e", pady=(5, 0))

        tk.Label(real_container, text="Încasat:", font=("Segoe UI", 11, "bold"),
                 bg=colors["card_bg"], fg=colors["fg"]).pack(side="left")

        tk.Label(real_container, text=f"{v_actual} RON", font=("Segoe UI", 16, "bold"),
                 bg=colors["card_bg"], fg=colors.get("success", "#2ECC71")).pack(side="right", padx=(10, 0))

        # --- Indicator Eficiență ---
        if v_maxim > 0:
            procent = int((v_actual / v_maxim) * 100)
            color_eff = colors.get("success", "#2ECC71") if procent > 80 else "#F1C40F"

            eff_label = tk.Label(stats_frame, text=f"Eficiență: {procent}%", font=("Segoe UI", 8, "italic"),
                                 bg=colors["card_bg"], fg=color_eff)
            eff_label.pack(anchor="e", pady=(5, 0))

    def _on_mousewheel(self, event):
        if self.canvas and self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def calculate_daily_total(self, date_str):
        """Calcul venit zilnic."""
        total = 0
        uid = self.master.user.get_id_entity()
        num_rows = self.master.rows_var.get()
        for r in range(1, num_rows + 1):
            cell_key = f"{uid}_{date_str}_R{r}"
            raw_data = self.master.schedule_data.get(f"{cell_key}_raw", {})
            if raw_data:
                group_id = raw_data.get('group_id')
                students = self.master.student_service.get_students_by_id_list(
                    self.master.group_service.get_group_students(group_id))
                absentees = raw_data.get('absentees', [])
                for s in students:
                    if s.get_id_entity() not in absentees:
                        try:
                            total += float(s.get_price())
                        except:
                            continue
        return int(total)
