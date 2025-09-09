from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QBrush


class CustomizePage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # ===== Top Bar =====
        top = QHBoxLayout()
        self._add_top_btn(top, "≡", on_menu)
        top.addStretch()
        self._add_top_btn(top, "⚙", on_settings)
        self._add_top_btn(top, "✕", on_close)
        root.addLayout(top)

        # ===== Title =====
        title = QLabel("Customize")
        title.setStyleSheet("color:white; font-size:24px; font-weight:700;")
        root.addWidget(title, alignment=Qt.AlignHCenter)

        # ===== Daily Objective =====
        root.addLayout(self._make_input_row("Daily Objective", "min"))

        # ===== Break Every =====
        root.addLayout(self._make_input_row("Break Every", "min"))

        # ===== Rest Reminder =====
        row = QHBoxLayout()
        lbl = QLabel("Rest Reminder")
        lbl.setStyleSheet("color:white; font-size:16px;")
        row.addWidget(lbl)
        row.addStretch()
        self.rest_toggle = QPushButton("Off")
        self.rest_toggle.setCheckable(True)
        self.rest_toggle.toggled.connect(self._toggle_rest)
        self._toggle_rest(False)
        row.addWidget(self.rest_toggle)
        root.addLayout(row)



        # ===== MBTI =====
        mbti_row = QHBoxLayout()
        mbti_lbl = QLabel("Your MBTI")
        mbti_lbl.setStyleSheet("color:white; font-size:16px;")
        mbti_box = QComboBox()
        mbti_types = [
            "INTJ", "INTP", "ENTJ", "ENTP",
            "INFJ", "INFP", "ENFJ", "ENFP",
            "ISTJ", "ISFJ", "ESTJ", "ESFJ",
            "ISTP", "ISFP", "ESTP", "ESFP"
        ]
        mbti_box.addItems(mbti_types)
        mbti_row.addWidget(mbti_lbl)
        mbti_row.addStretch()
        mbti_row.addWidget(mbti_box)
        root.addLayout(mbti_row)

        
        
        
        # ===== Whitelist =====
        wl_row = QHBoxLayout()
        wl_lbl = QLabel("Your Personal Whitelist")
        wl_lbl.setStyleSheet("color:white; font-size:16px;")
        self.wl_input = QLineEdit()
        self.wl_input.setPlaceholderText("Type URL and press Enter")
        self.wl_input.returnPressed.connect(self._add_whitelist_item)
        wl_row.addWidget(wl_lbl)
        wl_row.addStretch()
        wl_row.addWidget(self.wl_input)
        root.addLayout(wl_row)

        # 动态 whitelist 容器
        self.wl_container = QVBoxLayout()
        root.addLayout(self.wl_container)
        
        
        root.addStretch()
        
    # ---- Helpers ----
    def _make_input_row(self, label_text, unit):
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color:white; font-size:16px;")
        inp = QLineEdit()
        inp.setFixedWidth(60)
        unit_lbl = QLabel(unit)
        unit_lbl.setStyleSheet("color:white; font-size:16px;")
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(inp)
        row.addWidget(unit_lbl)
        return row

    def _add_top_btn(self, layout, symbol, slot=None):
        b = QPushButton(symbol)
        b.setFixedSize(32, 32)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet("""
            QPushButton { color:#fff; font-size:20px; border:none; background:transparent; }
            QPushButton:hover { background: rgba(255,255,255,0.12); border-radius:8px; }
        """)
        if slot:
            b.clicked.connect(slot)
        layout.addWidget(b)

    def _toggle_rest(self, checked):
        if checked:
            self.rest_toggle.setText("On")
            self.rest_toggle.setStyleSheet("background:#34d399; color:white; border-radius:12px; padding:4px 12px;")
        else:
            self.rest_toggle.setText("Off")
            self.rest_toggle.setStyleSheet("background:#9ca3af; color:white; border-radius:12px; padding:4px 12px;")

    def _add_whitelist_item(self):
        text = self.wl_input.text().strip()
        if not text:
            return
        item = WhitelistItem(text, self.wl_container)
        self.wl_container.addWidget(item)
        self.wl_input.clear()


    def paintEvent(self, e):
        """背景渐变"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)


from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class WhitelistItem(QWidget):
    def __init__(self, text, parent_layout):
        super().__init__()
        self.parent_layout = parent_layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.label = QLabel(text)
        self.label.setStyleSheet("color:white; font-size:14px;")
        layout.addWidget(self.label)

        btn = QPushButton("✕")
        btn.setFixedSize(20, 20)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                color:white;
                font-size:12px;
                border:none;
                border-radius:10px;
                background:#ef4444;
            }
            QPushButton:hover { background:#b91c1c; }
        """)
        btn.clicked.connect(self.remove_self)
        layout.addWidget(btn)

    def remove_self(self):
        """从父布局中移除自己"""
        self.setParent(None)
        self.deleteLater()
