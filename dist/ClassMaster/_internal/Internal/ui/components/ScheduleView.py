import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry


# def get_dynamic_colors(cell_id, raw_data, colors):
#     if not raw_data.get('group_name'):
#         return colors["card_bg"], colors["fg"]
#     now = datetime.now()
#     today_str = now.strftime("%Y-%m-%d")
#     curr_t = now.strftime("%H:%M")
#     cell_date = cell_id.split('_')[0]
#     end_of_current_week = (now + timedelta(days=(6 - now.weekday()))).strftime("%Y-%m-%d")
#
#     try:
#         start_t, end_t = raw_data.get('time', "00:00-00:00").split("-")
#         if cell_date < today_str or (cell_date == today_str and curr_t > end_t):
#             return colors.get("schedule_past_bg", "#1B3D2F"), colors.get("schedule_past_fg", "#A5D6A7")
#         if cell_date == today_str and start_t <= curr_t <= end_t:
#             return colors["accent"], "white"
#         if cell_date == today_str:
#             return colors.get("schedule_today_bg", "#1A237E"), colors.get("schedule_today_fg", "#E8EAF6")
#         if today_str < cell_date <= end_of_current_week:
#             return colors.get("schedule_future_bg", "#3D3A1B"), colors.get("schedule_future_fg", "#FFF59D")
#     except Exception as e:
#         print(e)
#         pass
#     return colors["card_bg"], colors["fg"]

def get_dynamic_colors(cell_id, raw_data, colors):
    if not raw_data.get('group_name'):
        return colors["card_bg"], colors["fg"]

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    curr_t = now.strftime("%H:%M")
    cell_date_str = cell_id.split('_')[0]
    cell_date_obj = datetime.strptime(cell_date_str, "%Y-%m-%d")
    start_of_current_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        time_range = raw_data.get('time', "00:00-00:00")
        start_t, end_t = time_range.split("-")

        # SĂPTĂMÂNI TRECUTE COMPLET ---
        if cell_date_obj < start_of_current_week:
            return colors.get("schedule_past_bg", "#2C2C2C"), colors.get("schedule_past_fg", "#777777")

        # ȘEDINȚE TERMINATE (Azi sau în sapt. curentă) ---
        if cell_date_str < today_str or (cell_date_str == today_str and curr_t > end_t):
            return colors.get("schedule_past_bg", "#1B3D2F"), colors.get("schedule_past_fg", "#A5D6A7")

        # ȘEDINȚA ACTIVĂ CHIAR ACUM ---
        if cell_date_str == today_str and start_t <= curr_t <= end_t:
            return colors["accent"], "white"

        # ȘEDINȚE CARE URMEAZĂ *AZI* (Culoare specială) ---
        if cell_date_str == today_str and curr_t < start_t:
            return colors.get("schedule_upcoming_today_bg", "#D35400"), "white"

        # ȘEDINȚE DIN ZILELE VIITOARE ALE SĂPTĂMÂNII ---
        return colors.get("schedule_future_bg", "#3D3A1B"), colors.get("schedule_future_fg", "#FFF59D")

    except Exception as e:
        print(f"Eroare culori: {e}")

    return colors["card_bg"], colors["fg"]


class ScheduleView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller
        self.table_container = None
        self.canvas = None
        self.cal_select = None

        # --- LOGICĂ ZILE SELECTATE (PERSISTENTĂ) ---
        uid = self.master.user.get_id_entity()
        user_settings = self.master.settings_service.get_user_settings(uid)
        saved_days = user_settings.get("active_days", [0, 1, 2, 3, 4, 5])

        # Preluăm numele zilelor traduse din LanguageService
        ls = self.master.language_service
        self.days_map = [
            ls.get_text(uid, "day_mon"),
            ls.get_text(uid, "day_tue"),
            ls.get_text(uid, "day_wed"),
            ls.get_text(uid, "day_thu"),
            ls.get_text(uid, "day_fri"),
            ls.get_text(uid, "day_sat"),
            ls.get_text(uid, "day_sun")
        ]
        self.selected_days = [tk.BooleanVar(value=(i in saved_days)) for i in range(7)]

    def render(self):
        """Metoda de randare principală cu suport multilingv."""
        uid = self.master.user.get_id_entity()
        ls = self.master.language_service
        self.days_map = [
            ls.get_text(uid, "day_mon"),
            ls.get_text(uid, "day_tue"),
            ls.get_text(uid, "day_wed"),
            ls.get_text(uid, "day_thu"),
            ls.get_text(uid, "day_fri"),
            ls.get_text(uid, "day_sat"),
            ls.get_text(uid, "day_sun")
        ]
        self.master.clear_content()
        uid = self.master.user.get_id_entity()
        ls = self.master.language_service
        self.master.colors = self.master.settings_service.get_colors(uid)
        colors = self.master.colors

        # --- Top Bar Stilizat ---
        header_frame = tk.Frame(self.parent, bg=colors["bg"], pady=15)
        header_frame.pack(fill="x")

        # Container Navigare (Stânga)
        nav_frame = tk.Frame(header_frame, bg=colors["bg"])
        nav_frame.pack(side="left", padx=20)

        # Buton "Astăzi" tradus
        today_btn_text = ls.get_text(uid, "btn_today")
        for btn_text, cmd in [("◀", self.master.prev_week), (f"📅 {today_btn_text}", self.master.go_to_today),
                              ("▶", self.master.next_week)]:
            tk.Button(nav_frame, text=btn_text, command=cmd,
                      bg=colors["card_bg"], fg=colors["accent"], font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=15, pady=8, cursor="hand2").pack(side="left", padx=3)

        # Configurare Locale Calendar în funcție de limba aleasă
        user_lang = self.master.settings_service.get_user_settings(uid).get("language", "ro")
        cal_locale = 'ro_RO' if user_lang == 'ro' else 'en_US'

        self.cal_select = DateEntry(nav_frame, width=14, background=colors["accent"],
                                    foreground='white', font=("Segoe UI", 11),
                                    date_pattern='dd.mm.yyyy', locale=cal_locale)
        self.cal_select.set_date(self.master.current_date)
        self.cal_select.pack(side="left", padx=15)
        self.cal_select.bind("<<DateEntrySelected>>", self.master.on_date_selected)

        # Container Acțiuni (Dreapta)
        actions_frame = tk.Frame(header_frame, bg=colors["bg"])
        actions_frame.pack(side="right", padx=20)

        # Butoane Preset traduse
        tk.Button(actions_frame, text=f"💾 {ls.get_text(uid, 'btn_save_preset')}", command=self.master.save_as_preset,
                  bg=colors.get("success", "#27AE60"), fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=15, pady=8, cursor="hand2").pack(side="left", padx=5)

        tk.Button(actions_frame, text=f"📋 {ls.get_text(uid, 'btn_apply_preset')}",
                  command=self.master.open_presets_manager,
                  bg="#8E44AD", fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), padx=15, pady=8, cursor="hand2").pack(side="left", padx=5)

        # --- Panou Selecție Zile (Centrat) ---
        days_selection_frame = tk.Frame(self.parent, bg=colors["bg"], pady=10)
        days_selection_frame.pack(fill="x")

        days_inner = tk.Frame(days_selection_frame, bg=colors["bg"])
        days_inner.pack(anchor="center")

        # Etichetă zile active tradusă
        tk.Label(days_inner, text=f"{ls.get_text(uid, 'label_active_days')}:", font=("Segoe UI", 9, "bold"),
                 bg=colors["bg"], fg=colors.get("sub", "#888")).pack(side="left", padx=10)

        for i, day_name in enumerate(self.days_map):
            cb = tk.Checkbutton(days_inner, text=day_name, variable=self.selected_days[i],
                                bg=colors["bg"], fg=colors["fg"], selectcolor=colors["card_bg"],
                                activebackground=colors["bg"], font=("Segoe UI", 10),
                                command=self.update_days_persistence)
            cb.pack(side="left", padx=10)

        # --- Grid Container ---
        grid_outer_container = tk.Frame(self.parent, bg=colors["bg"])
        grid_outer_container.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        self.canvas = tk.Canvas(grid_outer_container, bg=colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_outer_container, orient="vertical", command=self.canvas.yview)

        self.table_container = tk.Frame(self.canvas, bg=colors["grid_line"])
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
        uid = self.master.user.get_id_entity()
        active_indices = [i for i, var in enumerate(self.selected_days) if var.get()]
        self.master.settings_service.save_active_days(uid, active_indices)
        self.draw_grid()

    # def draw_grid(self):
    #     """Desenarea grid-ului cu CELULE MARI și format dată RO."""
    #     for widget in self.table_container.winfo_children():
    #         widget.destroy()
    #
    #     for i in range(10):
    #         self.table_container.grid_columnconfigure(i, weight=0, minsize=0)
    #
    #     colors = self.master.colors
    #     now = datetime.now()
    #     start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())
    #     num_rows = 5
    #     if self.master.rows_var:
    #         num_rows = self.master.rows_var.get()
    #
    #     active_days_indices = [i for i, var in enumerate(self.selected_days) if var.get()]
    #     if not active_days_indices:
    #         return
    #
    #     dynamic_minsize = 160 if len(active_days_indices) > 5 else 220
    #
    #     for col_idx, day_idx in enumerate(active_days_indices):
    #         self.table_container.grid_columnconfigure(col_idx, weight=1, minsize=dynamic_minsize)
    #         data_zi = start_of_week + timedelta(days=day_idx)
    #         data_str = data_zi.strftime('%Y-%m-%d')
    #
    #         is_today = (data_str == now.strftime('%Y-%m-%d'))
    #         header_bg = colors["accent"] if not is_today else "#CD5C5C"
    #
    #         h_frame = tk.Frame(self.table_container, bg=header_bg, pady=15)
    #         h_frame.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
    #
    #         tk.Label(h_frame, text=self.days_map[day_idx].upper(), font=("Segoe UI", 8, "bold"),
    #                  bg=header_bg, fg="white").pack()
    #         tk.Label(h_frame, text=data_zi.strftime('%d.%m.%Y'), font=("Segoe UI", 12, "bold"),
    #                  bg=header_bg, fg="white").pack(pady=3)
    #         tk.Label(h_frame, text=f"{self.calculate_daily_total(data_str)} RON", font=("Segoe UI", 9, "italic"),
    #                  bg=header_bg, fg="white").pack()
    #
    #     for row in range(1, num_rows + 1):
    #         self.table_container.grid_rowconfigure(row, weight=0, minsize=145)
    #         for col_idx, day_idx in enumerate(active_days_indices):
    #             data_zi = start_of_week + timedelta(days=day_idx)
    #             cell_id = f"{data_zi.strftime('%Y-%m-%d')}_R{row}"
    #             self.render_cell(row, col_idx, cell_id)
    def draw_grid(self):
        """Desenarea grid-ului cu diferențiere vizuală pentru săptămânile trecute."""
        for widget in self.table_container.winfo_children():
            widget.destroy()

        for i in range(10):
            self.table_container.grid_columnconfigure(i, weight=0, minsize=0)

        colors = self.master.colors
        now = datetime.now()

        # 1. Calculăm începutul săptămânii AFIȘATE în grid
        start_of_displayed_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())

        start_of_current_real_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0)

        num_rows = 5
        if self.master.rows_var:
            num_rows = self.master.rows_var.get()

        active_days_indices = [i for i, var in enumerate(self.selected_days) if var.get()]
        if not active_days_indices:
            return

        dynamic_minsize = 160 if len(active_days_indices) > 5 else 220

        for col_idx, day_idx in enumerate(active_days_indices):
            self.table_container.grid_columnconfigure(col_idx, weight=1, minsize=dynamic_minsize)
            data_zi = start_of_displayed_week + timedelta(days=day_idx)

            # Conversie pentru compararea săptămânilor
            data_zi_dt = datetime.combine(data_zi, datetime.min.time())
            data_str = data_zi.strftime('%Y-%m-%d')
            today_str = now.strftime('%Y-%m-%d')

            # --- LOGICĂ COLORARE HEADER ---
            # Verificăm dacă săptămâna afișată este înaintea săptămânii curente
            is_past_week = data_zi_dt < start_of_current_real_week

            if is_past_week:
                # Săptămână veche: Culori neutre (gri/stins)
                header_bg = colors.get("grid_line", "#333333")
                header_fg = colors.get("sub", "#888888")
            elif data_str == today_str:
                # Azi: Culoare de accent (roșu/roz)
                header_bg = "#CD5C5C"
                header_fg = "white"
            else:
                # Săptămâna curentă sau viitoare: Culori vii (verde/albastru)
                header_bg = colors["accent"]
                header_fg = "white"

            h_frame = tk.Frame(self.table_container, bg=header_bg, pady=15)
            h_frame.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)

            tk.Label(h_frame, text=self.days_map[day_idx].upper(), font=("Segoe UI", 8, "bold"),
                     bg=header_bg, fg=header_fg).pack()
            tk.Label(h_frame, text=data_zi.strftime('%d.%m.%Y'), font=("Segoe UI", 12, "bold"),
                     bg=header_bg, fg=header_fg).pack(pady=3)
            tk.Label(h_frame, text=f"{self.calculate_daily_total(data_str)} RON", font=("Segoe UI", 9, "italic"),
                     bg=header_bg, fg=header_fg).pack()

        # --- RANDARE CELULE ---
        for row in range(1, num_rows + 1):
            self.table_container.grid_rowconfigure(row, weight=0, minsize=145)
            for col_idx, day_idx in enumerate(active_days_indices):
                data_zi = start_of_displayed_week + timedelta(days=day_idx)
                cell_id = f"{data_zi.strftime('%Y-%m-%d')}_R{row}"
                self.render_cell(row, col_idx, cell_id)

    def render_cell(self, row, col, cell_id):
        """Randare celulă cu spațiere mare și suport absenți."""
        uid = self.master.user.get_id_entity()
        raw_data = self.master.schedule_service.get_schedule_data().get(f"{uid}_{cell_id}_raw", {})
        colors = self.master.colors
        bg_color, text_color = get_dynamic_colors(cell_id, raw_data, colors)

        cell_frame = tk.Frame(self.table_container, bg=bg_color)
        cell_frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        inner_content = tk.Frame(cell_frame, bg=bg_color, cursor="hand2")
        inner_content.pack(fill="both", expand=True, padx=12, pady=12)

        for w in [cell_frame, inner_content]:
            w.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))

        if raw_data.get('group_name'):
            tk.Label(inner_content, text=raw_data.get('time', ""), font=("Segoe UI", 9, "bold"),
                     bg=bg_color, fg=text_color).pack(anchor="nw")
            tk.Label(inner_content, text=raw_data.get('group_name'), font=("Segoe UI", 11, "bold"),
                     bg=bg_color, fg=text_color).pack(anchor="nw", pady=(3, 6))

            students = self.master.student_service.get_students_by_id_list(
                self.master.group_service.get_group_students(raw_data.get('group_id')))
            absentees = raw_data.get('absentees', [])

            for s in students[:5]:
                sid = s.get_id_entity()
                is_absent = sid in absentees
                lbl_font = ("Segoe UI", 9, "overstrike") if is_absent else ("Segoe UI", 9)
                lbl_color = "#FF7675" if is_absent else text_color

                s_lbl = tk.Label(inner_content, text=f"• {s.get_first_name()} {s.get_last_name()}", font=lbl_font,
                                 bg=bg_color, fg=lbl_color, anchor="w")
                s_lbl.pack(fill="x")
                s_lbl.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))
                s_lbl.bind("<Button-3>", lambda e, cid=cell_id, stid=sid: self.master.toggle_absentee(cid, stid))

    def render_stats_panel(self, colors):
        """Widget financiar tradus."""
        uid = self.master.user.get_id_entity()
        ls = self.master.language_service
        v_max, v_act = self.calculate_weekly_stats()

        stats_frame = tk.Frame(self.parent, bg=colors["card_bg"],
                               highlightthickness=2, highlightbackground=colors["grid_line"],
                               padx=25, pady=18)
        stats_frame.place(relx=0.98, rely=0.97, anchor="se")

        # Titlu Rezumat tradus
        tk.Label(stats_frame, text=ls.get_text(uid, "stats_title"), font=("Segoe UI", 8, "bold"),
                 bg=colors["card_bg"], fg="#888").pack(anchor="e")

        tk.Frame(stats_frame, height=1, bg=colors["grid_line"]).pack(fill="x", pady=8)

        # Potențial tradus
        p_f = tk.Frame(stats_frame, bg=colors["card_bg"])
        p_f.pack(fill="x")
        tk.Label(p_f, text=ls.get_text(uid, "stats_potential"), font=("Segoe UI", 10), bg=colors["card_bg"],
                 fg="#888").pack(side="left")
        tk.Label(p_f, text=f"{v_max} RON", font=("Segoe UI", 11, "bold"), bg=colors["card_bg"],
                 fg=colors["accent"]).pack(side="right", padx=(15, 0))

        # Încasat tradus
        i_f = tk.Frame(stats_frame, bg=colors["card_bg"])
        i_f.pack(fill="x", pady=(5, 0))
        tk.Label(i_f, text=ls.get_text(uid, "stats_actual"), font=("Segoe UI", 11, "bold"), bg=colors["card_bg"],
                 fg=colors["fg"]).pack(
            side="left")
        tk.Label(i_f, text=f"{v_act} RON", font=("Segoe UI", 18, "bold"), bg=colors["card_bg"],
                 fg=colors["success"]).pack(side="right", padx=(15, 0))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def calculate_daily_total(self, date_str):
        total = 0
        uid = self.master.user.get_id_entity()
        if self.master.rows_var:
            for r in range(1, self.master.rows_var.get() + 1):
                raw = self.master.schedule_service.get_schedule_data().get(f"{uid}_{date_str}_R{r}_raw", {})
                if raw:
                    st = self.master.student_service.get_students_by_id_list(
                        self.master.group_service.get_group_students(raw.get('group_id')))
                    for s in st:
                        if s.get_id_entity() not in raw.get('absentees', []):
                            try:
                                total += float(s.get_price())
                            except Exception as e:
                                print(e)
                                continue
        return int(total)

    def calculate_weekly_stats(self):
        v_max, v_act = 0, 0
        uid = self.master.user.get_id_entity()
        now = datetime.now()
        today_str, current_time_str = now.strftime('%Y-%m-%d'), now.strftime('%H:%M')
        start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())
        if self.master.rows_var:
            for i in range(7):
                data_zi = start_of_week + timedelta(days=i)
                data_str = data_zi.strftime('%Y-%m-%d')
                for r in range(1, self.master.rows_var.get() + 1):
                    raw = self.master.schedule_service.get_schedule_data().get(f"{uid}_{data_str}_R{r}_raw", {})
                    if raw:
                        st = self.master.student_service.get_students_by_id_list(
                            self.master.group_service.get_group_students(raw.get('group_id')))
                        is_past = (data_str < today_str) or (
                                data_str == today_str and
                                current_time_str > raw.get('time', "00:00-00:00").split("-")[1])
                        for s in st:
                            p = float(s.get_price())
                            v_max += p
                            if is_past and s.get_id_entity() not in raw.get('absentees', []):
                                v_act += p
        return int(v_max), int(v_act)
