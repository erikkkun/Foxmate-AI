# frontend/pages/home.py
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QMovie, QFont, QPixmap
class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(e)


class HomePage(QWidget):
    def _go_dressup(self):
        cb = getattr(self, "on_go_dressup", None)
        if callable(cb):
            cb()
    def __init__(
        self,
        on_menu,
        on_settings,
        on_close,
        on_go_fox,
        on_go_weekly,
        on_fox_it,
        on_go_dressup=None,   # ✅ 关键：加上这个参数，避免 unexpected keyword
    ):
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
        self.on_go_dressup = on_go_dressup  # ✅ 保存回调
        self.on_signin = None

        assets_dir = Path(__file__).resolve().parent.parent / "assets"

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

        # ===== Hero =====
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

        # ===== Fox sticker overlay =====
        self.fox_sticker = QLabel(self.hero)
        self.fox_sticker.setObjectName("foxSticker")
        self.fox_sticker.setAttribute(Qt.WA_TransparentForMouseEvents)

        sticker_candidates = [
            assets_dir / "fox_sticker.png",
            assets_dir / "fox_sticker.jpg",
            assets_dir / "fox_sticker.webp",
        ]
        self._fox_pixmap = None
        for p in sticker_candidates:
            if p.exists():
                pm = QPixmap(str(p))
                if not pm.isNull():
                    self._fox_pixmap = pm
                    break

        if self._fox_pixmap:
            self.fox_sticker.setPixmap(self._fox_pixmap)
            self.fox_sticker.setScaledContents(True)
        else:
            self.fox_sticker.setText("🦊")
            self.fox_sticker.setAlignment(Qt.AlignCenter)

        root.addWidget(self.hero)

        root.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # =========================
        # ===== Bottom card =====
        # =========================
        self.card = QFrame()
        self.card.setObjectName("bottomCard")
        self.card.setMinimumHeight(150)

        from PySide6.QtWidgets import QGridLayout
        grid = QGridLayout(self.card)
        grid.setContentsMargins(18, 16, 18, 16)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        # 标题：左上
        self.lbl_title = QLabel("Your Fox")
        self.lbl_title.setObjectName("cardTitle")
        grid.addWidget(self.lbl_title, 0, 0, 1, 2, alignment=Qt.AlignLeft | Qt.AlignTop)

        # GIF：左下（可点击）
        self.lbl_fox = ClickableLabel()
        self.lbl_fox.setObjectName("foxGif")
        self.lbl_fox.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.lbl_fox.clicked.connect(self._go_dressup)

        gif_candidates = [
            assets_dir / "fox_icon.gif",   # ✅ 你说你用这个
            assets_dir / "weekly_fox.gif",
            assets_dir / "fox_anim.gif",
        ]
        self._fox_movie = None
        for gp in gif_candidates:
            if gp.exists():
                mv = QMovie(str(gp))
                if mv.isValid():
                    self._fox_movie = mv
                    break

        gif_size = 140
        self.lbl_fox.setFixedSize(gif_size, gif_size)

        if self._fox_movie:
            self._fox_movie.setScaledSize(QSize(gif_size, gif_size))
            self.lbl_fox.setMovie(self._fox_movie)
            self._fox_movie.start()
        else:
            self.lbl_fox.setText("🦊")

        grid.addWidget(self.lbl_fox, 1, 0, alignment=Qt.AlignLeft | Qt.AlignBottom)

        # Weekly Report：右下
        self.btn_weekly = QPushButton("Weekly Report")
        self.btn_weekly.setObjectName("weeklyBtn")
        self.btn_weekly.setCursor(Qt.PointingHandCursor)
        self.btn_weekly.clicked.connect(self.on_go_weekly)
        grid.addWidget(self.btn_weekly, 1, 1, alignment=Qt.AlignRight | Qt.AlignBottom)

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)

        card_shadow = QGraphicsDropShadowEffect(self.card)
        card_shadow.setBlurRadius(26)
        card_shadow.setOffset(0, 10)
        card_shadow.setColor(Qt.black)
        self.card.setGraphicsEffect(card_shadow)

        root.addWidget(self.card)

        # ===== Styles =====
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

        QPushButton#menuBtn {
            width: 46px; height: 46px;
            border-radius: 23px;
            border: none;
            background: #F39A2D;
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

        QPushButton#powerBtn {
            border-radius: 145px;
            border: 10px solid #F39A2D;
            background: #214F3D;
            color: #F6EAD3;
        }
        QPushButton#powerBtn:hover { background: #1E4738; }
        QPushButton#powerBtn:pressed { background: #193D30; }

        QLabel#subtitle {
            color: rgba(0,0,0,0.70);
            font-size: 14px;
            letter-spacing: 0.6px;
        }

        QFrame#bottomCard {
    background: transparent;     /* ✅ 去掉灰底 */
    border: none;                /* ✅ 去掉边框线 */
}

        QLabel#cardTitle {
            color: #1C5B45;
            font-size: 22px;
            font-weight: 700;
        }

        QLabel#foxGif {
            background: transparent;
            border: none;
        }

        QPushButton#weeklyBtn {
    padding: 16px 22px;                 /* ✅ 更大 */
    border-radius: 20px;
    border: 1px solid rgba(28, 91, 69, 0.18);
    background: rgba(179, 227, 211, 0.78);
    color: #214F3D;
    font-size: 20px;                    /* ✅ 字更大 */
    font-weight: 700;
    min-width: 180px;                   /* ✅ 更宽 */
    min-height: 50px;                   /* ✅ 更高 */
}
QPushButton#weeklyBtn:hover {
    background: rgba(179, 227, 211, 0.95);
}

        QLabel#foxSticker {
            color: #F39A2D;
            font-size: 72px;
            background: transparent;
        }
        """)

        self._layout_fox()

    def _go_dressup(self):
        cb = getattr(self, "on_go_dressup", None)
        if callable(cb):
            cb()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._layout_fox()

    def _layout_fox(self):
        if not self.hero or not self.btn_power:
            return

        btn_geo = self.btn_power.geometry()

        w, h = 240, 240
        self.fox_sticker.setFixedSize(w, h)

        if self._fox_pixmap:
            pm = self._fox_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.fox_sticker.setPixmap(pm)
            self.fox_sticker.setScaledContents(False)

        x = btn_geo.x() + btn_geo.width() - int(w * 0.72) + 10
        y = btn_geo.y() + btn_geo.height() - int(h * 0.78) + 10
        self.fox_sticker.move(x, y)

    def update_login_ui(self, logged_in: bool, username: str, membership: str):
        self.btn_signin.setText(username if logged_in else "Sign In")

    def _handle_signin_clicked(self):
        if callable(self.on_signin):
            self.on_signin()
