# 🎓 ClassMaster - Sistem de Management Școlar 

**ClassMaster** este o aplicație desktop avansată dezvoltată în Python, concepută pentru profesori și mentori. Proiectul pune un accent critic pe **securitatea datelor prin criptare**, o **arhitectură robustă N-Tier** și o **interfață ultra-personalizabilă**.

---

## 🚀 Funcționalități Noi și Îmbunătățite

* **Securitate Militarizată (AES-256)**: Datele despre studenți, grupuri și orar sunt criptate folosind algoritmul AES prin `EncryptionManager`, fiind accesibile doar cu parola utilizatorului.
* **Orar Interactiv și Inteligent**: 
    * Diferențiere vizuală dinamică între ședințele trecute, cele în desfășurare și cele care urmează astăzi.
    * Logica de "Domeniul Trecutului" pentru vizualizarea săptămânilor anterioare în tonuri de gri.
* **Sistem de Presetări (Templates)**: Salvarea structurilor de orar sub formă de preseturi criptate și aplicarea lor rapidă pe săptămâni viitoare.
* **Ștergere în Cascadă (Data Integrity)**: Eliminarea unui grup curăță automat toate referințele din orarul activ și din toate preseturile salvate pentru a preveni erorile de tip `KeyError`.
* **Motor de Tematizare Avansat**: Peste 30 de teme incluse (ex: *Rose Pine Moon*, *Everforest*, *Oxocarbon*), cu suport pentru personalizarea culorilor la nivel de celulă.
* **Suport Multilingv Dinamic**: Interfața se adaptează instantaneu la limba aleasă (RO/EN) prin `LanguageService`.

---

## 🏗️ Arhitectura Sistemului



Proiectul este structurat pe straturi pentru a asigura o mentenanță ușoară:
* **UI Layer (Tkinter)**: Componente modulare (`ScheduleView`, `GroupsView`) care gestionează interacțiunea cu utilizatorul.
* **Service Layer**: Gestionează logica de business, calculele financiare și sincronizarea datelor.
* **Repository Layer**: Gestionează persistența fișierelor `.enc` și operațiunile I/O criptate.
* **Security & Utils**: Module dedicate pentru criptare (AES), hashing (SHA-256) și funcții helper.

---

## 🛠️ Tehnologii și Biblioteci

* **Limbaj**: Python 3.12+
* **Criptare**: `cryptography` (Fernet/AES-128/256)
* **Interfață**: `tkinter` cu suport High-DPI Awareness.
* **Componente**: `tkcalendar`, `customtkinter` (opțional pentru elemente moderne).

---

## 📂 Structura Proiectului

```text
ClassMaster/
├── Internal/
│   ├── entity/         # Modele de date (User, Student, Group, Preset)
│   ├── repository/     # Gestionarea fișierelor criptate .enc
│   ├── service/        # Logica de business (StudentService, ScheduleService)
│   ├── ui/             # Modulele de interfață grafică (ScheduleView, etc.)
│   ├── security/       # Nucleul de criptare: EncryptionManager.py
│   └── utils/          # Funcții utilitare globale: utils.py
├── main.py             # MainController și punctul de intrare în aplicație
└── settings.txt        # Configurațiile persistente ale utilizatorului
