import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from Internal.ui.ScheduleEditUi import ScheduleEditUi


class ScheduleView:
    def __init__(self, parent_frame, controller):
        """
        :param parent_frame: Frame-ul principal (main_content) din UserUi unde se va desena orarul.
        :param controller: Referință către instanța UserUi pentru a accesa datele comune (user, servicii).
        """
        self.parent = parent_frame
        self.master = controller  # Referință la UserUi

        # UI Elements pe care le vom manipula
        self.table_container = None
        self.canvas = None
        self.cal_select = None

    def render(self):
        """Metoda principală care desenează interfața orarului."""
        self.master.colors = self.master.settings_service.get_colors()

        header_frame = tk.Frame(self.parent, bg=self.master.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))

        # --- Navigare și Calendar ---
        nav_frame = tk.Frame(header_frame, bg=self.master.colors["bg"])
        nav_frame.pack(side="left")

        tk.Button(nav_frame, text="◀", command=self.master.prev_week,
                  bg=self.master.colors["accent"], fg="white", relief="flat").pack(side="left", padx=5)

        self.cal_select = DateEntry(nav_frame, width=20, background=self.master.colors["accent"],
                                    foreground='white', borderwidth=2, font=("Segoe UI", 12, "bold"),
                                    date_pattern='dd/mm/yyyy', locale='ro_RO')
        self.cal_select.set_date(self.master.current_date)
        self.cal_select.pack(side="left", padx=10)
        self.cal_select.bind("<<DateEntrySelected>>", self.master.on_date_selected)

        tk.Button(nav_frame, text="▶", command=self.master.next_week,
                  bg=self.master.colors["accent"], fg="white", relief="flat").pack(side="left", padx=5)

        # --- Butoane Preset ---
        tk.Button(nav_frame, text="💾 Salvează Preset", command=self.master.save_as_preset,
                  bg="#27AE60", fg="white", relief="flat", font=("Segoe UI", 9, "bold"),
                  padx=10).pack(side="left", padx=(25, 5))

        tk.Button(nav_frame, text="📋 Aplică Preset", command=self.master.open_presets_manager,
                  bg="#8E44AD", fg="white", relief="flat", font=("Segoe UI", 9, "bold"),
                  padx=10).pack(side="left", padx=5)

        # --- Control Rânduri ---
        rows_control = tk.Frame(header_frame, bg=self.master.colors["bg"])
        rows_control.pack(side="right")
        tk.Spinbox(rows_control, from_=2, to=20, textvariable=self.master.rows_var, width=5,
                   command=self.master.update_rows_count, bg=self.master.colors["input_bg"],
                   fg=self.master.colors["fg"]).pack(side="right", padx=10)

        # --- Container Tabel (Scrollable) ---
        canvas_container = tk.Frame(self.parent, bg=self.master.colors["bg"])
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg=self.master.colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)

        self.table_container = tk.Frame(self.canvas, bg=self.master.colors["bg"])
        self.canvas.create_window((0, 0), window=self.table_container, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.table_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.draw_grid()

    def draw_grid(self):
        """Logica de desenare a celulelor."""
        for widget in self.table_container.winfo_children():
            widget.destroy()

        start_of_week = self.master.current_date - timedelta(days=self.master.current_date.weekday())
        zile_nume = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă"]
        num_rows = self.master.rows_var.get()

        for i, nume in enumerate(zile_nume):
            data_zi = start_of_week + timedelta(days=i)
            text_header = f"{nume}\n{data_zi.strftime('%d.%m')}"
            self.table_container.grid_columnconfigure(i, weight=1, minsize=180)
            tk.Label(self.table_container, text=text_header, font=("Segoe UI", 10, "bold"),
                     bg="#4A90E2", fg="white", pady=10).grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        for row in range(1, num_rows + 1):
            self.table_container.grid_rowconfigure(row, weight=0, minsize=120)
            for col in range(len(zile_nume)):
                data_zi = start_of_week + timedelta(days=col)
                cell_id = f"{data_zi.strftime('%Y-%m-%d')}_R{row}"
                self.render_cell(row, col, cell_id)

    def render_cell(self, row, col, cell_id):
        """Randarea unei celule individuale."""
        unique_key = f"{self.master.user.get_id_entity()}_{cell_id}"
        raw_data = self.master.schedule_data.get(f"{unique_key}_raw", {})

        group_name = raw_data.get('group_name', "")
        time_val = raw_data.get('time', "")

        bg_color = self.master.colors["card_bg"]
        if group_name:
            bg_color = "#1B2631" if self.master.settings_service.get_theme() == "dark" else "#EBF5FB"

        cell_frame = tk.Frame(self.table_container, bg=bg_color, highlightthickness=1,
                              highlightbackground=self.master.colors["grid_line"])
        cell_frame.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        time_lbl = tk.Label(cell_frame, text=time_val, font=("Segoe UI", 9, "bold"),
                            bg=bg_color, fg=self.master.colors["fg"], width=10, anchor="center")
        time_lbl.pack(side="left", fill="y", padx=(5, 0))

        if group_name:
            tk.Frame(cell_frame, width=1, bg=self.master.colors["grid_line"]).pack(side="left", fill="y", padx=5)
            details = tk.Frame(cell_frame, bg=bg_color)
            details.pack(side="left", fill="both", expand=True, padx=5, pady=10)

            tk.Label(details, text=group_name, font=("Segoe UI", 11, "bold"),
                     bg=bg_color, fg=self.master.colors["fg"], anchor="nw").pack(fill="x")

            students_text = self.master.get_formatted_students(raw_data)
            tk.Label(details, text=students_text, font=("Segoe UI", 9),
                     bg=bg_color, fg=self.master.colors["fg"], justify="left",
                     anchor="nw", wraplength=150).pack(fill="both", expand=True)

        for widget in [cell_frame, time_lbl]:
            widget.bind("<Button-1>", lambda e, cid=cell_id: self.master.open_group_assignment_modal(cid))