# 🦊 FoxMate AI — Desktop Focus Assistant

FoxMate AI is an interactive productivity companion that tracks user activity,
analyzes focus levels using a trained ML regressor, and visualizes daily reports
through a floating “fox pet” desktop UI.

---

## 🚀 Features
- 🧠 Real-time focus prediction using `SentenceTransformer` + regression model  
- 🦊 Animated floating fox assistant (PySide6 GUI)  
- 📊 Weekly and session reports (Tkinter + Matplotlib charts)  
- 💾 Local logging of user activity and focus scores  
- 🧩 Modular structure for frontend / backend separation

---

## 🧰 Requirements

| Component | Details |
|------------|----------|
| **OS** | Windows 10 / 11 (PySide6 + Win32 APIs) |
| **Python** | 3.9 or later |
| **Hardware** | ≥2 GB free space, Internet connection (for model download) |

### Dependencies
See [`requirements.txt`](./requirements.txt).  
Install everything via:
```bash
pip install -r requirements.txt
🧱 Project Structure
bash
Copy code
FoxMate_AI/
│
├── backend/             # core logic and UI modules
│   ├── run.py
│   ├── pet_ui.py
│   ├── report_ui.py
│   ├── train_focus_regressor_sbert.py
│   ├── focus_regressor_sbert.pkl
│   └── images/          # fox images for animation
│
├── frontend/            # main app and page routing
│   ├── app.py           # 🟢 launch this to start the app
│   └── pages/
│       ├── home.py
│       ├── shop.py
│       ├── my_info.py
│       ├── weekly_report.py
│       └── ...
│
├── AI Part/             # training & evaluation scripts
│   ├── AI.py
│   └── process_file.py
│
├── requirements.txt
└── README.md
🖥️ How to Run Locally
Clone or download

bash
Copy code
git clone https://github.com/<yourname>/FoxMate_AI.git
cd FoxMate_AI
(If distributed as ZIP, extract it and open the folder instead.)

Set up virtual environment

bash
Copy code
python -m venv venv
venv\Scripts\activate     # Windows
# or source venv/bin/activate (macOS/Linux)
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the app

bash
Copy code
cd frontend
python app.py
The fox pet interface should appear. 🦊✨
(If console shows missing model, ensure focus_regressor_sbert.pkl is in backend/.)

🧾 Optional Convenience
To simplify running, you can create a start.bat:

bat
Copy code
@echo off
call venv\Scripts\activate
python frontend\app.py
pause