# frontend/pages/welcome.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from pathlib import Path

class WelcomePage(QWidget):
    """
    极简启动页（参考百度/虎扑）
    - 白色或浅色渐变背景
    - 中间显示 slogan（颜色足够深）
    - 底部显示 logo + 品牌信息
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("WelcomePage")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 26)
        root.setSpacing(0)

        # ===== 中间 slogan 区 =====
        root.addStretch(4)

        center = QVBoxLayout()
        center.setSpacing(6)

        # 你可以在这里改成你的文案（两行更像你图里的效果）
        line1 = QLabel("FocusMate")
        line2 = QLabel("Fox it!")

        f1 = QFont()
        f1.setPointSize(34)
        f1.setWeight(QFont.DemiBold)

        f2 = QFont()
        f2.setPointSize(34)
        f2.setWeight(QFont.DemiBold)

        line1.setFont(f1)
        line2.setFont(f2)

        line1.setAlignment(Qt.AlignCenter)
        line2.setAlignment(Qt.AlignCenter)

        line1.setObjectName("Slogan1")
        line2.setObjectName("Slogan2")

        center.addWidget(line1)
        center.addWidget(line2)

        # 如果你只想要一行，把 line2 注释掉即可
        wrapper = QWidget()
        wrapper.setLayout(center)
        root.addWidget(wrapper)

        root.addStretch(5)

        # ===== 底部 logo 区（像虎扑那种）=====
        bottom = QVBoxLayout()
        bottom.setSpacing(8)

        logo_row = QHBoxLayout()
        logo_row.setSpacing(10)
        logo_row.setAlignment(Qt.AlignCenter)

        logo = QLabel()
        logo.setObjectName("Logo")

        # 推荐你放一个logo到：frontend/assets/logo.png
        # 没有也没关系，会自动隐藏
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        logo_path = assets_dir / "logo.png"   # 你可以改名字，比如 welcome_logo.png
        if logo_path.exists():
            pm = QPixmap(str(logo_path))
            pm = pm.scaled(44, 44, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pm)
        else:
            logo.hide()

        app_name = QLabel("FocusMate")
        app_name.setObjectName("BrandName")
        app_font = QFont()
        app_font.setPointSize(18)
        app_font.setWeight(QFont.DemiBold)
        app_name.setFont(app_font)

        logo_row.addWidget(logo)
        logo_row.addWidget(app_name)

        footer = QLabel("Proudly presented by FoxMate Team")
        footer.setObjectName("Footer")
        footer.setAlignment(Qt.AlignCenter)

        bottom.addLayout(logo_row)
        bottom.addWidget(footer)

        bottom_wrap = QWidget()
        bottom_wrap.setLayout(bottom)
        root.addWidget(bottom_wrap)

        # ===== 样式（重点：字颜色要深，清晰可见）=====
        self.setStyleSheet("""
            #WelcomePage {
                /* 白底 + 非常轻的冷色渐变，类似你图的柔和氛围 */
                background: qradialgradient(
                    cx:0.5, cy:0.25, radius:0.9,
                    stop:0 rgba(220, 245, 255, 0.75),
                    stop:0.55 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(255, 255, 255, 1.0)
                );
            }

            /* 两行不同颜色（像百度那种双色手写感）——但颜色要够深 */
            #Slogan1 { color: #1D4ED8; }   /* 深蓝 */
            #Slogan2 { color: #7C3AED; }   /* 深紫 */

            #BrandName { color: rgba(0,0,0,0.80); }
            #Footer { color: rgba(0,0,0,0.38); font-size: 12px; }
        """)
