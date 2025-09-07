from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtGui import QFont, QPainter, QLinearGradient, QColor, QBrush
from PySide6.QtCore import Qt


class TopBar(QHBoxLayout):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(8)

        def _make_btn(symbol, slot=None):
            b = QPushButton(symbol)
            b.setFixedSize(32, 32)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    color:white; font-size:20px; border:none; background:transparent;
                }
                QPushButton:hover { background: rgba(255,255,255,0.12); border-radius:8px; }
            """)
            if slot:
                b.clicked.connect(slot)
            return b

        self.btn_menu = _make_btn("≡", on_menu)
        self.btn_settings = _make_btn("⚙", on_settings)
        self.btn_close = _make_btn("✕", on_close)

        self.addWidget(self.btn_menu)
        self.addStretch()
        self.addWidget(self.btn_settings)
        self.addWidget(self.btn_close)


class MembershipPage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
# 顶部 bar
        top = TopBar(on_menu, on_settings, on_close)
        layout.addLayout(top)

        title = QLabel("Membership")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:white; font-size:26px; font-weight:800; background:transparent;")
        layout.addWidget(title)

        gold = self._make_plan("🦊", "Gold Fox", "$3.99/Mo\n$39.99/Year")
        layout.addWidget(gold)

        platinum = self._make_plan("🦊", "Platinum", "$6.99/Mo\n$69.99/Year")
        layout.addWidget(platinum)

        note = QLabel("Sign in with school account for 2 months free!")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("color:white; font-size:14px; background:transparent;")
        layout.addStretch()
        layout.addWidget(note)

    def _make_plan(self, emoji, name, price):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.2);
                border-radius: 16px;
            }
        """)
        frame.setFixedHeight(120)
        lay = QHBoxLayout(frame)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(10)

        icon_lbl = QLabel(emoji)
        icon_lbl.setStyleSheet("font-size:28px; background:transparent; border:none;")
        lay.addWidget(icon_lbl, alignment=Qt.AlignTop)

        text_col = QVBoxLayout()
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color:white; font-size:20px; font-weight:700; background:transparent;")

        price_lbl = QLabel(price)
        price_lbl.setStyleSheet("color:white; font-size:16px; font-weight:500; background:transparent;")
        price_lbl.setAlignment(Qt.AlignLeft)

        btn = QPushButton("Choose Plan")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #0c4a6e;
                color:white;
                border:none;
                border-radius:12px;
                padding:6px 12px;
                font-weight:600;
            }
            QPushButton:hover { background:#075985; }
        """)

        text_col.addWidget(name_lbl, alignment=Qt.AlignLeft)
        text_col.addWidget(price_lbl, alignment=Qt.AlignLeft)
        text_col.addStretch()
        text_col.addWidget(btn, alignment=Qt.AlignLeft)
        lay.addLayout(text_col)

        return frame

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)
