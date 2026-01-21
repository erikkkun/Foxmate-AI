# backend/pet_ui.py
import os, math, time, threading, sys
from pathlib import Path
from PySide6.QtWidgets import QWidget, QLabel, QMenu, QProgressBar, QApplication
from PySide6.QtGui import QPixmap, QAction, QPainter, QPainterPath, QFont, QFontMetrics, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QPoint, QTimer, QRect

# 声音效果支持 - Support PyInstaller bundled path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS) / 'backend'
    PROJECT_ROOT = Path(sys._MEIPASS)  # 项目根目录（在打包后的位置）
else:
    # Running as script
    BASE_DIR = Path(__file__).parent
    PROJECT_ROOT = BASE_DIR.parent  # 项目根目录

ALERT_SOUND_FILE = str(PROJECT_ROOT / "notification-alert-269289.mp3")

# 尝试使用Windows COM对象播放MP3
try:
    import win32com.client
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False
    print("⚠️ win32com not available. Trying alternative methods...")

IMG = lambda name: str(BASE_DIR / "images" / name)

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
    return 1 - pow(1 - t, 3)

class SpeechBubble(QWidget):
    """
    自定义对话气泡组件：椭圆形气泡 + 指向狐狸的小尾巴
    根据文本长度自动调整大小
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self._text = ""
        self._min_width = 120
        self._max_width = 280  # 增加最大宽度以容纳更长文本
        self._padding = 12
        self._tail_size = 12  # 尾巴大小
        self._tail_offset = 0  # 尾巴在底部的偏移位置（相对于中心）
        
        # 设置字体（与分数徽章相同）
        self._font = QFont('Comic Sans MS', 14)
        self._font.setWeight(QFont.Weight.Bold)  # 使用枚举值而不是数字
        self._font.setItalic(True)
        
    def setText(self, text: str):
        """设置文本并自动调整大小"""
        self._text = text
        if text:
            self._update_size()
        self.update()  # 触发重绘
        
    def _update_size(self):
        """根据文本内容计算所需的大小"""
        fm = QFontMetrics(self._font)
        
        # 增加 padding 以提供更多空间
        effective_padding = self._padding + 4
        
        # 计算文本在最大宽度下的高度（使用更宽松的宽度限制）
        available_width = self._max_width - 2 * effective_padding
        text_rect = fm.boundingRect(
            QRect(0, 0, available_width, 0),
            Qt.TextWordWrap | Qt.AlignCenter | Qt.AlignVCenter,
            self._text
        )
        
        # 计算实际需要的宽度
        # 使用文本宽度 + 更多 padding，确保有足够空间
        text_width = text_rect.width()
        content_width = text_width + 2 * effective_padding + 8  # 额外增加8px缓冲
        bubble_width = max(self._min_width, min(content_width, self._max_width))
        
        # 重新计算高度，使用实际宽度
        text_rect_final = fm.boundingRect(
            QRect(0, 0, bubble_width - 2 * effective_padding, 0),
            Qt.TextWordWrap | Qt.AlignCenter | Qt.AlignVCenter,
            self._text
        )
        
        # 计算高度（文本高度 + padding + 尾巴高度 + 额外缓冲）
        text_height = text_rect_final.height()
        bubble_height = text_height + 2 * effective_padding + self._tail_size + 4  # 额外增加4px缓冲
        
        # 设置widget大小
        self.setFixedSize(int(bubble_width), int(bubble_height))
        
    def paintEvent(self, event):
        """绘制椭圆形气泡和尾巴"""
        if not self._text:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        width = self.width()
        height = self.height()
        tail_size = self._tail_size
        
        # 气泡主体（椭圆）
        bubble_height = height - tail_size
        bubble_rect = QRect(0, 0, width, bubble_height)
        
        # 创建完整的路径（椭圆 + 尾巴）
        full_path = QPainterPath()
        
        # 添加椭圆
        full_path.addEllipse(bubble_rect)
        
        # 添加尾巴（指向下方的小三角形）
        # 尾巴位置：椭圆底部中心稍微偏移
        tail_x = width / 2 + self._tail_offset
        tail_y = bubble_height  # 椭圆底部（这是椭圆的最底部y坐标）
        
        # 创建尾巴路径（三角形），从椭圆底部向下延伸
        # 尾巴应该形成一个向下的三角形，指向狐狸
        # 注意：三角形的顶点在底部（指向狐狸），顶部连接椭圆
        tail_path = QPainterPath()
        # 起点：尾巴底部顶点（指向狐狸的点）
        tail_path.moveTo(tail_x, tail_y + tail_size)
        # 左上角（连接椭圆的左侧点）
        tail_path.lineTo(tail_x - tail_size / 2, tail_y)
        # 右上角（连接椭圆的右侧点）
        tail_path.lineTo(tail_x + tail_size / 2, tail_y)
        # 闭合路径回到起点（形成三角形）
        tail_path.closeSubpath()
        
        # 合并路径（使用united确保无缝连接）
        # 这会将椭圆和尾巴合并成一个完整的形状
        full_path = full_path.united(tail_path)
        
        # 绘制填充
        painter.fillPath(full_path, QBrush(QColor(255, 255, 255, 230)))
        
        # 绘制边框（可选，更精致）
        pen = QPen(QColor(200, 200, 200, 150), 1)
        painter.setPen(pen)
        painter.drawPath(full_path)
        
        # 绘制文本
        painter.setFont(self._font)
        painter.setPen(QColor(34, 34, 34))  # 深灰色文字
        
        # 使用与计算大小相同的 padding
        effective_padding = self._padding + 4
        text_rect = QRect(
            effective_padding,
            0,
            width - 2 * effective_padding,
            bubble_height
        )
        
        painter.drawText(
            text_rect,
            Qt.TextWordWrap | Qt.AlignCenter | Qt.AlignVCenter,
            self._text
        )

class FloatingPet(QWidget):
    """
    可拖拽、右键菜单、圆形透明徽章 + 竖直加粗进度条的小狐狸桌宠。
    现在增加了“说话气泡”，AI提醒文字会实时显示在狐狸上方。
    """
    def __init__(self):
        super().__init__()
        # 无边框、置顶、透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 拖拽状态
        self._drag_active = False
        self._drag_pos = QPoint()
        self._always_on_top = True
        self._progress_visible = True

        # 动画状态
        self._display_score = 0.0
        self._anim_from = 0.0
        self._anim_to = 0.0
        self._anim_start_ts = 0.0
        self._anim_duration_ms = 500
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(16)
        self._anim_timer.timeout.connect(self._on_anim_tick)

        # 狐狸形象
        self.fox = QLabel(self)
        self.fox.setAlignment(Qt.AlignCenter)

        # 圆形分数徽章
        self.badge = QLabel(self)
        self.badge.setAlignment(Qt.AlignCenter)
        self.badge.setStyleSheet("""
            background: white;
            color: black;
            font-size: 18px;
            font-weight: 700;
            font-family: 'Comic Sans MS';
            font-style: italic;
            border: 2px solid #111;
            border-radius: 24px;
        """)
        self.badge.setText("--")
        self.badge.resize(48, 48)

        # 竖直进度条
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setOrientation(Qt.Vertical)
        self.progress.setFixedSize(28, 140)
        self.progress.setStyleSheet(self._bar_style("#4caf50"))
        self.progress.show()

        # === 新增：说话气泡（自定义椭圆形带尾巴） ===
        self.speech = SpeechBubble(self)
        self.speech.hide()


        # 初始布局
        # 增加窗口高度，为对话气泡留出空间（从260增加到350）
        self.resize(300, 350)
        self.move(60, 60)
        self._pixmaps = {}
        self._load_pixmaps()
        self._apply_state("neutral")
        self._relayout()

        # 右键菜单
        self.setContextMenuPolicy(Qt.DefaultContextMenu)

    # ---------- 样式 ----------
    def _bar_style(self, color_hex: str) -> str:
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
        if s < 40:   return "#ef5350"
        if s < 70:   return "#ffa726"
        return "#4caf50"

    # ---------- 资源 ----------
    def _load_pixmaps(self):
        for k, fname in FOX_FILES.items():
            path = IMG(fname)
            pm = QPixmap(path)
            if pm.isNull():
                pm = QPixmap(1, 1)
                pm.fill(Qt.transparent)
            self._pixmaps[k] = pm

    def _apply_state(self, state: str):
        pm = self._pixmaps.get(state) or self._pixmaps["neutral"]
        pm_scaled = pm.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.fox.setPixmap(pm_scaled)

    # ---------- 布局 ----------
    def _relayout(self):
        # 为对话气泡预留顶部空间（约100像素）
        SPEECH_SPACE_TOP = 100
        
        self.fox.resize(200, 200)
        # 将狐狸向下移动，为对话气泡留出空间
        fox_y = SPEECH_SPACE_TOP + int((self.height() - SPEECH_SPACE_TOP - 200) / 2)
        self.fox.move(int((self.width()-200)/2), fox_y)

        bx = self.fox.x() + self.fox.width() - self.badge.width() + 12
        by = self.fox.y() - 12
        self.badge.move(bx, by)

        px = self.badge.x() + (self.badge.width() - self.progress.width()) // 2
        py = self.badge.y() + self.badge.height() + 6
        self.progress.move(px, py)

        # 气泡在狐狸头顶上方，确保不被裁剪
        # 向上移动更多，并稍微向左偏移，避免遮挡狐狸头部
        speech_y = self.fox.y() - 130  # 向上移动130像素（增加更多）
        # 确保气泡不会超出窗口顶部（留出10像素边距）
        if speech_y < 10:
            speech_y = 10
        # 气泡向左偏移，避免遮挡狐狸头部
        # 水平居中后向左移动60像素（增加更多）
        speech_x = self.fox.x() + (self.fox.width() - self.speech.width()) // 2 - 60
        # 确保不会超出窗口左边界
        if speech_x < 0:
            speech_x = 10
        self.speech.move(speech_x, speech_y)
        
        # 如果气泡可见，更新尾巴位置指向狐狸
        if self.speech.isVisible() and self.speech._text:
            self._update_speech_tail()
    
    def _update_speech_tail(self):
        """更新对话气泡的尾巴位置，使其指向狐狸中心"""
        if not self.speech.isVisible() or not self.speech._text:
            return
        fox_center_x = self.fox.x() + self.fox.width() / 2
        bubble_center_x = self.speech.x() + self.speech.width() / 2
        tail_offset = fox_center_x - bubble_center_x
        # 限制偏移范围，避免尾巴太偏
        max_offset = self.speech.width() / 2 - self.speech._tail_size - 5
        self.speech._tail_offset = max(-max_offset, min(max_offset, tail_offset))
        self.speech.update()  # 触发重绘以更新尾巴位置

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._relayout()

    # ---------- 分数更新 ----------
    def update_by_score(self, new_score: float):
        new_score = max(0.0, min(100.0, float(new_score)))
        current = self._display_score
        if not self._anim_timer.isActive():
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
        elapsed = (time.time() - self._anim_start_ts) * 1000.0
        t = min(1.0, max(0.0, elapsed / self._anim_duration_ms))
        t_eased = ease_out_cubic(t)
        val = self._anim_from + (self._anim_to - self._anim_from) * t_eased
        self._display_score = val

        self._apply_state(fox_state_for(val))
        self.badge.setText(f"{val:.0f}")
        self.progress.setValue(int(round(val)))
        self.progress.setStyleSheet(self._bar_style(self._color_for_score(val)))

        if t >= 1.0:
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
            self.show()

        def do_close():
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

    # ---------- 新增：更新说话气泡 ----------
    def update_message(self, text: str):
        """显示 AI 生成的提醒文字"""
        # SpeechBubble会自动根据文本调整大小
        self.speech.setText(text)
        self.speech.show()
        self.speech.raise_()
        
        # ✅ 调整气泡位置，让它在狐狸头顶上方，并避免遮挡
        # 向上移动更多，并稍微向左偏移
        speech_y = self.fox.y() - 130  # 向上移动130像素（增加更多）
        # 确保气泡不会超出窗口顶部（留出10像素边距）
        if speech_y < 10:
            speech_y = 10
        
        # 气泡向左偏移，避免遮挡狐狸头部
        # 水平居中后向左移动60像素（增加更多）
        speech_x = self.fox.x() + (self.fox.width() - self.speech.width()) // 2 - 60
        # 确保不会超出窗口左边界
        if speech_x < 0:
            speech_x = 10
        self.speech.move(speech_x, speech_y)
        
        # 更新尾巴位置，使其指向狐狸中心
        self._update_speech_tail()
        
        QTimer.singleShot(8000, self.speech.hide)
    
    def play_alert_sound(self):
        """播放专注度提醒声音效果 - 使用MP3文件（无窗口）"""
        def play_sound():
            try:
                import platform
                
                # 检查MP3文件是否存在
                sound_path = os.path.abspath(ALERT_SOUND_FILE)
                if not os.path.exists(sound_path):
                    print(f"⚠️ Alert sound file not found: {sound_path}")
                    print(f"   Looking in: {os.path.dirname(sound_path)}")
                    return
                
                if platform.system() == 'Windows':
                    # 方法1: 使用Windows Media Player COM对象（无窗口播放）
                    if SOUND_AVAILABLE:
                        try:
                            wmp = win32com.client.Dispatch("WMPlayer.OCX")
                            # 设置为不可见模式
                            wmp.settings.autoStart = True
                            wmp.settings.volume = 100  # 设置音量
                            wmp.settings.mute = False
                            wmp.settings.enableErrorDialogs = False
                            
                            # 隐藏UI窗口 - 使用uiMode属性
                            try:
                                wmp.uiMode = "none"  # 无UI模式
                            except:
                                # 如果uiMode不可用，尝试其他方法
                                pass
                            
                            # 播放文件
                            wmp.URL = sound_path
                            wmp.controls.play()
                            
                            # 等待播放完成（在后台线程中，非阻塞）
                            # 使用异步方式，不阻塞主线程
                            def wait_and_cleanup():
                                try:
                                    while wmp.playState != 1:  # 1 = stopped
                                        time.sleep(0.1)
                                    wmp.controls.stop()
                                    wmp.close()
                                except:
                                    pass
                            
                            # 在另一个线程中等待和清理
                            cleanup_thread = threading.Thread(target=wait_and_cleanup, daemon=True)
                            cleanup_thread.start()
                            
                            # 静默播放，不打印成功信息
                            return
                        except Exception as e1:
                            print(f"⚠️ WMP COM failed: {e1}")
                            import traceback
                            traceback.print_exc()
                    
                    # 方法2: 使用PowerShell播放（无窗口，但只支持WAV）
                    # 跳过，因为我们需要MP3支持
                    
                    # 方法3: 使用subprocess + ffplay（如果可用）
                    try:
                        import subprocess
                        # 尝试使用ffplay（如果系统有ffmpeg）
                        result = subprocess.run(
                            ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', sound_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            timeout=5,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        # 静默播放，不打印成功信息
                        return
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        pass
                    except Exception as e2:
                        print(f"⚠️ ffplay failed: {e2}")
                    
                    print("⚠️ All silent playback methods failed")
                else:
                    print("⚠️ Unsupported platform for MP3 playback")
                    
            except Exception as e:
                print(f"⚠️ Sound error: {e}")
                import traceback
                traceback.print_exc()
        
        thread = threading.Thread(target=play_sound, daemon=True)
        thread.start()
