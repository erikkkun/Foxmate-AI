# 🦊 FoxMate AI — Desktop Focus Assistant

FoxMate AI is an interactive productivity companion that tracks user activity, analyzes focus levels using a trained ML regressor, and visualizes daily reports through a floating "fox pet" desktop UI.

---

## 🚀 Features

- 🧠 **Real-time focus prediction** using `SentenceTransformer` + regression model  
- 🦊 **Animated floating fox assistant** (PySide6 GUI)  
- 📊 **Weekly and session reports** (Tkinter + Matplotlib charts)  
- 💾 **Local logging** of user activity and focus scores  
- 🧩 **Modular structure** for frontend / backend separation
- 📦 **Single executable** distribution (PyInstaller)

---

## 👥 For End Users (Download & Run)

### Quick Start (No Installation Required!)

1. **Download the Application**
   - Go to the [Releases](../../releases) page on GitHub
   - Download the latest `FoxMate AI v1.0.zip` file
   - Extract the ZIP file to any folder on your computer

2. **Run the Application**
   - Open the extracted folder
   - Double-click `FoxMate AI.exe`
   - The application will start automatically

3. **Start Using**
   - Click the **"Fox it!"** button on the home page
   - A floating fox pet window will appear
   - The fox monitors your activity and shows your focus level

### System Requirements

- **Windows 10/11** (64-bit)
- **At least 2 GB** free disk space
- **Internet connection** (for initial model download)

### Troubleshooting

- **Windows Defender warning?** Click "More info" → "Run anyway" (the app is safe)
- **App won't start?** Make sure you extracted all files from the ZIP
- **First launch slow?** This is normal - the app is loading AI models

---

## 🧰 Requirements (For Developers)

| Component | Details |
|-----------|---------|
| **OS** | Windows 10 / 11 (PySide6 + Win32 APIs) |
| **Python** | 3.9 or later (for development) |
| **Hardware** | ≥2 GB free space, Internet connection (for model download) |

### Dependencies
See [`requirements.txt`](./requirements.txt).  
Install everything via:
```bash
pip install -r requirements.txt
```

---

## 🏗️ Project Structure

```
FoxMate AI/
│
├── launcher.py              # 🟢 Main entry point (for PyInstaller)
├── FoxMate AI.spec          # PyInstaller configuration
├── build_package.bat        # Windows build script
├── build_package.sh         # Linux/Git Bash build script
│
├── frontend/                # Frontend application
│   ├── app.py               # Main frontend app
│   ├── routes.py            # Route definitions
│   └── pages/               # UI pages
│       ├── home.py
│       ├── my_info.py
│       ├── weekly_report.py
│       └── ...
│
├── backend/                 # Backend logic and pet UI
│   ├── run.py               # Main backend entry point
│   ├── pet_ui.py            # Floating fox pet UI
│   ├── focus_regressor_sbert.pkl  # Trained ML model
│   ├── images/              # Fox animation images
│   └── activity_log_focus.jsonl   # Activity log
│
├── AI Part/                 # AI model training
│   ├── AI.py                # Model training code
│   └── focus_model.pkl      # Classifier model
│
├── docs/                    # Documentation
│   └── (packaging guides, fix notes, etc.)
│
└── README.txt               # User instructions (for distribution)
```

---

## 👨‍💻 For Developers

### Quick Start

1. **Clone or Download**
   ```bash
   git clone https://github.com/yourusername/FoxMate-AI.git
   cd FoxMate-AI
   ```
   Or download ZIP and extract it

2. **Set Up Environment**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run in Development Mode**
   ```bash
   # Run frontend
   python launcher.py
   
   # Run backend (in separate terminal)
   python launcher.py --backend
   ```

### Building Executable

To create a distributable `.exe` file:

1. **Windows:**
   ```bash
   build_package.bat
   ```
   Or manually:
   ```bash
   pyinstaller "FoxMate AI.spec"
   ```

2. **Linux/Git Bash:**
   ```bash
   ./build_package.sh
   ```

3. **Output:** The executable will be in `dist/FoxMate AI/FoxMate AI.exe`

   **For distribution:** Create a ZIP file containing:
   - `dist/FoxMate AI/` folder (with `FoxMate AI.exe` and `_internal/`)
   - `README.txt` (user instructions)

---

## 📦 Distribution

The project uses PyInstaller to create a single executable:

- **Entry point:** `launcher.py`
- **Configuration:** `FoxMate AI.spec`
- **Output:** Single `.exe` file with all dependencies bundled

### Distribution Package Structure

```
FoxMate AI v1.0.zip
├── FoxMate AI/
│   ├── FoxMate AI.exe
│   └── _internal/          # Bundled dependencies
└── README.txt              # User instructions
```

---

## 🎯 Usage Guide

### For End Users

1. **Launch:** Double-click `FoxMate AI.exe`
2. **Start Monitoring:** Click the **"Fox it!"** button on the home page
3. **View Reports:** Access weekly reports from the menu
4. **Customize:** Adjust settings in the Settings page

### Features Overview

- **Home Page:** Main dashboard with quick access to all features
- **My Account:** View and manage your account information
- **Weekly Report:** See your focus statistics and trends
- **Your Fox:** View your fox pet status and customization
- **Settings:** Configure app preferences

---

## 🔧 Development Notes

### Key Components

- **Frontend:** PySide6-based mobile-style UI
- **Backend:** Focus tracking with Windows API + ML prediction
- **Models:** LightGBM regressor + SentenceTransformer embeddings

### Important Files

- `launcher.py` - Unified entry point (handles `--backend` flag)
- `frontend/app.py` - Frontend application
- `backend/run.py` - Backend service (`_run()` function)
- `FoxMate AI.spec` - PyInstaller configuration

### Packaging Notes

- Uses `subprocess` to launch backend in separate process (avoids QApplication conflicts)
- All resources bundled via `datas` in `.spec` file
- Hidden imports explicitly listed for ML libraries

---

## 📝 License

[Add your license here]

---

## 🤝 Contributing

[Add contribution guidelines here]

---

## 📚 Documentation

Additional documentation available in [`docs/`](./docs/) directory:
- Packaging guides
- Fix notes and troubleshooting
- Build instructions

---

**Version:** 1.0.0  
**Last Updated:** January 2025
