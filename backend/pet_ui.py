# backend/pet_ui.py
import os, math, time
from PySide6.QtWidgets import QWidget, QLabel, QMenu, QProgressBar, QApplication
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QPoint, QTimer

BASE_DIR = os.path.dirname(__file__)
IMG = lambda name: os.path.join(BASE_DIR, "images", name)

# 按区间映射的占位图文件名（放在 backend/images/ 目录）
FOX_FILES = {
    "sleepy":     "fox_sleepy.png",     # 0-19
    "distracted": "fox_distracted.png", # 20-39
    "neutral":    "fox_neutral.png",    # 40-59
    "focus":      "fox_focus.png",      # 60-74
    "energized":  "fox_energized.png",  # 75-89
    "celebrate":  "fox_celebrate.png",  # 90-100
}

def fox_state_for(score: float) -> str:
    s = max(0, min(100, int(round(score))))
    if s <= 19:   return "sleepy"
    if s <= 39:   return "distracted"
    if s <= 59:   return "neutral"
    if s <= 74:   return "focus"
    if s <= 89:   return "energized"
    return "celebrate"

def ease_out_cubic(t: float) -> float:
    """0→1 的缓动曲线（出场更柔和）"""
    # https://easings.net/#easeOutCubic
    return 1 - pow(1 - t, 3)

class FloatingPet(QWidget):
    """
    可拖拽、右键菜单、圆形透明徽章 + 竖直加粗进度条 的小狐狸桌宠。
    支持分数平滑过渡动画：update_by_score(new_score) 会在 ~500ms 内从旧值缓动到新值。
    """
    def __init__(self):
        super().__init__()
        # 无边框、置顶、tool 窗口；透明背景以便不遮挡
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 拖拽状态
        self._drag_active = False
        self._drag_pos = QPoint()
        self._always_on_top = True
        self._progress_visible = True

        # —— 动画状态 —— #
        self._display_score = 0.0         # 当前显示中的分数（动画中的中间值）
        self._anim_from = 0.0
        self._anim_to = 0.0
        self._anim_start_ts = 0.0
        self._anim_duration_ms = 500      # 动画时长（毫秒）
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(16)  # ~60 FPS
        self._anim_timer.timeout.connect(self._on_anim_tick)

        # 狐狸形象
        self.fox = QLabel(self)
        self.fox.setAlignment(Qt.AlignCenter)

        # 圆形分数徽章（透明背景）
        self.badge = QLabel(self)
        self.badge.setAlignment(Qt.AlignCenter)
        self.badge.setStyleSheet("""
            background: white;
            color: black;
            font-size: 18px;
            font-weight: 700;
            font-family: 'Comic Sans MS';    /* change font family */
            font-style: italic;              /* make text italic */
            border: 2px solid #111;
            border-radius: 24px;
        """)
        self.badge.setText("--")
        self.badge.resize(48, 48)  # 圆形尺寸（宽高一致，半径=24）

        # 竖直进度条（0-100）
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setOrientation(Qt.Vertical)   # 竖直
        self.progress.setFixedSize(28, 140)         # 加粗 + 高度
        self.progress.setStyleSheet(self._bar_style("#4caf50"))
        self.progress.show()

        # 初始布局与资源
        self.resize(300, 260)
        self.move(60, 60)
        self._pixmaps = {}
        self._load_pixmaps()
        self._apply_state("neutral")
        self._relayout()

        # 右键菜单
        self.setContextMenuPolicy(Qt.DefaultContextMenu)

    # ---------- 颜色与样式 ----------
    def _bar_style(self, color_hex: str) -> str:
        # 圆角底轨 + 彩色 chunk；适配竖/横
        return f"""
            QProgressBar {{
                background-color: rgba(255,255,255,160);
                border: 1px solid rgba(0,0,0,80);
                border-radius: 8px;
            }}
            QProgressBar::chunk {{
                border-radius: 8px;
                background-color: {color_hex};
            }}
        """

    def _color_for_score(self, score: float) -> str:
        s = int(score)
        if s < 40:   return "#ef5350"   # 红
        if s < 70:   return "#ffa726"   # 橙
        return "#4caf50"                # 绿

    # ---------- 资源加载 ----------
    def _load_pixmaps(self):
        for k, fname in FOX_FILES.items():
            path = IMG(fname)
            pm = QPixmap(path)
            if pm.isNull():
                # 若无素材，用透明像素占位避免崩溃
                pm = QPixmap(1, 1); pm.fill(Qt.transparent)
            self._pixmaps[k] = pm

    def _apply_state(self, state: str):
        pm = self._pixmaps.get(state) or self._pixmaps["neutral"]
        pm_scaled = pm.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.fox.setPixmap(pm_scaled)

    # ---------- 布局 ----------
    def _relayout(self):
        # 狐狸居中略上
        self.fox.resize(200, 200)
        self.fox.move(int((self.width()-200)/2), int((self.height()-200)/2) - 8)

        # 圆形徽章：狐狸右上角稍外侧
        bx = self.fox.x() + self.fox.width() - self.badge.width() + 12
        by = self.fox.y() - 12
        self.badge.move(bx, by)

        # 竖直进度条：徽章正下方，水平居徽章中心线
        px = self.badge.x() + (self.badge.width() - self.progress.width()) // 2
        py = self.badge.y() + self.badge.height() + 6
        self.progress.move(px, py)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._relayout()

    # ---------- 对外接口：根据分数更新（带动画） ----------
    def update_by_score(self, new_score: float):
        # 裁剪 0-100
        new_score = max(0.0, min(100.0, float(new_score)))

        # 如果已有动画在跑，从当前显示值中断并接着往新目标滑
        current = self._display_score
        if not self._anim_timer.isActive():
            # 没动画在跑，就从 progress 当前值开始
            current = float(self.progress.value())
            self._display_score = current

        self._start_anim(current, new_score)

    def _start_anim(self, from_score: float, to_score: float):
        self._anim_from = from_score
        self._anim_to = to_score
        self._anim_start_ts = time.time()
        if not self._anim_timer.isActive():
            self._anim_timer.start()

    def _on_anim_tick(self):
        # 计算 0→1 的进度
        elapsed = (time.time() - self._anim_start_ts) * 1000.0
        t = min(1.0, max(0.0, elapsed / self._anim_duration_ms))
        t_eased = ease_out_cubic(t)

        # 当前显示值
        val = self._anim_from + (self._anim_to - self._anim_from) * t_eased
        self._display_score = val

        # —— 应用到 UI —— #
        # 1) 狐狸形态（按即时分数）
        self._apply_state(fox_state_for(val))
        # 2) 徽章数字（取整显示；也可显示一位小数）
        self.badge.setText(f"{val:.0f}")
        # 3) 进度条 + 颜色
        self.progress.setValue(int(round(val)))
        self.progress.setStyleSheet(self._bar_style(self._color_for_score(val)))

        if t >= 1.0:
            # 动画结束，确保终值一致
            self._display_score = self._anim_to
            self._anim_timer.stop()

    # ---------- 拖拽 ----------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_active and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_active = False
        super().mouseReleaseEvent(event)

    # ---------- 右键菜单 ----------
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        act_toggle_progress = QAction("Hide Progress" if self._progress_visible else "Show Progress", self)
        act_always_on_top   = QAction("Always on Top ✓" if self._always_on_top else "Always on Top", self)
        act_close           = QAction("Close", self)

        def toggle_progress():
            self._progress_visible = not self._progress_visible
            # 用当前显示值重绘（不破坏动画状态）
            self._apply_state(fox_state_for(self._display_score))
            self.badge.setText(f"{self._display_score:.0f}")
            if self._progress_visible:
                self.progress.show()
            else:
                self.progress.hide()

        def toggle_always_on_top():
            self._always_on_top = not self._always_on_top
            flags = Qt.FramelessWindowHint | Qt.Tool
            if self._always_on_top:
                flags |= Qt.WindowStaysOnTopHint
            self.setWindowFlags(flags)
            self.show()  # 变更 flags 后需要 show 一下

        def do_close():
            # 先关闭窗口，再退出事件循环
            self.close()
            app = QApplication.instance()
            if app is not None:
                app.quit()

        act_toggle_progress.triggered.connect(toggle_progress)
        act_always_on_top.triggered.connect(toggle_always_on_top)
        act_close.triggered.connect(do_close)

        menu.addAction(act_toggle_progress)
        menu.addAction(act_always_on_top)
        menu.addSeparator()
        menu.addAction(act_close)
        menu.exec(event.globalPos())
