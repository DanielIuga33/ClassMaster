import tkinter as tk
from tkinter import messagebox, ttk

class ScheduleEditUi(tk.Toplevel):
    def __init__(self, parent, theme, cell_id, day, current_data, on_save, on_delete, group_service, user_id, lang_service):
        super().__init__(parent)
        self.theme = theme
        self.on_save = on_save
        self.on_delete = on_delete
        self.cell_id = cell_id
        self.group_service = group_service
        self.user_id = user_id
        self.lang_service = lang_service # Serviciul de limbă injectat

        uid = self.user_id
        ls = self.lang_service
        self.txt_color = theme.get("schedule_text", theme["fg"])

        # Titlu fereastră tradus dinamic
        self.title(f"{ls.get_text(uid, 'sched_edit_title')} - {day}")
        self.setup_modal(400, 450)
        self.configure(bg=theme["bg"], padx=25, pady=25)
        self.grab_set()

        # Titlu modal tradus
        tk.Label(self, text=f"{ls.get_text(uid, 'sched_edit_header')}: {day}", font=("Segoe UI", 16, "bold"),
                 bg=theme["bg"], fg=theme["accent"]).pack(pady=(0, 20))

        # --- SELECȚIE GRUPĂ ---
        tk.Label(self, text=ls.get_text(uid, "sched_edit_choose_group"), bg=theme["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        self.available_groups = self.group_service.get_groups_for_teacher(self.user_id)
        group_names = [g.get_group_name() for g in self.available_groups]

        self.group_combo = ttk.Combobox(self, values=group_names, font=("Segoe UI", 11), state="readonly")
        self.group_combo.pack(fill="x", pady=(5, 15), ipady=5)

        if current_data and "group_name" in current_data:
            self.group_combo.set(current_data["group_name"])

        # --- INTERVAL ORAR ---
        tk.Label(self, text=ls.get_text(uid, "sched_edit_time_range"), bg=theme["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0))

        time_container = tk.Frame(self, bg=theme["bg"])
        time_container.pack(fill="x", pady=5)

        entry_bg = theme["input_bg"]

        # Start Time
        self.start_hh = self.create_time_entry(time_container, entry_bg, 23)
        tk.Label(time_container, text=":", bg=theme["bg"], fg=self.txt_color, font=("bold")).pack(side="left")
        self.start_mm = self.create_time_entry(time_container, entry_bg, 59)

        # "până la" tradus
        tk.Label(time_container, text=f"  {ls.get_text(uid, 'sched_edit_until')}  ", bg=theme["bg"], fg=self.txt_color,
                 font=("Segoe UI", 9, "italic")).pack(side="left", padx=5)

        # End Time
        self.end_hh = self.create_time_entry(time_container, entry_bg, 23)
        tk.Label(time_container, text=":", bg=theme["bg"], fg=self.txt_color, font=("bold")).pack(side="left")
        self.end_mm = self.create_time_entry(time_container, entry_bg, 59)

        if current_data and "time" in current_data:
            self.parse_and_fill_time(current_data["time"])

        # --- BUTOANE ---
        # Confirmare programare tradusă
        tk.Button(self, text=ls.get_text(uid, "sched_edit_btn_confirm"), command=self.handle_save,
                  bg=theme.get("success", "#2ECC71"),
                  fg="white", font=("Segoe UI", 11, "bold"), relief="flat", pady=12, cursor="hand2").pack(fill="x",
                                                                                                          pady=(30, 5))

        if current_data:
            # Eliminare tradusă
            tk.Button(self, text=ls.get_text(uid, "sched_edit_btn_remove"), command=lambda: [self.on_delete(self.cell_id), self.destroy()],
                      bg=theme.get("danger", "#E74C3C"), fg="white", font=("Segoe UI", 10),
                      relief="flat", pady=8, cursor="hand2").pack(fill="x")

    def create_time_entry(self, parent, bg, limit):
        vcmd = (self.register(self.validate_time), '%P', limit)
        ent = tk.Entry(parent, width=3, font=("Segoe UI", 12, "bold"), justify="center",
                       relief="flat", bg=bg, fg=self.txt_color,
                       insertbackground=self.txt_color, validate='key', validatecommand=vcmd)
        ent.pack(side="left", padx=2, ipady=4)
        ent.bind("<KeyRelease>", lambda e: self.auto_focus(e.widget))
        return ent

    def validate_time(self, P, limit):
        if P == "": return True
        if P.isdigit() and len(P) <= 2:
            if int(P) <= int(limit):
                return True
        return False

    def auto_focus(self, widget):
        if len(widget.get()) == 2:
            widget.tk_focusNext().focus()

    def parse_and_fill_time(self, time_str):
        try:
            start, end = time_str.split('-')
            sh, sm = start.split(':')
            eh, em = end.split(':')
            self.start_hh.insert(0, sh)
            self.start_mm.insert(0, sm)
            self.end_hh.insert(0, eh)
            self.end_mm.insert(0, em)
        except:
            pass

    def setup_modal(self, w, h):
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws / 2) - (w / 2), (hs / 2) - (h / 2)
        self.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

    def handle_save(self):
        uid = self.user_id
        ls = self.lang_service
        selected_group_name = self.group_combo.get()
        sh, sm = self.start_hh.get().strip(), self.start_mm.get().strip()
        eh, em = self.end_hh.get().strip(), self.end_mm.get().strip()

        if not selected_group_name or not all([sh, sm, eh, em]):
            # Avertisment tradus
            messagebox.showwarning(ls.get_text(uid, "warning"), ls.get_text(uid, "sched_edit_err_fields"))
            return

        time_formatted = f"{sh.zfill(2)}:{sm.zfill(2)}-{eh.zfill(2)}:{em.zfill(2)}"
        selected_group = next((g for g in self.available_groups if g.get_group_name() == selected_group_name), None)

        data = {
            "group_name": selected_group_name,
            "time": time_formatted,
            "group_id": selected_group.get_id_entity() if selected_group else "",
            "teacher_id": self.user_id,
            "absentees": []
        }

        self.on_save(self.cell_id, data)
        self.destroy()