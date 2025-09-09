import sys
import time
import json
import os
from datetime import datetime
import psutil
import win32gui
import win32process
import win32api
import joblib
from sentence_transformers import SentenceTransformer

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# ==== 路径设置 ====
BASE_DIR = os.path.dirname(__file__)

# ==== 导入 UI ====
from backend.pet_ui import FloatingPet

# ==== 模型 & 文件 ====
model_path = os.path.join(BASE_DIR, "rf_semantic_model.pkl")
clf = joblib.load(model_path)
sbert = SentenceTransformer("all-MiniLM-L6-v2")
LOG_FILE = os.path.join(BASE_DIR, "activity_log_with_prediction.json")

# ==== 状态变量 ====
last_label = 0
last_title = ""
last_reminder_time = 0
MIN_REMINDER_INTERVAL = 20  # 秒

# ==== 工具函数 ====
def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc = psutil.Process(pid)
        app_name = proc.name()
        window_title = win32gui.GetWindowText(hwnd)
        return app_name, window_title
    except Exception:
        return "Unknown", "Unknown"

def get_idle_duration():
    last_input = win32api.GetLastInputInfo()
    millis = win32api.GetTickCount() - last_input
    return millis / 1000.0

def predict_label(app: str, title: str):
    combined_text = f"{app} - {title}"
    vec = sbert.encode([combined_text])
    label = clf.predict(vec)[0]
    return int(label)

# ==== 核心逻辑 ====
def log_and_predict(pet):
    global last_label, last_title, last_reminder_time

    app, title = get_active_window_info()
    idle_sec = get_idle_duration()
    label = predict_label(app, title)
    now = time.time()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "app": app,
        "title": title,
        "idle_seconds": round(idle_sec, 2),
        "prediction": label
    }

    label_text = "🎓 工作中" if label == 0 else "😴 摸鱼中"
    print(f"[{entry['timestamp']}] {label_text} | {app} | {title}")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 控制宠物表情
    if label == 0:
        pet.show_study()
    else:
        title_changed = title != last_title
        long_enough = now - last_reminder_time > MIN_REMINDER_INTERVAL
        if title_changed or long_enough:
            pet.show_reminder()
            last_reminder_time = now
        else:
            pet.show_normal()

    last_label = label
    last_title = title

# ==== 提供给前端调用的启动函数 ====
def start_fox_pet():
    """创建桌宠并启动检测循环"""
    pet = FloatingPet()
    pet.show()

    timer = QTimer()
    timer.timeout.connect(lambda: log_and_predict(pet))
    timer.start(5000)

    return pet, timer

# ==== 主入口 ====
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     pet = FloatingPet()
#     pet.show()

#     timer = QTimer()
#     timer.timeout.connect(lambda: log_and_predict(pet))
#     timer.start(5000)  # 每 5 秒执行一次

#     print("🐾 FocusMate 桌宠正在运行中")
#     sys.exit(app.exec())

