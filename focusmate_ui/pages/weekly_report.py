from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame

class Card(QFrame):
    def __init__(self, title:str, content:str=""):
        super().__init__()
        self.setStyleSheet("QFrame{border:1px solid #e5e7eb;border-radius:12px;padding:12px;}")
        v = QVBoxLayout(self)
        t = QLabel(f"<b>{title}</b>")
        v.addWidget(t)
        v.addWidget(QLabel(content))

class WeeklyReportPage(QWidget):
    def __init__(self):
        super().__init__()
        head = QLabel("Weekly Report")
        head.setStyleSheet("font-size:22px;font-weight:800;")

        # 上：四块区域（Your Last Study Report、Your Last Week Stats、Plan for Next Week、Concentration Data）
        row1 = QHBoxLayout()
        row1.addWidget(Card("Your Last Study Report", "…占位"))
        row1.addWidget(Card("Your Last Week Stats", "…占位"))
        row1.addWidget(Card("Plan for Next Week", "…占位"))
        row1.addWidget(Card("Concentration Data", "…占位"))

        # 下：右侧是折线图占位
        row2 = QHBoxLayout()
        row2.addWidget(Card("AI Notes / Redeem（占位）", "上传/兑换区"))
        row2.addWidget(Card("Concentration Tracking（占位图）", "x轴:时间(5/10/20/30min)\ny轴:专注度(40-100)"))

        layout = QVBoxLayout(self)
        layout.addWidget(head)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addStretch()
