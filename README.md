# Real Estate Manager 🏡

A desktop application built with **Python** and **PyQt5** to manage real estate property listings, with full CRUD operations and image support, was created for the CECS 3210 course from PUPR and was presented as a demo.

---

## ✨ Features

- 📋 View full list of properties in a dynamic table
- ➕ Add new houses with address, size, and photo
- 🛠 Modify existing listings by ID
- 🔎 Search houses by ID (with photo preview)
- ❌ Remove listings after confirmation
- 📊 MySQL backend for persistent storage
- 💡 Clean UI with `.ui` files (Qt Designer)
- 🔐 Secure DB credentials using `.env` file

---

## 📁 Project Structure

```
Real-Estate-Manager-main/
│
├── main.py                     # Entry point
├── RealStateDB.sql             # MySQL database schema
├── .env.example                # Sample environment config
│
├── BackendSection/             # App logic
│   ├── DBConnection.py         # MySQL DB connector
│   ├── AddHouse.py             # Add functionality
│   ├── ModifyHouse.py          # Modify functionality
│   ├── ViewHouse.py            # View functionality
│   └── ...
│
├── UiFolder/                   # Qt .ui design files
│   └── MainWindow.ui, AddHouse.ui, etc.
│
├── icons/                      # App icons
├── photos/                     # Sample house photos
└── README.md                   # This file
```

---

### 🔧 Prerequisites

- Python 3.11 or later
- MySQL running locally
- `pip install -r requirements.txt` (see below)

### 🔑 The `.env` file

```env
DB_HOST=localhost
DB_USER=root
DB_PASS=yourpassword <-- This is replaced with the password 
DB_NAME=RealStateDB
```

### 💽 Create the database

```sql
-- In MySQL
SOURCE RealStateDB.sql;
```

### 🚀 Run the App

```bash
python main.py
```

---

## 📦 Dependencies

```bash
pip install PyQt5 pymysql python-dotenv
```

---

## 📸 Screenshots

### 🏠 Main Window
![Main Window](screenshots/mainwindow.png)

### ➕ Add House
![Add House](screenshots/addhouse.png)

### 📝 Modify House
![Modify House](screenshots/modifyhouse.png)

### 🔍 Search House
![Search House](screenshots/searchhouse.png)

### ❌ Remove House
![Remove House](screenshots/removehouse.png)

### 📋 Report Window
![Report](screenshots/report.png)

### ❓ Help Window
![Help](screenshots/Help.png)

---

## 💡 Notes

- `.env` is git-ignored for security
- Images are displayed using relative paths in-app
- Built for academic use