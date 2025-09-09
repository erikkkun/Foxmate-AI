from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QBrush

# ====== 可复用的 TopBar ======
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


# ====== FAQ 页面 ======
class FAQPage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # 顶部 bar
        top = TopBar(on_menu, on_settings, on_close)
        root.addLayout(top)

        # ===== Title =====
        title = QLabel("FAQ & Support")
        title.setStyleSheet("color:white; font-size:24px; font-weight:700;")
        root.addWidget(title, alignment=Qt.AlignHCenter)

        # ===== Buttons (fake URLs) =====
        self._add_button(root, "Quick FAQ", "https://fake-link.com/faq")
        self._add_button(root, "Issue Search", "https://fake-link.com/search")
        self._add_button(root, "Submit Your Feedback", "https://fake-link.com/feedback")
        self._add_button(root, "View Tutorials", "https://fake-link.com/tutorials")
        self._add_button(root, "Contact Us", "https://fake-link.com/contact")

        root.addStretch()

        # ===== Contact Info =====
        contact = QLabel("Contact Us:\n(949) · fox · mate\nus.support@foxmate.com")
        contact.setStyleSheet("color:white; font-size:14px;")
        contact.setAlignment(Qt.AlignCenter)
        root.addWidget(contact)

    def _add_button(self, layout, text, fake_url):
        btn = QPushButton(text + " →")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 18px;
                text-align: left;
                border: none;
                padding: 8px 12px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.1); border-radius: 6px; }
        """)
        # 现在只是打印 URL，未来可以换成真正的 webbrowser.open(url)
        btn.clicked.connect(lambda: print(f"TODO: Open {fake_url}"))
        layout.addWidget(btn)

    def paintEvent(self, e):
        """背景渐变"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)
