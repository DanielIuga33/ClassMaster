import tkinter as tk

from Internal.entity.Group import Group
from Internal.ui.GroupEditUi import GroupEditUi

class GroupsView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller
        self.user_id = self.master.user.get_id_entity()
        self.colors = self.master.settings_service.get_colors(self.user_id)

    def render(self):
        """Randarea tabelului de gestionare grupe cu scroll și control prin mouse."""
        self.master.clear_content()
        colors = self.master.settings_service.get_colors(self.user_id)
        txt_color = colors.get("schedule_text", colors["fg"])

        # 1. Header principal
        header_frame = tk.Frame(self.parent, bg=colors["bg"])
        header_frame.pack(fill="x", pady=(0, 25))

        tk.Label(header_frame, text="🏫 Gestiune Grupe", font=("Segoe UI", 26, "bold"),
                 bg=colors["bg"], fg=colors["fg"]).pack(side="left")

        tk.Button(header_frame, text="+ Grupă Nouă", command=self.master.open_add_group_modal,
                  bg="#9B59B6", fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=25, pady=12, cursor="hand2").pack(side="right")

        # 2. Container Scrollbar (Canvas + Frame)
        canvas_container = tk.Frame(self.parent, bg=colors["bg"])
        canvas_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_container, bg=colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)

        # Frame-ul interior pentru conținut
        table_inner = tk.Frame(canvas, bg=colors["bg"])
        canvas_window = canvas.create_window((0, 0), window=table_inner, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # --- LOGICĂ SCROLL SIGURĂ ---
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))
        canvas.bind("<Destroy>", lambda _: canvas.unbind_all("<MouseWheel>"))

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())

        table_inner.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # --- Header Tabel ---
        header_table = tk.Frame(table_inner, bg=colors["input_bg"])
        header_table.pack(fill="x")

        headers = ["Nume Grupă", "Membri & Tarife", "Total / Ședință", "Acțiuni"]
        widths = [25, 40, 15, 20]  # Distribuție lățime coloane

        for i, h in enumerate(headers):
            tk.Label(header_table, text=h.upper(), font=("Segoe UI", 10, "bold"),
                     bg=colors["input_bg"], fg=txt_color, pady=18, width=widths[i]).pack(side="left", fill="x",
                                                                                         expand=True)

        # 3. Populare rânduri
        groups = sorted(self.master.group_service.get_groups_for_teacher(self.user_id),
                        key=lambda group: group.get_group_name())

        for idx, g in enumerate(groups):
            bg_row = colors["card_bg"] if idx % 2 == 0 else colors["input_bg"]
            row_frame = tk.Frame(table_inner, bg=bg_row)
            row_frame.pack(fill="x")

            # Nume Grupă
            tk.Label(row_frame, text=g.get_group_name(), font=("Segoe UI", 11, "bold"),
                     bg=bg_row, fg=txt_color, pady=20, width=widths[0]).pack(side="left", fill="x", expand=True)

            # Membri & Tarife
            members_info = ""
            total_p = 0
            for s_id in g.get_student_ids():
                s = self.master.student_service.get_student_by_id(s_id)
                if s:
                    members_info += f"• {s.get_last_name()} {s.get_first_name()} ({s.get_price()} RON)\n"
                    total_p += s.get_price()

            tk.Label(row_frame, text=members_info.strip(), font=("Segoe UI", 10),
                     bg=bg_row, fg=txt_color, width=widths[1], justify="left").pack(side="left", fill="x", expand=True)

            # Total / Ședință
            tk.Label(row_frame, text=f"{total_p} RON", font=("Segoe UI", 11, "bold"),
                     bg=bg_row, fg="#27AE60", width=widths[2]).pack(side="left", fill="x", expand=True)

            # Acțiuni
            act_f = tk.Frame(row_frame, bg=bg_row, width=widths[3])
            act_f.pack(side="left", fill="x", expand=True)
            btns = tk.Frame(act_f, bg=bg_row)
            btns.pack(expand=True)

            tk.Button(btns, text=" ✏️ ", bg="#F1C40F", relief="flat", cursor="hand2",
                      command=lambda gr=g: self.open_edit_group_modal(gr)).pack(side="left", padx=5)
            tk.Button(btns, text=" 🗑️ ", bg="#E74C3C", fg="white", relief="flat", cursor="hand2",
                      command=lambda gr=g: self.master.handle_delete_group(gr)).pack(side="left", padx=5)

    def open_edit_group_modal(self, group):
        GroupEditUi(self.master.root, self.colors, group, self.master.group_service,
                    self.master.student_service, self.master.show_groups)
