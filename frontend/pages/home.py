# frontend/pages/home.py
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPixmap


class HomePage(QWidget):
    """
    Warm style home page (match mock #1):
    - Warm beige gradient background
    - Big dark-green circle with orange rim
    - Fox sticker overlapping bottom-right of circle
    - Bottom creamy card + Weekly Report button
    """

    def __init__(self, on_menu, on_settings, on_close, on_go_fox, on_go_weekly, on_fox_it):
        super().__init__()
        self.setObjectName("HomePage")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.on_menu = on_menu
        self.on_settings = on_settings
        self.on_close = on_close
        self.on_go_fox = on_go_fox
        self.on_go_weekly = on_go_weekly
        self.on_fox_it = on_fox_it

        # allow app.py assign later: home.on_signin = ...
        self.on_signin = None

        # ===== Root layout =====
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(14)

        # ===== Top bar =====
        top = QHBoxLayout()
        top.setSpacing(10)

        self.btn_menu = QPushButton("☰")
        self.btn_menu.setObjectName("menuBtn")
        self.btn_menu.setCursor(Qt.PointingHandCursor)
        self.btn_menu.clicked.connect(self.on_menu)

        top.addWidget(self.btn_menu, 0, Qt.AlignLeft)
        top.addStretch(1)

        self.btn_signin = QPushButton("Sign In")
        self.btn_signin.setObjectName("signinBtn")
        self.btn_signin.setCursor(Qt.PointingHandCursor)
        self.btn_signin.clicked.connect(self._handle_signin_clicked)
        top.addWidget(self.btn_signin, 0, Qt.AlignRight)

        self.btn_settings = QPushButton("⚙")
        self.btn_settings.setObjectName("settingsBtn")
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_settings.clicked.connect(self.on_settings)
        top.addWidget(self.btn_settings, 0, Qt.AlignRight)

        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("closeBtn")
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.clicked.connect(self.on_close)
        top.addWidget(self.btn_close, 0, Qt.AlignRight)

        root.addLayout(top)

        # ===== Hero area (circle + subtitle + fox sticker overlay) =====
        root.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.hero = QFrame()
        self.hero.setObjectName("hero")
        self.hero.setMinimumHeight(360)
        hero_layout = QVBoxLayout(self.hero)
        hero_layout.setContentsMargins(0, 0, 0, 0)
        hero_layout.setSpacing(10)
        hero_layout.setAlignment(Qt.AlignHCenter)

        self.btn_power = QPushButton("Fox it!")
        self.btn_power.setObjectName("powerBtn")
        self.btn_power.setCursor(Qt.PointingHandCursor)
        self.btn_power.setFixedSize(290, 290)
        self.btn_power.clicked.connect(self.on_fox_it)

        f_btn = QFont()
        f_btn.setPointSize(28)
        f_btn.setWeight(QFont.DemiBold)
        self.btn_power.setFont(f_btn)

        # subtle shadow for the big circle
        shadow = QGraphicsDropShadowEffect(self.btn_power)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 10)
        shadow.setColor(Qt.black)
        self.btn_power.setGraphicsEffect(shadow)

        self.lbl_sub = QLabel("Let's focus together")
        self.lbl_sub.setObjectName("subtitle")
        self.lbl_sub.setAlignment(Qt.AlignCenter)

        hero_layout.addWidget(self.btn_power, 0, Qt.AlignHCenter)
        hero_layout.addWidget(self.lbl_sub, 0, Qt.AlignHCenter)

        # fox sticker overlay (absolute-positioned inside hero)
        self.fox_sticker = QLabel(self.hero)
        self.fox_sticker.setObjectName("foxSticker")
        self.fox_sticker.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Try load fox image if exists: frontend/assets/fox_sticker.png (or .jpg)
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        candidates = [
            assets_dir / "fox_sticker.png",
            assets_dir / "fox_sticker.jpg",
            assets_dir / "fox_sticker.webp",
        ]
        self._fox_pixmap = None
        for p in candidates:
            if p.exists():
                pm = QPixmap(str(p))
                if not pm.isNull():
                    self._fox_pixmap = pm
                    break

        if self._fox_pixmap:
            # scale later in _layout_fox()
            self.fox_sticker.setPixmap(self._fox_pixmap)
            self.fox_sticker.setScaledContents(True)
        else:
            # fallback
            self.fox_sticker.setText("🦊")
            self.fox_sticker.setAlignment(Qt.AlignCenter)

        root.addWidget(self.hero)

        root.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # ===== Bottom card =====
        self.card = QFrame()
        self.card.setObjectName("bottomCard")
        card_layout = QHBoxLayout(self.card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(12)

        self.lbl_fox = QLabel()
        self.lbl_fox.setObjectName("foxIcon")
        self.lbl_fox.setFixedSize(46, 46)
        self.lbl_fox.setAlignment(Qt.AlignCenter)

        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        icon_candidates = [
            assets_dir / "fox_icon.png",
            assets_dir / "fox_icon.jpg",
            assets_dir / "fox_icon.webp",
        ]
        pm = None
        for p in icon_candidates:
            if p.exists():
                t = QPixmap(str(p))
                if not t.isNull():
                    pm = t
                    break

        if pm:
            self.lbl_fox.setPixmap(pm.scaled(
                46, 46,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            ))
            self.lbl_fox.setScaledContents(True)
        else:
            self.lbl_fox.setText("🦊")

        right = QVBoxLayout()
        right.setSpacing(6)

        self.lbl_title = QLabel("Your Fox")
        self.lbl_title.setObjectName("cardTitle")

        self.btn_weekly = QPushButton("Weekly Report")
        self.btn_weekly.setObjectName("weeklyBtn")
        self.btn_weekly.setCursor(Qt.PointingHandCursor)
        self.btn_weekly.clicked.connect(self.on_go_weekly)

        right.addWidget(self.lbl_title)
        right.addWidget(self.btn_weekly, 0, Qt.AlignLeft)

        card_layout.addWidget(self.lbl_fox)
        card_layout.addLayout(right)
        card_layout.addStretch(1)

        # card shadow
        card_shadow = QGraphicsDropShadowEffect(self.card)
        card_shadow.setBlurRadius(26)
        card_shadow.setOffset(0, 10)
        card_shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(card_shadow)

        root.addWidget(self.card)

        # ===== Styles (match mock #1) =====
        self.setStyleSheet("""
        QWidget#HomePage {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFF6E8,
        stop:0.45 #FBE7CF,
        stop:0.85 #F6D5A8,
        stop:1 #F3C98D
    );
}

        /* Top buttons */
        QPushButton#menuBtn {
            width: 46px; height: 46px;
            border-radius: 23px;
            border: none;
            background: #F39A2D;  /* orange */
            color: white;
            font-size: 18px;
        }
        QPushButton#menuBtn:hover { background: #F6A94A; }

        QPushButton#signinBtn {
            padding: 10px 18px;
            border-radius: 16px;
            border: 2px solid rgba(243, 154, 45, 0.70);
            background: rgba(255,255,255,0.75);
            color: #1C5B45;
            font-size: 16px;
            font-weight: 600;
        }
        QPushButton#signinBtn:hover { background: rgba(255,255,255,0.92); }

        QPushButton#settingsBtn, QPushButton#closeBtn {
            width: 46px; height: 46px;
            border-radius: 16px;
            border: none;
            background: rgba(255,255,255,0.70);
            color: #F39A2D;
            font-size: 18px;
        }
        QPushButton#settingsBtn:hover, QPushButton#closeBtn:hover {
            background: rgba(255,255,255,0.92);
        }

        /* Big circle button */
        QPushButton#powerBtn {
            border-radius: 145px;
            border: 10px solid #F39A2D;    /* orange rim */
            background: #214F3D;          /* deep green */
            color: #F6EAD3;               /* warm off-white */
        }
        QPushButton#powerBtn:hover {
            background: #1E4738;
        }
        QPushButton#powerBtn:pressed {
            background: #193D30;
        }

        QLabel#subtitle {
            color: rgba(255, 245, 232, 0.88);
            font-size: 14px;
            letter-spacing: 0.6px;
        }

        /* bottom card */
        QFrame#bottomCard {
            border-radius: 22px;
            background: rgba(255, 246, 232, 0.86);
            border: 1px solid rgba(0,0,0,0.06);
        }
        QLabel#cardTitle {
            color: #1C5B45;
            font-size: 22px;
            font-weight: 700;
        }
        QLabel#foxIcon {
        background: transparent;
        border: none;
        border-radius: 16px;
        }

        QPushButton#weeklyBtn {
            padding: 10px 14px;
            border-radius: 16px;
            border: 1px solid rgba(28, 91, 69, 0.18);
            background: rgba(179, 227, 211, 0.70); /* mint */
            color: #214F3D;
            font-size: 16px;
            font-weight: 600;
        }
        QPushButton#weeklyBtn:hover {
            background: rgba(179, 227, 211, 0.90);
        }

        /* fox sticker fallback (emoji) */
        QLabel#foxSticker {
            color: #F39A2D;
            font-size: 72px;
        }
        """)

        # initial layout of fox sticker
        self._layout_fox()

    # keep fox overlay pinned to bottom-right of the big circle
    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._layout_fox()

    def _layout_fox(self):
        if not self.hero or not self.btn_power:
            return

        btn_geo = self.btn_power.geometry()

        # 你要多大就改这里：240/260 都行
        w, h = 240, 240

        self.fox_sticker.setFixedSize(w, h)

        # ✅ 关键：按 label 尺寸缩放图片（否则改 w/h 看起来不会变）
        if self._fox_pixmap:
            pm = self._fox_pixmap.scaled(
                w, h,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.fox_sticker.setPixmap(pm)
            self.fox_sticker.setScaledContents(False)  # 我们已经手动缩放了，不需要它

        # 位置：压在圆右下角（你可以微调 0.72 / 0.78）
        x = btn_geo.x() + btn_geo.width() - int(w * 0.72)
        y = btn_geo.y() + btn_geo.height() - int(h * 0.78)
        self.fox_sticker.move(x, y)

    # ===== public API used by app.py =====
    def update_login_ui(self, logged_in: bool, username: str, membership: str):
        self.btn_signin.setText(username if logged_in else "Sign In")

    def _handle_signin_clicked(self):
        if callable(self.on_signin):
            self.on_signin()
