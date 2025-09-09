from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QBrush

class WeeklyReportPage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
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
        self.stack.addWidget(self._make_weekly_status())
        self.stack.addWidget(self._make_compare_last_week())
        self.stack.addWidget(self._make_concentration_chart())
        self.stack.addWidget(self._make_working_time_chart())
        self.stack.addWidget(self._make_upgrade_page())

        root.addWidget(self.stack)

    def _make_weekly_status(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Weekly Status")
        title.setStyleSheet("color:white; font-size:22px; font-weight:700;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addWidget(QLabel("Times Study Last Week: 7 (>92%)"))
        layout.addWidget(QLabel("Average Study Time: 48.3 min (>73%)"))
        layout.addWidget(QLabel("Average Concentration Rate: 81 (>88.2%)"))
        layout.addWidget(QLabel("Average Diversion#: 13 times/study (>98%)"))

        # 下箭头
        btn_next = QPushButton("⬇")
        btn_next.setStyleSheet("color:white; background:transparent; font-size:20px;")
        btn_next.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_next, alignment=Qt.AlignCenter)

        return page

    def _make_compare_last_week(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Compare to Last Week (placeholder)", alignment=Qt.AlignCenter))

        # 上下切换按钮
        btn_prev = QPushButton("⬆")
        btn_prev.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_next = QPushButton("⬇")
        btn_next.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        nav = QHBoxLayout()
        nav.addWidget(btn_prev)
        nav.addWidget(btn_next)
        layout.addLayout(nav)

        return page

    def _make_concentration_chart(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Concentration Tracking (chart placeholder)", alignment=Qt.AlignCenter))

        btn_prev = QPushButton("⬆")
        btn_prev.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_next = QPushButton("⬇")
        btn_next.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        nav = QHBoxLayout()
        nav.addWidget(btn_prev)
        nav.addWidget(btn_next)
        layout.addLayout(nav)

        return page

    def _make_working_time_chart(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Working Time (chart placeholder)", alignment=Qt.AlignCenter))

        btn_prev = QPushButton("⬆")
        btn_prev.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_next = QPushButton("⬇")
        btn_next.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        nav = QHBoxLayout()
        nav.addWidget(btn_prev)
        nav.addWidget(btn_next)
        layout.addLayout(nav)

        return page

    def _make_upgrade_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Upgrade to Gold Fox to unlock premium plan!", alignment=Qt.AlignCenter))

        btn_prev = QPushButton("⬆")
        btn_prev.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        layout.addWidget(btn_prev, alignment=Qt.AlignCenter)

        return page

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

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)
