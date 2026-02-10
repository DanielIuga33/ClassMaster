import tkinter as tk
from tkinter import messagebox, filedialog
from Internal.entity.User import User

from Internal.service.UserService import UserService


class RegisterUi:
    def __init__(self, root, user_service: UserService, on_back, settings_service):
        self.root = root
        self.user_service = user_service
        self.on_back = on_back
        self.settings_service = settings_service

        # Tema culori
        self.theme = self.get_theme_colors()
        self.root.title("Înregistrare - ClassMaster")

        # AJUSTARE: Dimensiune fereastră și centrare
        # Am setat o înălțime de 750 (în loc de 850) pentru a fi mai sigură pe laptopuri
        self.setup_window(600, 750)
        self.root.configure(bg=self.theme["bg"])

        # Container principal - folosim place pentru centrare conținut dacă vrei,
        # dar pack este mai sigur pentru formulare lungi cu scroll
        self.container = tk.Frame(self.root, bg=self.theme["bg"])
        self.container.pack(expand=True, fill="both", padx=50, pady=20)

        # Titlu (Am redus pady-ul ca să "urcăm" formularul)
        tk.Label(self.container, text="Creează un cont nou", font=("Segoe UI", 20, "bold"),
                 bg=self.theme["bg"], fg=self.theme["fg"]).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Stiluri Entry
        self.lbl_style = {"bg": self.theme["bg"], "fg": self.theme["fg"], "font": ("Segoe UI", 9, "bold")}
        self.ent_style = {"font": ("Segoe UI", 11), "relief": "flat", "bg": self.theme["ent_bg"],
                          "fg": self.theme["fg"], "insertbackground": self.theme["fg"]}

        # 1. Date Identitate
        self.add_field("Nume", "entry_ln", 1, 0)
        self.add_field("Prenume", "entry_fn", 1, 1)
        self.add_field("Username", "entry_uname", 2, 0)
        self.add_field("Email", "entry_email", 2, 1)

        # 2. Securitate
        self.add_field("Parolă", "entry_pass", 3, 0, show="*")
        self.add_field("Confirmă Parola", "entry_confirm_pass", 3, 1, show="*")

        # 3. Adresă
        self.add_field("Adresă (Stradă)", "entry_street", 4, 0, columnspan=2)
        self.add_field("Oraș", "entry_city", 5, 0)
        self.add_field("Județ/Stat", "entry_state", 5, 1)
        self.add_field("Data Nașterii", "entry_birth", 6, 0, columnspan=2)

        # 4. Stocare
        tk.Label(self.container, text="Locație stocare date", **self.lbl_style).grid(row=14, column=0, sticky="w",
                                                                                     pady=(10, 0))
        path_frame = tk.Frame(self.container, bg=self.theme["bg"])
        path_frame.grid(row=15, column=0, columnspan=2, sticky="ew")

        self.entry_path = tk.Entry(path_frame, **self.ent_style)
        self.entry_path.pack(side="left", expand=True, fill="x", ipady=4)

        tk.Button(path_frame, text="Răsfoiește", command=self.browse_folder, bg="#4A90E2", fg="white",
                  relief="flat", cursor="hand2").pack(side="right", padx=(5, 0))

        # Buton Final
        tk.Button(self.container, text="Finalizează Înregistrarea", command=self.handle_register,
                  font=("Segoe UI", 12, "bold"), bg="#2ECC71", fg="white", relief="flat", pady=10).grid(row=16,
                                                                                                        column=0,
                                                                                                        columnspan=2,
                                                                                                        sticky="ew",
                                                                                                        pady=(25, 10))

        tk.Button(self.container, text="Înapoi", command=on_back, bg=self.theme["bg"], fg="#888", relief="flat",
                  cursor="hand2").grid(
            row=17, column=0, columnspan=2)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

    def setup_window(self, w, h):
        # Calculare pentru centrare reală
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        # Am scăzut 50 pixeli din Y pentru a ridica fereastra mai sus de bara de start
        y = (hs / 2) - (h / 2) - 50

        if y < 0: y = 10  # Siguranță să nu iasă din ecran sus
        self.root.geometry(f'{int(w)}x{int(h)}+{int(x)}+{int(y)}')

    def add_field(self, label_text, attr_name, row, col, columnspan=1, show=None):
        r = row * 2
        tk.Label(self.container, text=label_text, **self.lbl_style).grid(row=r, column=col, columnspan=columnspan,
                                                                         sticky="w", pady=(10, 2))
        entry = tk.Entry(self.container, show=show, **self.ent_style)
        entry.grid(row=r + 1, column=col, columnspan=columnspan, sticky="ew",
                   padx=(0, 10 if col == 0 and columnspan == 1 else 0), ipady=5)
        setattr(self, attr_name, entry)

    def get_theme_colors(self):
        if self.settings_service.get_theme() == "dark":
            return {"bg": "#121212", "fg": "#FFFFFF", "ent_bg": "#1E1E1E"}
        return {"bg": "#F8F9FA", "fg": "#2D3436", "ent_bg": "#FFFFFF"}

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, folder)

    def handle_register(self):
        # 1. Extragerea datelor (Fără def handle_register(self) aici!)
        username = self.entry_uname.get().strip()
        first_name = self.entry_fn.get()
        last_name = self.entry_ln.get()
        email = self.entry_email.get()
        password = self.entry_pass.get()
        confirm_pass = self.entry_confirm_pass.get()
        street = self.entry_street.get()
        city = self.entry_city.get()
        state = self.entry_state.get()
        birthday = self.entry_birth.get()
        data_path = self.entry_path.get()

        # 2. Validări
        if password != confirm_pass:
            messagebox.showerror("Eroare", "Parolele nu coincid!")
            return

        fields = [username, first_name, last_name, email, password, street, city, state, birthday, data_path]
        if not all(fields):
            messagebox.showwarning("Atenție", "Toate câmpurile sunt obligatorii!")
            return

        # 3. Crearea obiectului și trimiterea la Service
        try:
            new_user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                data_path=data_path,
                street_address=street,
                city=city,
                state=state,
                birthday=birthday
            )

            result = self.user_service.add_user(new_user)

            if result and result[0] == 201:
                messagebox.showinfo("Succes", "Cont creat! Te poți loga.")
                self.on_back()
            else:
                msg = result[1] if result else "Eroare necunoscută"
                messagebox.showerror("Eroare", f"Nu s-a putut crea contul: {msg}")

        except Exception as e:
            messagebox.showerror("Eroare Critică", f"A apărut o problemă: {str(e)}")