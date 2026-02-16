import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry


class ScheduleView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller
        self.table_container = None
        self.canvas = None
        self.cal_select = None

    def render(self):
        """Metoda de randare cu contrast optimizat și panou de statistici."""
        uid = self.master.user.get_id_entity()
        self.master.colors = self.master.settings_service.get_colors(uid)
        colors = self.master.colors

        header_frame = tk.Frame(self.parent, bg=colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))

        # --- Navigare și Calendar ---
        nav_frame = tk.Frame(header_frame, bg=colors["bg"])
        nav_frame.pack(side="left")

        tk.Button(nav_frame, text="◀", command=self.master.prev_week,
                  bg=colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="left", padx=5)

        tk.Button(nav_frame, text="📅 Astăzi", command=self.master.go_to_today,
                  bg=colors["card_bg"], fg=colors.get("schedule_text", "#FFFFFF"),
                  font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2",
                  padx=10).pack(side="left", padx=5)

        self.cal_select = DateEntry(nav_frame, width=20, background=colors["accent"],
                                    foreground='white', headersbackground=colors["sidebar_bg"],
                                    headersforeground="white", borderwidth=2, font=("Segoe UI", 12, "bold"),
                                    date_pattern='dd/mm/yyyy', locale='ro_RO')
        self.cal_select.set_date(self.master.current_date)
        self.cal_select.pack(side="left", padx=10)
        self.cal_select.bind("<<DateEntrySelected>>", self.master.on_date_selected)

        tk.Button(nav_frame, text="▶", command=self.master.next_week,
                  bg=colors["accent"], fg="white", relief="flat", cursor="hand2").pack(side="left", padx=5)

        # --- Butoane Preset ---
        tk.Button(nav_frame, text="💾 Salvează Preset", command=self.master.save_as_preset,
                  bg=colors.get("success", "#27AE60"), fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=10, cursor="hand2").pack(side="left", padx=(25, 5))

        tk.Button(nav_frame, text="📋 Aplică Preset", command=self.master.open_presets_manager,
                  bg="#8E44AD", fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=10, cursor="hand2").pack(side="left", padx=5)

        # --- Control Rânduri ---
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

        # --- Panou Statistici Financiare (Dreapta Jos) ---
        self.render_stats_panel(colors)

    def render_stats_panel(self, colors):
        """Creează un widget financiar modern fără opțiuni invalide."""
        v_maxim, v_actual = self.calculate_weekly_stats()

        # Container principal
        stats_frame = tk.Frame(self.parent, bg=colors["card_bg"],
                               highlightthickness=2, highlightbackground=colors["grid_line"],
                               padx=20, pady=15)
        # Plasare precisă în colțul din dreapta jos
        stats_frame.place(relx=0.97, rely=0.94, anchor="se")

        # Titlu Secțiune - Am eliminat -letterspace pentru a repara eroarea
        tk.Label(stats_frame, text="REZUMAT FINANCIAR", font=("Segoe UI", 8, "bold"),
                 bg=colors["card_bg"], fg=colors.get("sub", "#888")).pack(anchor="e", pady=(0, 10))

        # Divider orizontal
        tk.Frame(stats_frame, height=1, bg=colors["grid_line"]).pack(fill="x", pady=(0, 10))

        # --- Zona Venit Maxim ---
        max_container = tk.Frame(stats_frame, bg=colors["card_bg"])
        max_container.pack(fill="x", anchor="e")

        tk.Label(max_container, text="Potențial:", font=("Segoe UI", 9),
                 bg=colors["card_bg"], fg=colors.get("sub", "#888")).pack(side="left")
        tk.Label(max_container, text=f"{v_maxim} RON", font=("Segoe UI", 10, "bold"),
                 bg=colors["card_bg"], fg=colors["accent"]).pack(side="right", padx=(10, 0))

        # --- Zona Venit Real ---
        real_container = tk.Frame(stats_frame, bg=colors["card_bg"])
        real_container.pack(fill="x", anchor="e", pady=(5, 0))

        tk.Label(real_container, text="Încasat:", font=("Segoe UI", 11, "bold"),
                 bg=colors["card_bg"], fg=colors["fg"]).pack(side="left")

        # Suma principală
        tk.Label(real_container, text=f"{v_actual} RON", font=("Segoe UI", 16, "bold"),
                 bg=colors["card_bg"], fg=colors.get("success", "#2ECC71")).pack(side="right", padx=(10, 0))

        # --- Indicator Eficiență ---
        if v_maxim > 0:
            procent = int((v_actual / v_maxim) * 100)
            color_eff = colors.get("success", "#2ECC71") if procent > 80 else "#F1C40F"

            eff_label = tk.Label(stats_frame, text=f"Eficiență: {procent}%", font=("Segoe UI", 8, "italic"),
                                 bg=colors["card_bg"], fg=color_eff)
            eff_label.pack(anchor="e", pady=(5, 0))

    def calculate_weekly_stats(self):
        """Parcurge saptamana curenta pentru a genera totalurile."""
        v_maxim = 0
        v_actual = 0
        uid = self.master.user.get_id_entity()
        num_rows = self.master.rows_var.get()
        start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())

        for i in range(6):  # Luni-Sâmbătă
            data_str = (start_of_week + timedelta(days=i)).strftime('%Y-%m-%d')
            for r in range(1, num_rows + 1):
                cell_key = f"{uid}_{data_str}_R{r}"
                raw_data = self.master.schedule_data.get(f"{cell_key}_raw", {})
                if raw_data:
                    group_id = raw_data.get('group_id')
                    students = self.master.student_service.get_students_by_id_list(
                        self.master.group_service.get_group_students(group_id))
                    absentees = raw_data.get('absentees', [])
                    for s in students:
                        try:
                            price = float(s.get_price())
                            v_maxim += price
                            if s.get_id_entity() not in absentees:
                                v_actual += price
                        except:
                            continue
        return int(v_maxim), int(v_actual)

    def _on_mousewheel(self, event):
        if self.canvas and self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def calculate_daily_total(self, date_str):
        """Calculează venitul pe zi scăzând prețul absenților."""
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

    def draw_grid(self):
        """Desenarea grid-ului cu totaluri financiare dinamice."""
        for widget in self.table_container.winfo_children():
            widget.destroy()

        colors = self.master.colors
        start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())
        zile_nume = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă"]
        num_rows = self.master.rows_var.get()

        for i, nume in enumerate(zile_nume):
            data_zi = start_of_week + timedelta(days=i)
            data_str = data_zi.strftime('%Y-%m-%d')
            total_venit = self.calculate_daily_total(data_str)
            text_header = f"{nume} ({data_zi.strftime('%d.%m')})\n{total_venit} RON"

            self.table_container.grid_columnconfigure(i, weight=1, minsize=180)
            tk.Label(self.table_container, text=text_header, font=("Segoe UI", 10, "bold"),
                     bg=colors["accent"], fg="white", pady=10).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row in range(1, num_rows + 1):
            self.table_container.grid_rowconfigure(row, weight=0, minsize=120)
            for col in range(len(zile_nume)):
                data_zi = start_of_week + timedelta(days=col)
                cell_id = f"{data_zi.strftime('%Y-%m-%d')}_R{row}"
                self.render_cell(row, col, cell_id)

    def render_cell(self, row, col, cell_id):
        """Randarea unei celule cu contrast optimizat."""
        uid = self.master.user.get_id_entity()
        unique_key = f"{uid}_{cell_id}"
        raw_data = self.master.schedule_data.get(f"{unique_key}_raw", {})

        group_name = raw_data.get('group_name', "")
        time_val = raw_data.get('time', "")
        colors = self.master.colors

        # Preluăm culoarea textului dedicată din temă
        text_color = colors.get("schedule_text", colors["fg"])

        bg_color = colors["card_bg"]
        if group_name:
            current_theme = self.master.settings_service.get_theme(uid)
            bg_color = colors["input_bg"] if "dark" in current_theme or "midnight" in current_theme else "#EBF5FB"

        cell_frame = tk.Frame(self.table_container, bg=bg_color, highlightthickness=1,
                              highlightbackground=colors["grid_line"])
        cell_frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        cell_frame.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))

        time_lbl = tk.Label(cell_frame, text=time_val, font=("Segoe UI", 10, "bold"),
                            bg=bg_color, fg=text_color, width=10, anchor="center")
        time_lbl.pack(side="left", fill="y", padx=(2, 0))
        time_lbl.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))

        if group_name:
            tk.Frame(cell_frame, width=1, bg=colors["grid_line"]).pack(side="left", fill="y", padx=2)
            details = tk.Frame(cell_frame, bg=bg_color)
            details.pack(side="left", fill="both", expand=True, padx=2, pady=5)
            details.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))

            tk.Label(details, text=group_name, font=("Segoe UI", 10, "bold"),
                     bg=bg_color, fg=text_color, anchor="nw").pack(fill="x")

            group_id = raw_data.get('group_id')
            students = self.master.student_service.get_students_by_id_list(
                self.master.group_service.get_group_students(group_id))
            absentees = raw_data.get('absentees', [])

            for s in students:
                sid = s.get_id_entity()
                is_absent = sid in absentees

                if is_absent:
                    lbl_color = "#FF5555" if text_color == "#FFFFFF" else "#E74C3C"
                    lbl_font = ("Segoe UI", 9, "overstrike")
                else:
                    lbl_color = text_color
                    lbl_font = ("Segoe UI", 9)

                s_lbl = tk.Label(details, text=f"• {s.get_first_name()}", font=lbl_font,
                                 bg=bg_color, fg=lbl_color, anchor="w", cursor="hand2")
                s_lbl.pack(fill="x")

                s_lbl.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))
                s_lbl.bind("<Button-3>", lambda e, cid=cell_id, stid=sid: self.master.toggle_absentee(cid, stid))