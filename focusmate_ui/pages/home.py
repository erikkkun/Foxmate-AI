from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QBrush, QPixmap
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtWidgets import QGraphicsDropShadowEffect

APP_DIR = Path(__file__).resolve().parents[1]
ASSETS = APP_DIR / "assets"


class HomePage(QWidget):
    def __init__(self, on_menu, on_settings, on_close, on_go_fox, on_go_weekly, on_fox_it):
        super().__init__()
        self.on_menu = on_menu
        self.on_settings = on_settings
        self.on_close = on_close
        self.on_go_fox = on_go_fox
        self.on_go_weekly = on_go_weekly
        self.on_fox_it = on_fox_it

        self.logged_in = False   # 登录状态

        # ========== 顶部按钮 ==========
        top = QHBoxLayout()
        self.btn_menu = self._icon_btn("≡");   self.btn_menu.clicked.connect(self.on_menu)
        self.btn_signin = QPushButton("Sign In")
        self.btn_signin.setFixedSize(72, 32)
        self.btn_signin.setCursor(Qt.PointingHandCursor)
        self.btn_signin.setStyleSheet("""
            QPushButton {
                color: #fff; font-size:14px; font-weight:600;
                border:1px solid rgba(255,255,255,0.6);
                border-radius: 6px; background: transparent;
            }
            QPushButton:hover { background: rgba(255,255,255,0.15); }
        """)
        self.btn_signin.clicked.connect(lambda: self.on_signin() if hasattr(self, "on_signin") else None)

        self.btn_settings = self._icon_btn("⚙"); self.btn_settings.clicked.connect(self.on_settings)
        self.btn_close = self._icon_btn("✕");    self.btn_close.clicked.connect(self.on_close)

        top.addWidget(self.btn_menu)
        top.addStretch()
        top.addWidget(self.btn_signin)   # Sign In 默认显示
        top.addWidget(self.btn_settings)
        top.addWidget(self.btn_close)

        # ========== 用户信息（默认隐藏） ==========
        self.avatar = QLabel()
        self.avatar.setFixedSize(84, 84)
        self.avatar.setStyleSheet("""
            QLabel{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #b2f5ea, stop:1 #7ee0d6);
                border-radius: 42px; border: 2px solid rgba(0,0,0,0.18);
            }
        """)
        a_shadow = QGraphicsDropShadowEffect(self)
        a_shadow.setBlurRadius(20)
        a_shadow.setOffset(0, 2)
        a_shadow.setColor(QColor(0, 0, 0, 60))
        self.avatar.setGraphicsEffect(a_shadow)

        self.username = QLabel("Username")
        self.username.setStyleSheet("color:#fff; font-size:26px; font-weight:800;")
        self.membership = QLabel("Membership Status: White Fox")
        self.membership.setStyleSheet("color:rgba(255,255,255,0.9);")

        self.user_block = QVBoxLayout()
        self.user_block.setSpacing(6)
        self.user_block.setAlignment(Qt.AlignHCenter)
        self.user_block.addWidget(self.avatar, alignment=Qt.AlignHCenter)
        self.user_block.addWidget(self.username, alignment=Qt.AlignHCenter)
        self.user_block.addWidget(self.membership, alignment=Qt.AlignHCenter)

        # 默认隐藏用户信息
        self.avatar.hide()
        self.username.hide()
        self.membership.hide()

        # ========== 中部 Fox it! 按钮 ==========
        self.btn_foxit = QPushButton("Fox it!")
        self.btn_foxit.setCursor(Qt.PointingHandCursor)
        self.btn_foxit.setStyleSheet("""
            QPushButton {
                color:#0f172a; font-size:30px; font-weight:800;
                border-radius:110px; border:2px solid rgba(0,0,0,0.18);
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #69F0DF, stop:1 #7CE0CF);
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.btn_foxit.setGraphicsEffect(shadow)

        self.btn_foxit.clicked.connect(self.on_fox_it)
        self.btn_foxit.pressed.connect(self._press_anim)
        self.btn_foxit.released.connect(self._release_anim)

        center = QVBoxLayout()
        center.addStretch(1)
        center.addWidget(self.btn_foxit, alignment=Qt.AlignHCenter)
        center.addStretch(1)

        # ========== 底部 Fox 卡片 ==========
        card = QFrame(); card.setObjectName("foxCard")
        card.setStyleSheet("""
            QFrame#foxCard { background: rgba(0,0,0,0.18); border-radius:20px; }
            QLabel.title { color:white; font-size:20px; font-weight:700; }
            QPushButton.pill {
                background: rgba(0,0,0,0.28); color:white; border:none; border-radius:16px;
                padding:10px 14px; font-size:16px; font-weight:600;
            }
            QPushButton.pill:hover { background: rgba(0,0,0,0.35); }
        """)
        card_lay = QHBoxLayout(card)

        fox_img = ASSETS / "fox.png"
        if fox_img.exists():
            fox = QLabel(); fox.setPixmap(QPixmap(str(fox_img)).scaled(86, 86, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            fox = QLabel("🦊"); fox.setStyleSheet("font-size:48px; color:white;")
        card.mousePressEvent = lambda e: self.on_go_fox()

        text_col = QVBoxLayout()
        t1 = QLabel("Your Fox"); t1.setProperty("class","title"); text_col.addWidget(t1)
        btn_weekly = QPushButton("Weekly Report"); btn_weekly.setProperty("class","pill")
        btn_weekly.setCursor(Qt.PointingHandCursor); btn_weekly.clicked.connect(self.on_go_weekly)
        text_col.addWidget(btn_weekly); text_col.addStretch()

        card_lay.addWidget(fox); card_lay.addSpacing(8); card_lay.addLayout(text_col); card_lay.addStretch()
        card.setFixedHeight(130)

        # ========== 主布局 ==========
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 12, 16, 16)
        root.setSpacing(8)
        root.addLayout(top)
        root.addLayout(self.user_block)
        root.addLayout(center, 1)
        root.addWidget(card)

    # ---------- 工具方法 ----------
    def _icon_btn(self, txt):
        b = QPushButton(txt)
        b.setFixedSize(32, 32)
        b.setCursor(Qt.PointingHandCursor)
        b.setStyleSheet("""
            QPushButton { color:#fff; font-size:20px; border:none; background:transparent; }
            QPushButton:hover { background: rgba(255,255,255,0.12); border-radius:8px; }
        """)
        return b

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)

    def resizeEvent(self, e):
        d = int(min(self.width(), self.height()) * 0.38)
        d = max(180, min(d, 260))
        self.btn_foxit.setFixedSize(d, d)
        self.btn_foxit.setStyleSheet(self.btn_foxit.styleSheet().replace("border-radius:110px", f"border-radius:{d//2}px"))
        return super().resizeEvent(e)

    # ---------- 动画 ----------
    def _press_anim(self):
        self._foxit_rect_before_press = self.btn_foxit.geometry()
        r = self._foxit_rect_before_press
        shrink = max(2, int(r.width() * 0.04))
        end = QRect(r.x() + shrink, r.y() + shrink, r.width() - 2*shrink, r.height() - 2*shrink)

        self._anim_foxit = QPropertyAnimation(self.btn_foxit, b"geometry", self)
        self._anim_foxit.setDuration(90)
        self._anim_foxit.setEasingCurve(QEasingCurve.OutCubic)
        self._anim_foxit.setStartValue(r)
        self._anim_foxit.setEndValue(end)
        self._anim_foxit.start()

    def _release_anim(self):
        if not hasattr(self, "_foxit_rect_before_press"):
            return
        r0 = self._foxit_rect_before_press
        r = self.btn_foxit.geometry()

        self._anim_foxit = QPropertyAnimation(self.btn_foxit, b"geometry", self)
        self._anim_foxit.setDuration(120)
        self._anim_foxit.setEasingCurve(QEasingCurve.OutBack)
        self._anim_foxit.setStartValue(r)
        self._anim_foxit.setEndValue(r0)
        self._anim_foxit.start()

    # ---------- 登录状态切换 ----------
    def update_login_ui(self, logged_in: bool, username=None, membership=None):
        self.logged_in = logged_in
        if logged_in:
            self.btn_signin.hide()
            self.avatar.show()
            self.username.setText(username or "Username")
            self.username.show()
            self.membership.setText(membership or "Membership Status: White Fox")
            self.membership.show()
        else:
            self.btn_signin.show()
            self.avatar.hide()
            self.username.hide()
            self.membership.hide()
