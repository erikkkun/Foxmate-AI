# frontend/pages/dress_up_preview.py
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class DressUpPreviewPage(QWidget):
    def __init__(self, on_back=None):
        super().__init__()
        self.setObjectName("DressUpPreviewPage")
        self.setAttribute(Qt.WA_StyledBackground, True)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(12)

        # ===== Top bar (only back button) =====
        top = QHBoxLayout()
        top.setSpacing(10)

        btn_back = QPushButton("←")
        btn_back.setObjectName("backBtn")
        btn_back.setCursor(Qt.PointingHandCursor)
        if on_back:
            btn_back.clicked.connect(on_back)

        top.addWidget(btn_back, 0, Qt.AlignLeft)
        top.addStretch(1)

        root.addLayout(top)

        # ===== Image =====
        self.img = QLabel()
        self.img.setObjectName("previewImg")
        self.img.setAlignment(Qt.AlignCenter)

        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        # 你把截图保存成这个名字（建议：dress_up_preview.png）
        img_path = assets_dir / "dress_up_preview.png"

        pm = QPixmap(str(img_path)) if img_path.exists() else QPixmap()
        if pm.isNull():
            self.img.setText("⚠️ dress_up_preview.png not found in frontend/assets/")
            self.img.setStyleSheet("color: rgba(0,0,0,0.70); font-size: 16px;")
        else:
            # 先存原图，resizeEvent里自适应缩放
            self._pm = pm
            self._apply_scaled()

        root.addWidget(self.img, 1)

        # ===== Style =====
        self.setStyleSheet("""
        QWidget#DressUpPreviewPage {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFF6E8,
                stop:0.45 #FBE7CF,
                stop:0.85 #F6D5A8,
                stop:1 #F3C98D
            );
        }
        QPushButton#backBtn {
            width: 46px; height: 46px;
            border-radius: 16px;
            border: none;
            background: rgba(255,255,255,0.75);
            color: #F39A2D;
            font-size: 22px;
            font-weight: 700;
        }
        QPushButton#backBtn:hover {
            background: rgba(255,255,255,0.92);
        }
        QLabel#previewImg {
            background: transparent;
        }
        """)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._apply_scaled()

    def _apply_scaled(self):
        if not hasattr(self, "_pm") or self._pm.isNull():
            return
        # 适配屏幕，保留边距
        w = max(10, self.width() - 36)
        h = max(10, self.height() - 90)
        scaled = self._pm.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img.setPixmap(scaled)
