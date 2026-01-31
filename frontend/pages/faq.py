# frontend/pages/faq.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt


# ====== 可复用的 TopBar（浅色主题版） ======
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


# ====== FAQ 页面 ======
class FAQPage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()

        # ✅ 关键：让 theme.py 的 QWidget#Page 背景生效
        self.setObjectName("Page")
        self.setAttribute(Qt.WA_StyledBackground, True)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # 顶部 bar
        top = TopBar(on_menu, on_settings, on_close)
        root.addLayout(top)

        # Title
        title = QLabel("FAQ & Support")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#1C5B45; font-size:24px; font-weight:900; background:transparent;")
        root.addWidget(title)

        # 说明文字（可选）
        hint = QLabel("Find answers quickly, or contact us if you need help.")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: rgba(0,0,0,0.55); font-size:13px; font-weight:600;")
        root.addWidget(hint)

        # Links card
        card = QFrame()
        card.setObjectName("Card")
        card.setStyleSheet("""
            QFrame#Card {
                background: rgba(255,255,255,0.72);
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 18px;
            }
        """)
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(14, 14, 14, 14)
        card_lay.setSpacing(10)

        self._add_link_button(card_lay, "Quick FAQ", "https://fake-link.com/faq")
        self._add_link_button(card_lay, "Issue Search", "https://fake-link.com/search")
        self._add_link_button(card_lay, "Submit Your Feedback", "https://fake-link.com/feedback")
        self._add_link_button(card_lay, "View Tutorials", "https://fake-link.com/tutorials")
        self._add_link_button(card_lay, "Contact Us", "https://fake-link.com/contact")

        root.addWidget(card)
        root.addStretch()

        # Contact info
        contact = QLabel("Contact Us:\n(949) · fox · mate\nus.support@foxmate.com")
        contact.setAlignment(Qt.AlignCenter)
        contact.setStyleSheet("color: rgba(0,0,0,0.62); font-size:13px; font-weight:650;")
        root.addWidget(contact)

    def _add_link_button(self, layout, text, fake_url):
        btn = QPushButton(f"{text}  →")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 12px 12px;
                border-radius: 14px;
                border: 1px solid rgba(0,0,0,0.06);
                background: rgba(255,255,255,0.55);
                color: rgba(0,0,0,0.78);
                font-size: 16px;
                font-weight: 800;
            }
            QPushButton:hover {
                background: rgba(243,154,45,0.14);
                border: 1px solid rgba(243,154,45,0.22);
            }
            QPushButton:pressed {
                background: rgba(243,154,45,0.22);
            }
        """)
        btn.clicked.connect(lambda: print(f"TODO: Open {fake_url}"))
        layout.addWidget(btn)
