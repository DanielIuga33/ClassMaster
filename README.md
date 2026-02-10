# 🎓 ClassMaster - Sistem de Management Școlar

**ClassMaster** este o aplicație desktop modernă dezvoltată în Python, concepută pentru a eficientiza gestionarea datelor școlare (studenți, cursuri, note). Proiectul pune un accent deosebit pe **securitate**, **arhitectură curată** și **experiența utilizatorului**.

---

## 🚀 Funcționalități Principale

* **Sistem de Autentificare Hibrid**: Permite logarea securizată folosind fie `Username`, fie `Email`.
* **Securitate Avansată**: Parolele sunt protejate folosind algoritmul de hashing **SHA-256** prin librăria `hashlib`.
* **Managementul Datelor (JSON)**: Persistența datelor este realizată în format JSON, oferind portabilitate și viteză.
* **Stocare Dinamică**: Utilizatorul are posibilitatea de a alege locația bazei de date (ex: pe un stick USB sau folder de cloud).
* **Interfață Adaptivă**: Suport complet pentru **Dark Mode** și **Light Mode**, cu scalare automată pentru monitor (DPI Awareness).
* **Arhitectură Layered (N-Tier)**: Proiectul este structurat pentru a asigura separarea responsabilităților:
    * **UI Layer**: Interfață grafică realizată cu Tkinter.
    * **Service Layer**: Logica de business, validări și criptare.
    * **Repository Layer**: Gestionarea operațiunilor de citire/scriere (I/O).
    * **Entity Layer**: Definirea modelelor de date.



---

## 🛠️ Tehnologii Utilizate

* **Limbaj**: Python 3.12+
* **Interfață**: Tkinter
* **Format Date**: JSON
* **Securitate**: SHA-256 Hashing
* **OS Awareness**: `ctypes` pentru scalare High-DPI în Windows.

---

## 📦 Instalare și Rulare

1.  **Clonarea depozitului**:
    ```bash
    git clone [https://github.com/utilizator/ClassMaster.git](https://github.com/utilizator/ClassMaster.git)
    cd ClassMaster
    ```

2.  **Lansarea aplicației**:
    ```bash
    python main.py
    ```

---

## 📂 Structura Proiectului

```text
ClassMaster/
├── Data/               # Locația implicită pentru baze de date (Users.json)
├── Internal/           # Nucleul aplicației
│   ├── entity/         # Modelele (User.py, Student.py)
│   ├── repository/     # Logica de salvare/încărcare date
│   ├── service/        # Logica de business (UserService.py)
│   └── ui/             # Modulele de interfață (LoginUi.py, RegisterUi.py)
├── main.py             # Punctul de intrare (MainController)
└── settings.txt        # Configurațiile utilizatorului (tema, ultima locație date)