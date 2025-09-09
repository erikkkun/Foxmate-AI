from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

class WorkshopPage(QWidget):
    def __init__(self):
        super().__init__()
        title = QLabel("Workshop")
        title.setStyleSheet("font-size:22px;font-weight:800;")
        listw = QListWidget()
        listw.addItems(["How to stay focused", "Pomodoro 101", "Deep Work Tips"])  # 占位
        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(listw)
        layout.addStretch()
