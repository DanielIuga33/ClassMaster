import tkinter as tk
from Internal.ui.StudentEditUi import StudentEditUi


class StudentsView:
    def __init__(self, parent_frame, controller):
        self.parent = parent_frame
        self.master = controller

    def render(self, sort_by="grade"):
        """Randare cu suport multilingv și sortare interactivă."""
        self.master.clear_content()
        user_id = self.master.user.get_id_entity()
        ls = self.master.language_service  # Serviciul de limbă
        colors = self.master.settings_service.get_colors(user_id)
        txt_color = colors.get("schedule_text", colors["fg"])

        # 1. Header principal tradus
        header_frame = tk.Frame(self.parent, bg=colors["bg"])
        header_frame.pack(fill="x", pady=(0, 25))

        tk.Label(header_frame, text=f"👥 {ls.get_text(user_id, 'menu_students')}", font=("Segoe UI", 26, "bold"),
                 bg=colors["bg"], fg=colors["fg"]).pack(side="left")

        tk.Button(header_frame, text=ls.get_text(user_id, 'btn_add_student'),
                  command=self.master.open_add_student_modal,
                  bg=colors.get("success", "#2ECC71"), fg="white", font=("Segoe UI", 11, "bold"),
                  relief="flat", padx=25, pady=12, cursor="hand2").pack(side="right")

        # 2. Container Scrollbar
        canvas_container = tk.Frame(self.parent, bg=colors["bg"])
        canvas_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_container, bg=colors["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        table_inner = tk.Frame(canvas, bg=colors["bg"])

        canvas_window = canvas.create_window((0, 0), window=table_inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

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

        # --- Header Tabel Tradus cu Sortare ---
        header_table = tk.Frame(table_inner, bg=colors["input_bg"])
        header_table.pack(fill="x")

        # Configurație butoane header traduse
        headers_config = [
            (ls.get_text(user_id, "col_name_lastname"), "name"),
            (ls.get_text(user_id, "reg_city").replace(":", ""), "grade"),  # Reutilizăm etichete dacă e posibil
            (ls.get_text(user_id, "col_price_h"), "price"),
            (ls.get_text(user_id, "col_actions"), None)
        ]

        # Corecție manuală pentru "Clasă" dacă nu vrei să reutilizezi orașul
        headers_config[1] = (ls.get_text(user_id, "col_grade"), "grade")

        for text, sort_key in headers_config:
            if sort_key:
                btn = tk.Button(header_table, text=text.upper(), font=("Segoe UI", 10, "bold"),
                                bg=colors["input_bg"], fg=txt_color, relief="flat",
                                activebackground=colors["accent"], cursor="hand2",
                                command=lambda k=sort_key: self.render(k))
                btn.pack(side="left", fill="x", expand=True, ipady=15)
            else:
                tk.Label(header_table, text=text.upper(), font=("Segoe UI", 10, "bold"),
                         bg=colors["input_bg"], fg=txt_color, pady=18, width=20).pack(side="left", fill="x",
                                                                                      expand=True)

        # 3. Populare rânduri
        students = self.master.student_service.get_sorted_students(user_id, sort_by)

        for idx, s in enumerate(students):
            bg_row = colors["card_bg"] if idx % 2 == 0 else colors["input_bg"]
            row_frame = tk.Frame(table_inner, bg=bg_row)
            row_frame.pack(fill="x")

            student_grade = s.get_grade()

            tk.Label(row_frame, text=f"  {s.get_last_name()} {s.get_first_name()}",
                     font=("Segoe UI", 11), bg=bg_row, fg=txt_color,
                     pady=15, width=40, anchor="w").pack(side="left", fill="x", expand=True)

            tk.Label(row_frame, text=student_grade, font=("Segoe UI", 11),
                     bg=bg_row, fg=txt_color, width=15).pack(side="left", fill="x", expand=True)

            tk.Label(row_frame, text=f"{s.get_price()} RON", font=("Segoe UI", 11, "bold"),
                     bg=bg_row, fg=colors.get("success", "#27AE60"),
                     width=20).pack(side="left", fill="x", expand=True)

            act_f = tk.Frame(row_frame, bg=bg_row, width=20)
            act_f.pack(side="left", fill="x", expand=True)
            btns = tk.Frame(act_f, bg=bg_row)
            btns.pack(expand=True)

            tk.Button(btns, text=" ✏️ ", bg="#F1C40F", fg="black", relief="flat",
                      command=lambda st=s: self.open_edit_modal(st),
                      cursor="hand2", padx=8).pack(side="left", padx=5)

            tk.Button(btns, text=" 🗑️ ", bg="#E74C3C", fg="white", relief="flat",
                      command=lambda st=s: self.confirm_delete(st),
                      cursor="hand2", padx=8).pack(side="left", padx=5)

    def open_edit_modal(self, student):
        StudentEditUi(self.parent, self.master.colors, student,
                      self.master.student_service, self.master.show_students)

    def confirm_delete(self, student):
        user_id = self.master.user.get_id_entity()
        ls = self.master.language_service
        self.master.student_service.delete_student(student)

        # Mesaj ștergere tradus dinamic
        msg = ls.get_text(user_id, "msg_student_deleted").replace("{name}", student.get_last_name())
        self.master.show_toast(f"🗑️ {msg}", "#34495E")
        self.render()