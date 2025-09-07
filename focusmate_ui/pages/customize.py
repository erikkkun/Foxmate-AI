from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox

class CustomizePage(QWidget):
    def __init__(self):
        super().__init__()
        title = QLabel("Customize")
        title.setStyleSheet("font-size:22px;font-weight:800;")

        theme = QComboBox(); theme.addItems(["System", "Light", "Dark"])
        size = QSpinBox(); size.setRange(8, 24); size.setValue(12)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(QLabel("Theme（占位）")); layout.addWidget(theme)
        layout.addWidget(QLabel("Font Size（占位）")); layout.addWidget(size)
        layout.addWidget(QPushButton("Apply（占位）"))
        layout.addStretch()
