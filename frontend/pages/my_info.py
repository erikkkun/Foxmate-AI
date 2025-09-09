from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QBrush


class MyInfoPage(QWidget):
    def __init__(self, user_data=None, on_logout=None, on_menu=None, on_settings=None, on_close=None):
        super().__init__()
        self.on_logout = on_logout

        # 默认数据（未登录）
        self.user_data = user_data or {
            "username": " ",
            "email": " ",
            "telephone": " ",
            "school": " ",
            "password": " "
        }

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # ===== 顶部 bar =====
        top = QHBoxLayout()
        self._add_top_btn(top, "≡", on_menu)
        top.addStretch()
        self._add_top_btn(top, "⚙", on_settings)
        self._add_top_btn(top, "✕", on_close)
        root.addLayout(top)

        # ===== Title =====
        title = QLabel("My Account")
        title.setStyleSheet("color:white; font-size:24px; font-weight:700;")
        root.addWidget(title, alignment=Qt.AlignHCenter)

        # ===== 信息行（保存 QLabel 引用，方便刷新） =====
        self.lbl_username = QLabel(self.user_data["username"])
        self.lbl_email = QLabel(self.user_data["email"])
        self.lbl_telephone = QLabel(self.user_data["telephone"])
        self.lbl_school = QLabel(self.user_data["school"])
        self.lbl_password = QLabel("•" * len(self.user_data["password"]))

        root.addLayout(self._make_row("Username", self.lbl_username, "Edit"))
        root.addLayout(self._make_row("Email", self.lbl_email, "Edit"))
        root.addLayout(self._make_row("Telephone", self.lbl_telephone, "Edit"))
        root.addLayout(self._make_row("School", self.lbl_school, "Edit"))
        root.addLayout(self._make_row("Password", self.lbl_password, "Change"))

        root.addStretch()

        # ===== Logout 按钮 =====
        btn_logout = QPushButton("Log Out")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.15);
                color: white;
                font-size: 18px;
                font-weight:600;
                border: none;
                border-radius: 14px;
                padding: 10px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.25); }
        """)
        btn_logout.clicked.connect(self._handle_logout)
        root.addWidget(btn_logout)

    # ===== 更新用户数据 =====
    def update_user_data(self, new_data):
        self.user_data = new_data
        self.lbl_username.setText(self.user_data.get("username", " "))
        self.lbl_email.setText(self.user_data.get("email", " "))
        self.lbl_telephone.setText(self.user_data.get("telephone", " "))
        self.lbl_school.setText(self.user_data.get("school", " "))
        self.lbl_password.setText("•" * len(self.user_data.get("password", "")))

    # ===== 信息行生成 =====
    def _make_row(self, label_text, val_label, btn_text):
        row = QHBoxLayout()

        lbl = QLabel(f"{label_text}:")
        lbl.setStyleSheet("color:white; font-size:16px;")

        val_label.setStyleSheet("color:white; font-size:16px;")

        row.addWidget(lbl, alignment=Qt.AlignLeft)
        row.addWidget(val_label, alignment=Qt.AlignLeft)
        row.addStretch()

        btn = QPushButton(btn_text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: #075985;
                color:white;
                border:none;
                border-radius:12px;
                padding:6px 12px;
                font-weight:600;
            }
            QPushButton:hover { background:#0c4a6e; }
        """)
        row.addWidget(btn, alignment=Qt.AlignRight)
        return row

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

    def _handle_logout(self):
        print("Logging out...")
        if self.on_logout:
            self.on_logout()

    def paintEvent(self, e):
        """背景渐变"""
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        g = QLinearGradient(0, 0, 0, self.height())
        g.setColorAt(0.0, QColor("#0c7a7f"))
        g.setColorAt(1.0, QColor("#19b2a0"))
        p.fillRect(self.rect(), QBrush(g))
        super().paintEvent(e)
