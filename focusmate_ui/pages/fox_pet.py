from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class FoxPetPage(QWidget):
    def __init__(self):
        super().__init__()
        title = QLabel("Your Fox")
        title.setStyleSheet("font-size:22px;font-weight:800;")

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(QLabel("🦊 Fox 状态：开心（占位）"))
        row = QHBoxLayout()
        row.addWidget(QPushButton("喂食（占位）"))
        row.addWidget(QPushButton("训练（占位）"))
        row.addWidget(QPushButton("更名（占位）"))
        layout.addLayout(row)
        layout.addStretch()
