# backend/run.py
import sys, os, time, math, threading, json
from collections import deque
from datetime import datetime
from pathlib import Path
from io import BytesIO

import psutil, joblib
import win32gui, win32process
from pynput import keyboard, mouse
from sentence_transformers import SentenceTransformer
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

# === UI ===
from pet_ui import FloatingPet

# === 路径与模型 ===
BASE_DIR = Path(__file__).resolve().parent
BUNDLE_PATH = BASE_DIR / "focus_regressor_sbert.pkl"
LOG_PATH = BASE_DIR / "activity_log_focus.jsonl"

# === 加载回归模型 ===
bundle = joblib.load(BUNDLE_PATH)
reg = bundle["regressor"]
scaler = bundle["numeric_scaler"]
sbert = SentenceTransformer(bundle["sbert_model_name"])

# === 加载 AI 模型 ===
AI_DIR = (BASE_DIR / ".." / "AI Part").resolve()
sys.path.append(str(AI_DIR))
import importlib.util
spec = importlib.util.spec_from_file_location("AI", str(AI_DIR / "AI.py"))
AI = importlib.util.module_from_spec(spec)
sys.modules["AI"] = AI
sys.modules["__main__"] = AI
spec.loader.exec_module(AI)

FocusClassifier = AI.FocusClassifier
ai_model = FocusClassifier(use_gpu=False)
ai_model.load_model(str(AI_DIR / "focus_model.pkl"))

# === 记录 session start ===
SESSION_START = datetime.now().isoformat()
SESSION_SCORES = []  # ✅ 实时缓存每次 tick 的 focus score
try:
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"session_start": SESSION_START}, ensure_ascii=False) + "\n")
except Exception as e:
    print("Session start log failed:", e)

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

# === 键鼠统计 ===
WINDOW = 60
lock = threading.Lock()
key_press_times = deque()
mouse_move_deltas = deque()
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
    with lock:
        key_press_times.append(time.time())

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

keyboard.Listener(on_press=on_key_press, suppress=False).start()
mouse.Listener(on_move=on_mouse_move).start()

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

# === tags 推断 ===
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
    tags = [tag for tag, kws in KEYWORDS.items() if any(k in t for k in kws)]
    if not tags:
        tags.append("browsing")
    return ", ".join(sorted(set(tags + ["behavior"])))

# === focus预测 ===
def predict_focus(app, title, ks_per_min, mouse_px_per_min):
    tags = infer_tags(app, title)
    text = f"{app} | {title} | {tags}"
    emb = sbert.encode([text], convert_to_numpy=True)
    num = scaler.transform([[ks_per_min, mouse_px_per_min]])
    X = np.hstack([emb, num])
    X_df = pd.DataFrame(X, columns=[f"f{i}" for i in range(X.shape[1])])
    score = float(reg.predict(X_df)[0])
    return max(0.0, min(100.0, score)), tags

# === tick ===
def tick(pet: FloatingPet):
    app_name, title = get_active_window_info()
    ks = ks_last_60s()
    mp = mouse_px_last_60s()
    score, tags = predict_focus(app_name, title, ks, mp)
    SESSION_SCORES.append(score)  # ✅ 缓存实时分数

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
        print("log write error:", e)

    try:
        result = ai_model.monitor_activity(entry)
        if result:
            pet.update_message(result["message"])
    except Exception as e:
        print("AI 提示失败:", e)

    pet.update_by_score(score)
    print(f"[{entry['ts']}] {app_name} | ks={ks}/min, mouse={mp:.0f}px/min -> {score:.1f}")

# === 生成 Tkinter 报告 ===
def show_report(scores):
    if not scores:
        scores = [0]

    avg, high, low = np.mean(scores), np.max(scores), np.min(scores)

    fig, ax = plt.subplots(figsize=(5.2, 2.3))
    ax.plot(scores, color="#43A047", linewidth=2, label="Focus Score")
    ax.axhline(avg, color="#FB8C00", linestyle="--", linewidth=1.5, label=f"Avg: {avg:.1f}")
    ax.set_ylim(0, 100)
    ax.set_title("Focus Score Over Time", fontsize=11)
    ax.set_xlabel("Time Index")
    ax.set_ylabel("Score")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    chart_img = Image.open(buf)

    root = tk.Tk()
    root.title("🦊 Focus Session Report")
    root.geometry("640x560")
    root.configure(bg="white")

    tk.Label(root, text="Session Summary", font=("Arial", 20, "bold"), bg="white", fg="#222").pack(pady=10)

    chart_photo = ImageTk.PhotoImage(chart_img)
    chart_label = tk.Label(root, image=chart_photo, bg="white")
    chart_label.image = chart_photo
    chart_label.pack(pady=10)

    summary_text = (
        f"Average Focus: {avg:.1f}\n"
        f"Highest Focus: {high:.1f}\n"
        f"Lowest Focus: {low:.1f}\n"
        f"Records: {len(scores)}"
    )
    tk.Label(root, text=summary_text, font=("Arial", 13), bg="white", fg="#333", justify="center").pack(pady=10)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=8)
    ttk.Button(root, text="Close Report", command=root.destroy).pack(pady=12)

    print("🦊 Report window shown (cached session data).")
    root.mainloop()

# === 主程序 ===
def _run():
    qapp = QApplication(sys.argv)
    pet = FloatingPet()
    pet.show()

    timer = QTimer()
    timer.timeout.connect(lambda: tick(pet))
    timer.start(5000)  # tick every 5s

    def cleanup():
        try:
            timer.stop()
        except:
            pass
        print("🦊 Session ended — generating report...")
        show_report(SESSION_SCORES)
        sys.exit(0)

    qapp.aboutToQuit.connect(cleanup)
    print("✅ Fox pet with AI Hybrid model is running…")
    sys.exit(qapp.exec())

if __name__ == "__main__":
    _run()
