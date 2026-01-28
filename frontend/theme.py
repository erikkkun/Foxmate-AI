# frontend/theme.py

LIGHT_QSS = """
/* ===== Global base ===== */
QWidget {
    font-family: "-apple-system","Segoe UI","Microsoft YaHei","Arial";
    color: rgba(0,0,0,0.84);
}

/* ===== Page background (统一浅色渐变背景) ===== */
QWidget#Page {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #FFF6E8,
        stop:0.50 #FBE7CF,
        stop:0.85 #F6D5A8,
        stop:1 #F3C98D
    );
}

/* 通用卡片 */
QFrame#Card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 18px;
}

/* ===== Drawer / Overlay ===== */
QWidget#overlay {
    background: rgba(0,0,0,120);
}

QFrame#drawer {
    background: rgba(255, 246, 232, 0.95);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 22px;
}

/* Drawer close */
QPushButton#drawerClose {
    color: rgba(0,0,0,0.70);
    border: none;
    font-size: 18px;
}
QPushButton#drawerClose:hover {
    background: rgba(0,0,0,0.06);
    border-radius: 14px;
}

/* Drawer items（只给抽屉里的按钮生效） */
QPushButton[drawerItem="true"] {
    color: rgba(0,0,0,0.82);
    font-size: 20px;
    padding: 12px 14px;
    text-align: left;
    border: none;
    border-radius: 12px;
    background: transparent;
}
QPushButton[drawerItem="true"]:hover {
    background: rgba(243,154,45,0.16);
}

/* ===== Inputs / Combo ===== */
QLineEdit, QComboBox {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(0,0,0,0.12);
    border-radius: 12px;
    padding: 8px 10px;
}
QComboBox::drop-down { border: none; width: 26px; }
QComboBox QAbstractItemView {
    background: white;
    border: 1px solid rgba(0,0,0,0.15);
}

/* ===== Generic Buttons ===== */
QPushButton {
    border: none;
}
"""

def apply_theme(app):
    app.setStyleSheet(LIGHT_QSS)
