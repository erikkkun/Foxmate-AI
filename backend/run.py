# backend/run.py
import sys, os, time, math, threading, json
from collections import deque
from datetime import datetime
from pathlib import Path

import psutil, joblib
import win32gui, win32process
from pynput import keyboard, mouse
from sentence_transformers import SentenceTransformer

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# === UI ===
from pet_ui import FloatingPet


# === 路径 ===
BASE_DIR = Path(__file__).resolve().parent
BUNDLE_PATH = BASE_DIR / "focus_regressor_sbert.pkl"
LOG_PATH   = BASE_DIR / "activity_log_focus.jsonl"

# === 模型包 ===
bundle = joblib.load(BUNDLE_PATH)
reg = bundle["regressor"]
scaler = bundle["numeric_scaler"]
sbert = SentenceTransformer(bundle["sbert_model_name"])

# === 活动窗口信息 ===
def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        app_name = psutil.Process(pid).name()
        title = win32gui.GetWindowText(hwnd)
        return app_name or "Unknown", title or "Unknown"
    except Exception:
        return "Unknown", "Unknown"

# === 键鼠 60s 滑窗统计 ===
WINDOW = 60
lock = threading.Lock()
key_press_times = deque()
mouse_move_deltas = deque()  # (t, dp)
_last_pos = None

def _purge_older(deq, cutoff, is_move=False):
    while deq:
        head = deq[0]
        t = head[0] if is_move else head
        if t < cutoff:
            deq.popleft()
        else:
            break

def on_key_press(key):
    t = time.time()
    with lock:
        key_press_times.append(t)

def on_mouse_move(x, y):
    global _last_pos
    t = time.time()
    with lock:
        if _last_pos is not None:
            dx, dy = x - _last_pos[0], y - _last_pos[1]
            dp = math.hypot(dx, dy)
            if dp > 0:
                mouse_move_deltas.append((t, dp))
        _last_pos = (x, y)

kb_listener = keyboard.Listener(on_press=on_key_press, suppress=False)
ms_listener = mouse.Listener(on_move=on_mouse_move)
kb_listener.start()
ms_listener.start()

def ks_last_60s():
    cutoff = time.time() - WINDOW
    with lock:
        _purge_older(key_press_times, cutoff)
        return len(key_press_times)

def mouse_px_last_60s():
    cutoff = time.time() - WINDOW
    with lock:
        _purge_older(mouse_move_deltas, cutoff, is_move=True)
        return sum(dp for _, dp in mouse_move_deltas)

# === 轻量 tags 推断（用于日志 & 文本提示） ===
KEYWORDS = {
    "study": ["docs", "notion", "overleaf", "report", "homework", "lecture", "pdf",
              "vscode", "pycharm", "jupyter", "word", "google docs"],
    "entertainment": ["youtube", "netflix", "twitch", "spotify", "music", "reddit",
                      "weibo", "bilibili"],
    "meeting": ["zoom", "teams", "meet", "slack"],
    "shopping": ["amazon", "bestbuy", "ebay", "cart", "checkout"],
    "email": ["gmail", "outlook", "inbox", "compose"]
}
def infer_tags(app, title):
    t = f"{app} {title}".lower()
    tags = []
    for tag, kws in KEYWORDS.items():
        if any(k in t for k in kws):
            tags.append(tag)
    if not tags:
        tags.append("browsing")
    return ", ".join(sorted(set(tags + ["behavior"])))

# === 文本 + 数值 → 预测（返回 score, tags） ===
import numpy as np, pandas as pd
def predict_focus(app, title, ks_per_min, mouse_px_per_min):
    tags = infer_tags(app, title)
    text = f"{app} | {title} | {tags}"
    emb = sbert.encode([text], convert_to_numpy=True)
    num = scaler.transform([[ks_per_min, mouse_px_per_min]])
    X = np.hstack([emb, num])
    X_df = pd.DataFrame(X, columns=[f"f{i}" for i in range(X.shape[1])])
    score = float(reg.predict(X_df)[0])
    # score = 99
    return max(0.0, min(100.0, score)), tags

# === 定时器 ===
def tick(pet: FloatingPet):
    app_name, title = get_active_window_info()
    ks = ks_last_60s()
    mp = mouse_px_last_60s()
    score, tags = predict_focus(app_name, title, ks, mp)

    # 写 JSONL 日志
    entry = {
        "ts": datetime.now().isoformat(),
        "app": app_name,
        "title": title,
        "keystrokes_per_min": ks,
        "mouse_px_per_min": round(mp, 1),
        "tags": tags,
        "pred_focus": round(score, 2),
    }
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        # 不让写日志的问题阻断 UI
        print("log write error:", e)

    # 更新 UI
    pet.update_by_score(score)

    # 控制台打印（可选）
    print(f"[{entry['ts']}] {app_name} | {title} | ks={ks}/min, mouse={mp:.0f}px/min -> {score:.1f}")

# === 入口 ===
def _run():
    qapp = QApplication(sys.argv)
    pet = FloatingPet()
    pet.show()

    timer = QTimer()
    timer.timeout.connect(lambda: tick(pet))
    timer.start(2000)  # 每2秒刷新

    # 退出清理
    def cleanup():
        try: timer.stop()
        except: pass
        try: kb_listener.stop()
        except: pass
        try: ms_listener.stop()
        except: pass

    qapp.aboutToQuit.connect(cleanup)
    print("✅ Fox pet with logging is running…")
    sys.exit(qapp.exec())

# 兼容两种启动方式
if __name__ == "__main__":
    _run()

# 前端调用入口（如需）
def start_backend():
    print("Backend started!")
    _run()
