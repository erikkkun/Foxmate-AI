from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMessageBox



class SignInDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setFixedSize(360, 420)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setStyleSheet("""
        QDialog {
            background: qlineargradient(x1:0,y1:0, x2:0,y2:1,
                stop:0 #0c7a7f, stop:1 #19b2a0);
            border: 2px solid rgba(255,255,255,0.6);
            border-radius: 0px;   
        }
        QLabel { color: white; }
        QLineEdit {
            background: rgba(255,255,255,0.8);
            border: none;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }
        QPushButton {
            background: qlineargradient(x1:0,y1:0, x2:0,y2:1,
                stop:0 #34d399, stop:1 #059669);
            color: white; font-weight:600;
            border-radius: 8px; padding: 10px;
        }
        QPushButton:hover { background: #047857; }
    """)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Sign In")
        title.setFont(QFont("", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.username)
        layout.addWidget(self.password)

        btn_signin = QPushButton("Sign In")
        btn_signin.clicked.connect(self.try_login)

        layout.addWidget(btn_signin)

        # 关闭按钮
        close_row = QHBoxLayout()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32,32)
        close_btn.setStyleSheet("QPushButton{background:transparent; font-size:18px;}")
        close_btn.clicked.connect(self.reject)
        close_row.addStretch()
        close_row.addWidget(close_btn)
        layout.addLayout(close_row)
        
        # 居中到父窗口
        if parent:
            geo = parent.frameGeometry()
            self.move(geo.center() - self.rect().center())


    
    
    def try_login(self):
        user = self.username.text().strip()
        pwd = self.password.text().strip()
        if user == "Test" and pwd == "123":
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.\n(Use Test / 123)")