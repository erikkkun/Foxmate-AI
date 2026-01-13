# Packaging Guide

This document explains how to build and distribute FoxMate AI as a standalone executable.

## Overview

FoxMate AI uses PyInstaller to create a single executable file that bundles all dependencies, making it easy to distribute without requiring users to install Python or dependencies.

## Build Process

### Prerequisites

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

### Building

#### Windows (Command Prompt)
```bash
build_package.bat
```

#### Windows (Git Bash)
```bash
./build_package.sh
```

#### Manual Build
```bash
pyinstaller "FoxMate AI.spec"
```

### Output

The build process creates:
- `build/` - Temporary build files (can be deleted)
- `dist/FoxMate AI/` - Final distribution package
  - `FoxMate AI.exe` - Main executable
  - `_internal/` - Bundled dependencies and resources

## Configuration

The build configuration is in `FoxMate AI.spec`:

- **Entry point:** `launcher.py`
- **Data files:** All images, models, and resources listed in `datas`
- **Hidden imports:** ML libraries and submodules explicitly listed
- **Console:** Currently enabled for debugging (set `console=False` for release)

## Key Design Decisions

### 1. Unified Entry Point (`launcher.py`)

Instead of separate executables, we use a single entry point that checks command-line arguments:
- No arguments → Start frontend
- `--backend` argument → Start backend

This avoids QApplication conflicts and simplifies distribution.

### 2. Subprocess Launch

The frontend uses `subprocess.Popen` to launch the backend in a separate process:
- Avoids multiprocessing pickle issues
- Each process has independent QApplication instance
- Simple and reliable

### 3. Resource Bundling

All resources are explicitly listed in `datas`:
- Frontend pages and routes
- Backend images and models
- Sound files
- Data files

## Troubleshooting

### Common Issues

1. **Missing modules:** Add to `hiddenimports` in `.spec` file
2. **Missing files:** Add to `datas` in `.spec` file
3. **QApplication conflicts:** Ensure backend runs in separate process
4. **Import errors:** Check that all modules are in `hiddenimports`

### Debug Mode

To enable console output for debugging:
- Set `console=True` in `FoxMate AI.spec`
- Rebuild the executable
- Check console output for errors

## Distribution

### Creating Distribution Package

1. Build the executable (see above)
2. Create ZIP file:
   ```
   FoxMate AI v1.0.zip
   ├── FoxMate AI/
   │   ├── FoxMate AI.exe
   │   └── _internal/
   └── README.txt
   ```

3. Test on clean Windows machine (without Python installed)

### User Instructions

Include `README.txt` in the distribution package with:
- System requirements
- Installation instructions
- Usage guide
- Troubleshooting tips

## Future Improvements

- [ ] Code signing for Windows
- [ ] Auto-update mechanism
- [ ] Installer (NSIS/Inno Setup)
- [ ] Icon file for executable
- [ ] Version information in executable
