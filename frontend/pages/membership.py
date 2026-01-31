
# frontend/pages/membership.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt


class TopBar(QHBoxLayout):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(10)

        def _make_btn(symbol, slot=None):
            b = QPushButton(symbol)
            b.setFixedSize(40, 40)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    color: rgba(0,0,0,0.72);
                    font-size: 20px;
                    border: none;
                    background: rgba(255,255,255,0.60);
                    border-radius: 14px;
                }
                QPushButton:hover { background: rgba(243,154,45,0.16); }
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

        # ✅ 关键：让 theme.py 的 QWidget#Page 背景生效
        self.setObjectName("Page")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 顶部 bar
        top = TopBar(on_menu, on_settings, on_close)
        layout.addLayout(top)

        # Title
        title = QLabel("Membership")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#1C5B45; font-size:26px; font-weight:900; background:transparent;")
        layout.addWidget(title)

        # Plans
        gold = self._make_plan("🦊", "Gold Fox", "$3.99 / Mo\n$39.99 / Year", accent="gold")
        layout.addWidget(gold)

        platinum = self._make_plan("🦊", "Platinum", "$6.99 / Mo\n$69.99 / Year", accent="platinum")
        layout.addWidget(platinum)

        layout.addStretch()

        note = QLabel("Sign in with school account for 2 months free!")
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("color: rgba(0,0,0,0.55); font-size:13px; font-weight:600; background:transparent;")
        layout.addWidget(note)

    def _make_plan(self, emoji, name, price, accent="gold"):
        frame = QFrame()
        frame.setObjectName("PlanCard")
        frame.setFixedHeight(132)

        # 不同方案有不同强调色（很轻，保证统一）
        if accent == "platinum":
            rim = "rgba(28, 91, 69, 0.22)"     # 深绿
            chip_bg = "rgba(179, 227, 211, 0.35)"
        else:
            rim = "rgba(243,154,45,0.28)"     # 橙
            chip_bg = "rgba(243,154,45,0.14)"

        frame.setStyleSheet(f"""
            QFrame#PlanCard {{
                background: rgba(255,255,255,0.70);
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 18px;
            }}
        """)

        lay = QHBoxLayout(frame)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(12)

        # icon chip
        chip = QFrame()
        chip.setFixedSize(44, 44)
        chip.setStyleSheet(f"""
            QFrame {{
                background: {chip_bg};
                border: 1px solid {rim};
                border-radius: 14px;
            }}
        """)
        chip_lay = QVBoxLayout(chip)
        chip_lay.setContentsMargins(0, 0, 0, 0)

        icon_lbl = QLabel(emoji)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size:22px; background:transparent;")
        chip_lay.addWidget(icon_lbl)

        lay.addWidget(chip, alignment=Qt.AlignTop)

        # text col
        text_col = QVBoxLayout()
        text_col.setSpacing(6)

        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("color: rgba(0,0,0,0.82); font-size:18px; font-weight:900;")

        price_lbl = QLabel(price)
        price_lbl.setStyleSheet("color: rgba(0,0,0,0.62); font-size:14px; font-weight:700;")
        price_lbl.setAlignment(Qt.AlignLeft)

        btn = QPushButton("Choose Plan")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: rgba(255,255,255,0.70);
                border: 1px solid {rim};
                color: rgba(0,0,0,0.78);
                border-radius: 14px;
                padding: 8px 14px;
                font-weight: 800;
            }}
            QPushButton:hover {{
                background: rgba(243,154,45,0.14);
            }}
            QPushButton:pressed {{
                background: rgba(243,154,45,0.22);
            }}
        """)

        text_col.addWidget(name_lbl)
        text_col.addWidget(price_lbl)
        text_col.addStretch()
        text_col.addWidget(btn, alignment=Qt.AlignLeft)

        lay.addLayout(text_col)

        return frame
