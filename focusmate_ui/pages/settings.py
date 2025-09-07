from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QLinearGradient, QColor, QBrush

from PySide6.QtWidgets import QCheckBox


from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtGui import QPainter, QColor, QBrush

from PySide6.QtWidgets import QCheckBox
from PySide6.QtCore import QPropertyAnimation, QRect, Qt, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QCheckBox

class ToggleSwitch(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setTristate(False)
        self.setFixedSize(60, 28)
        self.setStyleSheet("""
        QCheckBox::indicator {
        width: 50px;
        height: 28px;
        border-radius: 14px;
    }

    /* 未选中状态的轨道 */
    QCheckBox::indicator:unchecked {
        background-color: #cccccc;
    }

    /* 选中状态的轨道 */
    QCheckBox::indicator:checked {
        background-color: #4ade80;
    }

    /* 在轨道里放一个白色圆点 —— 用 box-shadow 来假装 knob */
    QCheckBox::indicator:unchecked {
        border: 3px solid #cccccc;
        background-color: white;
        margin-left: 0px;
    }
    QCheckBox::indicator:checked {
        border: 3px solid #4ade80;
        background-color: white;
        margin-left: 22px;  /* 往右移动 */
    }
        """)


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

class SettingsPage(QWidget):
    def __init__(self, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # 顶部 bar
        top = TopBar(on_menu, on_settings, on_close)
        root.addLayout(top)

        # 标题
        title = QLabel("Setting")
        title.setStyleSheet("color:white; font-size:24px; font-weight:700;")
        root.addWidget(title)

        # 选项行
        root.addLayout(self._make_row("Dark Mode", ToggleSwitch()))
        root.addLayout(self._make_row("Study Reminder", ToggleSwitch()))
        root.addLayout(self._make_row("Mark Read", ToggleSwitch()))
        root.addLayout(self._make_row("Notification", ToggleSwitch()))

        # Language 选择
        lang_combo = QComboBox()
        lang_combo.addItems(["English", "中文", "日本語"])
        root.addLayout(self._make_row("Language", lang_combo))

        # Task Cycle 选择
        cycle_combo = QComboBox()
        cycle_combo.addItems(["Daily", "Weekly", "Monthly"])
        root.addLayout(self._make_row("Task Cycle", cycle_combo))

        root.addStretch()

    def _make_row(self, text, widget):
        """生成一行: 左label + 右控件"""
        row = QHBoxLayout()
        lbl = QLabel(text)
        lbl.setStyleSheet("color:white; font-size:16px;")
        row.addWidget(lbl, alignment=Qt.AlignLeft)
        row.addStretch()
        row.addWidget(widget, alignment=Qt.AlignRight)
        return row

    def paintEvent(self, e):
        """背景渐变"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)
