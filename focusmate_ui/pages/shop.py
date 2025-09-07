from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

class ShopPage(QWidget):
    def __init__(self):
        super().__init__()
        title = QLabel("Shop")
        title.setStyleSheet("font-size:22px;font-weight:800;")
        listw = QListWidget()
        listw.addItems(["Theme Pack", "Icon Pack", "Focus Alarm", "Sticker Set"])  # 占位
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(listw)
        layout.addStretch()
