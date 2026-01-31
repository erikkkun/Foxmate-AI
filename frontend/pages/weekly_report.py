from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt


class WeeklyReportPage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()

        # ✅ 让 theme.py 的 QWidget#Page 背景生效
        self.setObjectName("Page")
        self.setAttribute(Qt.WA_StyledBackground, True)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(10)

        # ===== 顶部 bar =====
        top = QHBoxLayout()
        self._add_top_btn(top, "≡", on_menu)
        top.addStretch()
        self._add_top_btn(top, "⚙", on_settings)
        self._add_top_btn(top, "✕", on_close)
        root.addLayout(top)

        # ===== Stacked pages =====
        self.stack = QStackedWidget()
        self.stack.setObjectName("Card")  # 可选：想要像卡片一样的质感
        self.stack.addWidget(self._make_weekly_status())
        self.stack.addWidget(self._make_compare_last_week())
        self.stack.addWidget(self._make_concentration_chart())
        self.stack.addWidget(self._make_working_time_chart())
        self.stack.addWidget(self._make_upgrade_page())

        root.addWidget(self.stack)

    def _title(self, text: str) -> QLabel:
        t = QLabel(text)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("color: rgba(0,0,0,0.82); font-size:22px; font-weight:700;")
        return t

    def _text(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setStyleSheet("color: rgba(0,0,0,0.78); font-size:16px;")
        l.setAlignment(Qt.AlignLeft)
        return l

    def _nav_btn(self, symbol: str, slot):
        b = QPushButton(symbol)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedSize(40, 40)
        b.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.70);
                border: 1px solid rgba(0,0,0,0.08);
                border-radius: 12px;
                color: rgba(0,0,0,0.70);
                font-size: 18px;
                font-weight: 700;
            }
            QPushButton:hover { background: rgba(255,255,255,0.92); }
        """)
        b.clicked.connect(slot)
        return b

    def _make_weekly_status(self):
        page = QWidget()
        page.setObjectName("Page")
        page.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        layout.addWidget(self._title("Weekly Status"))

        layout.addWidget(self._text("Times Study Last Week: 7  (>92%)"))
        layout.addWidget(self._text("Average Study Time: 48.3 min  (>73%)"))
        layout.addWidget(self._text("Average Concentration Rate: 81  (>88.2%)"))
        layout.addWidget(self._text("Average Diversion#: 13 times/study  (>98%)"))

        layout.addStretch()

        btn_next = self._nav_btn("⬇", lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_next, alignment=Qt.AlignCenter)

        return page

    def _make_compare_last_week(self):
        page = QWidget()
        page.setObjectName("Page")
        page.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        layout.addWidget(self._title("Compare to Last Week"))
        layout.addWidget(self._text("(placeholder)"))

        layout.addStretch()

        nav = QHBoxLayout()
        nav.addWidget(self._nav_btn("⬆", lambda: self.stack.setCurrentIndex(0)))
        nav.addStretch()
        nav.addWidget(self._nav_btn("⬇", lambda: self.stack.setCurrentIndex(2)))
        layout.addLayout(nav)

        return page

    def _make_concentration_chart(self):
        page = QWidget()
        page.setObjectName("Page")
        page.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        layout.addWidget(self._title("Concentration Tracking"))
        layout.addWidget(self._text("(chart placeholder)"))

        layout.addStretch()

        nav = QHBoxLayout()
        nav.addWidget(self._nav_btn("⬆", lambda: self.stack.setCurrentIndex(1)))
        nav.addStretch()
        nav.addWidget(self._nav_btn("⬇", lambda: self.stack.setCurrentIndex(3)))
        layout.addLayout(nav)

        return page

    def _make_working_time_chart(self):
        page = QWidget()
        page.setObjectName("Page")
        page.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        layout.addWidget(self._title("Working Time"))
        layout.addWidget(self._text("(chart placeholder)"))

        layout.addStretch()

        nav = QHBoxLayout()
        nav.addWidget(self._nav_btn("⬆", lambda: self.stack.setCurrentIndex(2)))
        nav.addStretch()
        nav.addWidget(self._nav_btn("⬇", lambda: self.stack.setCurrentIndex(4)))
        layout.addLayout(nav)

        return page

    def _make_upgrade_page(self):
        page = QWidget()
        page.setObjectName("Page")
        page.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(page)
        layout.setSpacing(12)

        layout.addWidget(self._title("Upgrade"))
        msg = QLabel("Upgrade to Gold Fox to unlock premium plan!")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("color: rgba(0,0,0,0.78); font-size:16px;")
        layout.addWidget(msg)

        layout.addStretch()

        btn_prev = self._nav_btn("⬆", lambda: self.stack.setCurrentIndex(3))
        layout.addWidget(btn_prev, alignment=Qt.AlignCenter)

        return page

    def _add_top_btn(self, layout, symbol, slot=None):
        b = QPushButton(symbol)
        b.setFixedSize(32, 32)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet("""
            QPushButton {
                color: rgba(0,0,0,0.70);
                font-size: 20px;
                border: none;
                background: rgba(255,255,255,0.60);
                border-radius: 10px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.92); }
        """)
        if slot:
            b.clicked.connect(slot)
        layout.addWidget(b)
