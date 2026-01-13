# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],  # 使用launcher.py作为入口点
    pathex=['.'], # Start search in current directory (project root)
    binaries=[],
    datas=[
        # --- Frontend Files ---
        ('frontend/app.py', 'frontend'),  # 主前端文件
        ('frontend/routes.py', 'frontend'),
        ('frontend/pages', 'frontend/pages'),
        ('frontend/__init__.py', 'frontend'),  # 确保frontend是一个包
        
        # --- Backend Images ---
        ('backend/images', 'backend/images'),
        
        # --- Backend Files & Models ---
        ('backend/run.py', 'backend'),
        ('backend/pet_ui.py', 'backend'),
        ('backend/__init__.py', 'backend'),  # 确保backend是一个包
        ('backend/focus_regressor_sbert.pkl', 'backend'), # Model bundle
        ('backend/result.txt', 'backend'),
        
        # --- AI Part Files ---
        ('AI Part/AI.py', 'AI Part'),
        ('AI Part/focus_model.pkl', 'AI Part'), # Classifier model
        
        # --- Sound File ---
        ('notification-alert-269289.mp3', '.'),
        
        # --- Data Files (Needed for logging, though content is skipped) ---
        ('backend/activity_log_focus.jsonl', 'backend'),
    ],
    hiddenimports=[
        # Frontend and Backend modules (explicitly include)
        'app',  # frontend/app.py
        'run',  # backend/run.py
        'routes',  # frontend/routes.py
        'pet_ui',  # backend/pet_ui.py
        
        # System monitoring
        'psutil', 'pynput', 'win32gui', 'win32process',
        
        # Model serialization (joblib needs all model libraries)
        'joblib',
        
        # Machine Learning libraries (needed for model loading)
        'lightgbm',  # Required for .pkl model deserialization
        'sklearn', 'sklearn.neighbors._base', 'sklearn.ensemble',
        'sklearn.linear_model', 'sklearn.tree', 'sklearn.base',
        'sklearn.utils', 'sklearn.utils._param_validation',
        
        # Sentence transformers
        'sentence_transformers',
        
        # Data science libraries
        'numpy', 'pandas', 'scipy',
        
        # Visualization
        'matplotlib', 'matplotlib.backends.backend_agg',
        'PIL', 'PIL.Image', 'PIL.ImageTk',
        
        # Tkinter and its submodules (for report generator)
        'tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox',
        
        # PySide6 GUI
        'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
        
        # Windows COM for sound playback
        'win32com.client',
        
        # PyTorch and transformers (if used by models)
        'torch', 'torch.nn', 'torch.optim', 'torch.utils.data',
        'transformers',
        
        # Progress bar (used by AI.py)
        'tqdm',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
# ... everything else below 'a = Analysis(...)'
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FoxMate AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Temporarily enable console for debugging (change back to False after fixing)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Can add icon path here if you have one
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FoxMate AI',
)
