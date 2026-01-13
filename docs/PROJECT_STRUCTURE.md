# Project Structure

This document describes the organization of the FoxMate AI project.

## Directory Structure

```
FoxMate AI/
│
├── 📄 launcher.py              # Main entry point (handles --backend flag)
├── 📄 FoxMate AI.spec          # PyInstaller configuration
├── 📄 build_package.bat        # Windows build script
├── 📄 build_package.sh         # Linux/Git Bash build script
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md                # Main project documentation
├── 📄 README.txt               # User instructions (for distribution)
├── 📄 .gitignore              # Git ignore rules
│
├── 📁 frontend/                # Frontend application
│   ├── app.py                  # Main frontend app (QApplication)
│   ├── routes.py               # Route definitions
│   ├── pages/                  # UI pages
│   │   ├── home.py            # Home page with "Fox it!" button
│   │   ├── my_info.py         # User account page
│   │   ├── membership.py      # Membership page
│   │   ├── customize.py       # Customization page
│   │   ├── weekly_report.py   # Weekly report page
│   │   ├── workshop.py        # Workshop page
│   │   ├── fox_pet.py         # Fox pet page
│   │   ├── shop.py            # Shop page
│   │   ├── settings.py        # Settings page
│   │   ├── signin.py          # Sign-in dialog
│   │   └── faq.py             # FAQ page
│   └── __init__.py
│
├── 📁 backend/                 # Backend logic and pet UI
│   ├── run.py                  # Main backend entry point (_run function)
│   ├── pet_ui.py              # Floating fox pet UI (PySide6)
│   ├── focus_regressor_sbert.pkl  # Trained ML model (LightGBM)
│   ├── activity_log_focus.jsonl   # Activity log file
│   ├── focus_training_data_large.csv  # Training data
│   ├── train_focus_regressor_sbert.py  # Model training script
│   ├── result.txt             # Temporary result file
│   ├── images/                # Fox animation images
│   │   ├── fox_neutral.png
│   │   ├── fox_focus.png
│   │   ├── fox_distracted.png
│   │   ├── fox_energized.png
│   │   ├── fox_celebrate.png
│   │   └── fox_sleepy.png
│   └── __init__.py
│
├── 📁 AI Part/                 # AI model training
│   ├── AI.py                   # Model training code (PyTorch)
│   ├── focus_model.pkl         # Classifier model
│   ├── focused_data.txt        # Training data
│   ├── not_focused_data.txt    # Training data
│   └── process_file.py         # Data processing script
│
├── 📁 docs/                    # Documentation
│   ├── PACKAGING.md            # Packaging guide
│   ├── PROJECT_STRUCTURE.md    # This file
│   └── (various fix notes and guides)
│
├── 📁 build/                   # PyInstaller build files (temporary)
│   └── (can be deleted after build)
│
└── 📁 dist/                    # Distribution package (output)
    └── FoxMate AI/
        ├── FoxMate AI.exe      # Final executable
        └── _internal/          # Bundled dependencies
```

## Key Files

### Entry Points

- **`launcher.py`** - Unified entry point that handles both frontend and backend
  - No arguments → Start frontend
  - `--backend` argument → Start backend

### Configuration

- **`FoxMate AI.spec`** - PyInstaller configuration
  - Entry point: `launcher.py`
  - Data files: All resources listed in `datas`
  - Hidden imports: ML libraries explicitly listed

### Build Scripts

- **`build_package.bat`** - Windows build script
- **`build_package.sh`** - Linux/Git Bash build script

## File Purposes

### Frontend (`frontend/`)

- **`app.py`** - Main frontend application
  - Creates QApplication
  - Manages window and navigation
  - Handles "Fox it!" button click → launches backend via subprocess

- **`routes.py`** - Route definitions (enum)

- **`pages/`** - Individual UI pages
  - Each page is a QWidget subclass
  - Pages are registered in `app.py`

### Backend (`backend/`)

- **`run.py`** - Main backend service
  - `_run()` function creates QApplication and FloatingPet
  - Monitors active window activity
  - Uses ML model to predict focus scores

- **`pet_ui.py`** - Floating fox pet UI
  - PySide6-based floating window
  - Displays fox images based on focus state
  - Plays sound alerts

- **`focus_regressor_sbert.pkl`** - Trained ML model
  - LightGBM regressor
  - Uses SentenceTransformer embeddings
  - Predicts focus scores (0-100)

### AI Part (`AI Part/`)

- **`AI.py`** - Model training code
  - PyTorch-based classifier
  - Trains on focus/not-focus data

## Resource Files

- **`notification-alert-269289.mp3`** - Sound alert file
- **`backend/images/`** - Fox animation images
- **`backend/focus_regressor_sbert.pkl`** - ML model file
- **`AI Part/focus_model.pkl`** - Classifier model

## Temporary Files (Can Be Deleted)

- **`build/`** - PyInstaller build files
- **`dist/`** - Distribution output (keep for distribution)
- **`__pycache__/`** - Python cache files
- **`backend/result.txt`** - Temporary result file
- **`backend/activity_log_focus.jsonl`** - Log file (can be regenerated)

## Documentation

- **`README.md`** - Main project documentation
- **`README.txt`** - User instructions (for distribution)
- **`docs/PACKAGING.md`** - Packaging guide
- **`docs/PROJECT_STRUCTURE.md`** - This file
- **`docs/`** - Various fix notes and troubleshooting guides

## Build Output

After running `pyinstaller "FoxMate AI.spec"`:

- **`build/`** - Temporary build files (can be deleted)
- **`dist/FoxMate AI/`** - Final distribution package
  - `FoxMate AI.exe` - Main executable
  - `_internal/` - All bundled dependencies and resources

## Distribution Package

The final distribution package structure:

```
FoxMate AI v1.0.zip
├── FoxMate AI/
│   ├── FoxMate AI.exe
│   └── _internal/
│       ├── (all Python modules)
│       ├── frontend/
│       ├── backend/
│       └── (all resources)
└── README.txt
```
