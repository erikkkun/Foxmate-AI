# frontend/pages/auth.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AuthPage(QWidget):
    def __init__(self, on_back, on_login_success=None, parent=None):
        super().__init__(parent)
        self.setObjectName("AuthPage")
        self.on_back = on_back
        self.on_login_success = on_login_success  # 回调：登录成功后更新home/myinfo

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(14)

        # ===== Top bar: back + title =====
        top = QHBoxLayout()
        btn_back = QPushButton("←")
        btn_back.setObjectName("TopIcon")
        btn_back.clicked.connect(self.on_back)

        title = QLabel("Account")
        title.setObjectName("TopTitle")
        title.setAlignment(Qt.AlignCenter)

        top.addWidget(btn_back, 0, Qt.AlignLeft)
        top.addStretch(1)
        top.addWidget(title, 0, Qt.AlignCenter)
        top.addStretch(1)
        top.addSpacing(40)  # 右侧占位，让标题居中

        root.addLayout(top)
        root.addStretch(1)

        # ===== Card container =====
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        # toggle row
        toggle = QHBoxLayout()
        self.btn_signin = QPushButton("Sign In")
        self.btn_register = QPushButton("Register")
        self.btn_signin.setObjectName("ToggleActive")
        self.btn_register.setObjectName("ToggleIdle")
        self.btn_signin.clicked.connect(lambda: self._switch(0))
        self.btn_register.clicked.connect(lambda: self._switch(1))
        toggle.addWidget(self.btn_signin)
        toggle.addWidget(self.btn_register)
        card_layout.addLayout(toggle)

        # stacked pages
        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_signin())
        self.stack.addWidget(self._build_register())
        card_layout.addWidget(self.stack)

        root.addWidget(card)
        root.addStretch(2)

        self.setStyleSheet("""
            #AuthPage {
                background: #F6F7F9;
            }
            QPushButton#TopIcon {
                width: 40px; height: 40px;
                border-radius: 12px;
                border: 1px solid rgba(0,0,0,0.10);
                background: rgba(255,255,255,0.85);
                color: rgba(0,0,0,0.80);
                font-size: 18px;
            }
            QLabel#TopTitle {
                color: rgba(0,0,0,0.80);
                font-size: 18px;
                font-weight: 600;
            }
            QFrame#Card {
                border-radius: 18px;
                background: rgba(255,255,255,0.95);
                border: 1px solid rgba(0,0,0,0.08);
            }
            QPushButton#ToggleActive {
                padding: 10px 12px;
                border-radius: 12px;
                border: 1px solid rgba(58, 255, 210, 0.60);
                background: rgba(58, 255, 210, 0.16);
                color: rgba(0,0,0,0.80);
                font-size: 14px;
            }
            QPushButton#ToggleIdle {
                padding: 10px 12px;
                border-radius: 12px;
                border: 1px solid rgba(0,0,0,0.10);
                background: rgba(0,0,0,0.04);
                color: rgba(0,0,0,0.70);
                font-size: 14px;
            }
            QLineEdit {
                padding: 12px 12px;
                border-radius: 12px;
                border: 1px solid rgba(0,0,0,0.12);
                background: rgba(255,255,255,1);
                color: rgba(0,0,0,0.82);
                font-size: 14px;
            }
            QLabel#Hint {
                color: rgba(0,0,0,0.55);
                font-size: 12px;
            }
            QPushButton#Primary {
                padding: 12px 14px;
                border-radius: 14px;
                border: 1px solid rgba(58, 255, 210, 0.70);
                background: rgba(58, 255, 210, 0.22);
                color: rgba(0,0,0,0.82);
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton#Primary:hover {
                background: rgba(58, 255, 210, 0.30);
            }
        """)

    def _switch(self, idx: int):
        self.stack.setCurrentIndex(idx)
        if idx == 0:
            self.btn_signin.setObjectName("ToggleActive")
            self.btn_register.setObjectName("ToggleIdle")
        else:
            self.btn_signin.setObjectName("ToggleIdle")
            self.btn_register.setObjectName("ToggleActive")
        # 让样式立即刷新
        self.btn_signin.style().unpolish(self.btn_signin); self.btn_signin.style().polish(self.btn_signin)
        self.btn_register.style().unpolish(self.btn_register); self.btn_register.style().polish(self.btn_register)

    def _build_signin(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        title = QLabel("Welcome back")
        title.setStyleSheet("color: rgba(0,0,0,0.82); font-size: 20px; font-weight: 700;")
        lay.addWidget(title)

        self.si_user = QLineEdit()
        self.si_user.setPlaceholderText("Username")
        lay.addWidget(self.si_user)

        self.si_pwd = QLineEdit()
        self.si_pwd.setPlaceholderText("Password")
        self.si_pwd.setEchoMode(QLineEdit.Password)
        lay.addWidget(self.si_pwd)

        hint = QLabel("Tip: demo mode accepts any username.")
        hint.setObjectName("Hint")
        lay.addWidget(hint)

        btn = QPushButton("Sign In")
        btn.setObjectName("Primary")
        btn.clicked.connect(self._do_signin)
        lay.addWidget(btn)

        return w

    def _build_register(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)

        title = QLabel("Create account")
        title.setStyleSheet("color: rgba(0,0,0,0.82); font-size: 20px; font-weight: 700;")
        lay.addWidget(title)

        self.re_user = QLineEdit()
        self.re_user.setPlaceholderText("Username")
        lay.addWidget(self.re_user)

        self.re_email = QLineEdit()
        self.re_email.setPlaceholderText("Email (optional)")
        lay.addWidget(self.re_email)

        self.re_pwd = QLineEdit()
        self.re_pwd.setPlaceholderText("Password")
        self.re_pwd.setEchoMode(QLineEdit.Password)
        lay.addWidget(self.re_pwd)

        self.re_pwd2 = QLineEdit()
        self.re_pwd2.setPlaceholderText("Confirm password")
        self.re_pwd2.setEchoMode(QLineEdit.Password)
        lay.addWidget(self.re_pwd2)

        btn = QPushButton("Create Account")
        btn.setObjectName("Primary")
        btn.clicked.connect(self._do_register)
        lay.addWidget(btn)

        return w

    def _do_signin(self):
        username = self.si_user.text().strip()
        if not username:
            username = "Guest"

        # 先做 demo：认为登录成功
        if callable(self.on_login_success):
            self.on_login_success(username=username)
        self.on_back()

    def _do_register(self):
        username = self.re_user.text().strip() or "NewUser"
        # 这里先不做真正数据库校验，先走 demo
        if callable(self.on_login_success):
            self.on_login_success(username=username)
        self.on_back()
