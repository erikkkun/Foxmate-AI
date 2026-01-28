# frontend/pages/launching.py
import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from pathlib import Path
from PySide6.QtGui import QPixmap

class LaunchingPage(QWidget):
    """
    白底极简等待页（类似你发的示例）
    - 中间“狐狸”
    - 下方小 loading 圆圈（用进度条伪装成 spinner）
    - 文案：正在加载中，请稍后
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LaunchingPage")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addStretch(6)

        # ===== 狐狸（先用emoji占位，之后你换成图片也很简单）=====
        fox = QLabel()
        fox.setObjectName("bottombage")
        fox.setAlignment(Qt.AlignCenter)
        fox.setStyleSheet("background: transparent;")

        # 兼容 PyInstaller / 本地运行路径
        if getattr(sys, "frozen", False):
            base_dir = Path(sys._MEIPASS) / "frontend"
        else:
            base_dir = Path(__file__).resolve().parents[1]  # .../frontend

        img_path = base_dir / "assets" / "fox.png"  # <- 这里改成你的真实文件名
        pix = QPixmap(str(img_path))

        if not pix.isNull():
            # 你可以调这个大小，比如 140 / 160 / 200
            pix = pix.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            fox.setPixmap(pix)
        else:
            fox.setText("🦊")  # 找不到图片时 fallback
            fox.setStyleSheet("font-size: 64px; background: transparent;")
        fox_font = QFont()
        fox_font.setPointSize(64)          # 控制狐狸大小
        fox.setFont(fox_font)
        fox.setObjectName("Fox")

        root.addWidget(fox)
        root.addSpacing(18)

        # ===== loading 圆圈：用不确定进度条实现 =====
        spinner = QProgressBar()
        spinner.setRange(0, 0)             # 0,0 => 无限动画（indeterminate）
        spinner.setTextVisible(False)
        spinner.setFixedWidth(120)
        spinner.setFixedHeight(10)
        spinner.setObjectName("Spinner")

        # 居中
        spinner_wrap = QWidget()
        wrap_layout = QVBoxLayout(spinner_wrap)
        wrap_layout.setContentsMargins(0, 0, 0, 0)
        wrap_layout.setAlignment(Qt.AlignCenter)
        wrap_layout.addWidget(spinner)

        root.addWidget(spinner_wrap)
        root.addSpacing(14)

        # ===== 文案 =====
        text = QLabel("Loading")
        text.setAlignment(Qt.AlignCenter)
        text_font = QFont()
        text_font.setPointSize(14)
        text.setFont(text_font)
        text.setObjectName("Hint")
        root.addWidget(text)

        root.addStretch(9)

        # ===== 样式：白底 + 轻灰文字 + 小黄进度条（像图里一样）=====
        self.setStyleSheet("""
            #LaunchingPage {
                background: white;
            }
            #Hint {
                color: rgba(0,0,0,0.40);
                letter-spacing: 1px;
            }

            /* 让进度条更像小圆圈/小条，颜色偏黄绿 */
            QProgressBar#Spinner {
                border: none;
                background: rgba(0,0,0,0.06);
                border-radius: 5px;
            }
            QProgressBar#Spinner::chunk {
                border-radius: 5px;
                background: #C9B84A;
            }
        """)
