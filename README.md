# 🎓 ClassMaster - Sistem de Management Școlar

**ClassMaster** este o aplicație desktop de înaltă performanță dezvoltată în Python 3.13, special concepută pentru profesori și mentori care gestionează fluxuri complexe de studenți. Proiectul se remarcă printr-o **arhitectură N-Tier**, securitate bazată pe **criptare binară** și o interfață ultra-adaptivă.

---

## 🚀 Funcționalități Core

### 🔐 Securitate și Confidențialitate
* **Criptare AES-256**: Toate datele sensibile (studenți, grupuri, finanțe) sunt stocate în fișiere `.enc`, gestionate prin `EncryptionManager`.
* **Zero-Knowledge Hashing**: Parolele utilizatorilor sunt procesate folosind **SHA-256**, asigurând un nivel de securitate industrial.
* **Izolarea Datelor**: Fiecare cont de utilizator are propriul mediu de date criptat, prevenind accesul neautorizat între profiluri.

### 📅 Management Inteligent al Orarului
* **Diferențiere Dinamică**: Sistem vizual care marchează automat ședințele trecute (tonuri de gri), cele curente și cele viitoare.
* **Smart Presets**: Permite salvarea unor structuri de săptămâni sub formă de template-uri criptate pentru aplicare rapidă în viitor.
* **Integritate în Cascadă**: Ștergerea unui grup elimină automat toate referințele din orar și preseturi pentru a preveni erorile de tip `KeyError` sau datele orfane.

### 🎨 Personalizare și UX
* **Motor de Tematizare**: Suport pentru peste 30 de teme profesionale (ex: *Rose Pine Moon*, *Everforest*, *Oxocarbon*).
* **High-DPI Awareness**: Interfața este optimizată pentru a se scala corect pe monitoare 4K și laptopuri moderne.
* **Localizare Instantanee**: Schimbarea limbii (RO/EN) se aplică instantaneu fără repornirea aplicației prin `LanguageService`.

---

## 🏗️ Arhitectura Sistemului

Aplicația respectă principiile programării orientate pe obiecte (OOP) și este divizată în straturi pentru mentenanță maximă:



* **UI Layer (Tkinter)**: Componente modulare și decuplate (`ScheduleView`, `LoginUi`).
* **Service Layer**: Nucleul logicii de business, calcule financiare și managementul temelor.
* **Repository Layer**: Interfața cu sistemul de fișiere, gestionând scrierea/citirea criptată și persistența datelor.
* **Security & Utils**: Module dedicate pentru criptografie (AES) și funcții helper esențiale (`resource_path`).

---

## 🛠️ Stack Tehnologic

* **Limbaj**: Python 3.13
* **Criptografie**: `cryptography` (Fernet & hazmat primitives)
* **UI & Calendar**: `tkinter`, `tkcalendar` (cu suport `Babel` pentru localizare internațională)
* **Compilare & Build**: `PyInstaller` (executabil standalone) & `Inno Setup` (kit de instalare Windows oficial)

---

## 📦 Ghid de Instalare

1. Mergi la secțiunea **[Releases](https://github.com/utilizator/ClassMaster/releases)**.
2. Descarcă fișierul `Setup.exe`.
3. Rulează kit-ul de instalare.
   * *Notă: Deoarece aplicația este independentă, Windows SmartScreen poate afișa o alertă. Alege "More Info" -> "Run Anyway"*.
4. Aplicația va stoca bazele de date criptate în mod securizat în `%APPDATA%/ClassMaster/data`, protejându-le împotriva ștergerii accidentale la dezinstalare.

---

## 🔧 Informații pentru Dezvoltatori (Build din sursă)

Dacă dorești să modifici codul și să generezi un nou executabil:

### Instalare dependințe
```bash
pip install cryptography tkcalendar babel pillow

## 📂 Structura Proiectului

ClassMaster/
├── Internal/
│   ├── entity/         # Modele de date (User, Student, Group, Preset)
│   ├── repository/     # Logica de persistență și I/O criptat
│   ├── service/        # Business logic, orar și servicii de sistem
│   ├── ui/             # Modulele interfeței grafice și componentele custom
│   ├── security/       # Nucleul de criptare (EncryptionManager)
│   └── utils/          # Funcții utilitare (resource_path, color management)
├── main.py             # MainController și punctul de intrare (Entry Point)
└── ClassMaster.spec    # Configurația de build avansată pentru PyInstaller
