# train_focus_regressor_sbert.py
import os, joblib, numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from lightgbm import LGBMRegressor

BASE_DIR = os.path.dirname(__file__) if "__file__" in globals() else "."
CSV_NAME = "focus_training_data_large.csv"     # 放同目录
CSV_PATH = os.path.join(BASE_DIR, CSV_NAME)
MODEL_PATH = os.path.join(BASE_DIR, "focus_regressor_sbert.pkl")
EMB_MODEL_NAME = "all-MiniLM-L6-v2"
BATCH = 256

df = pd.read_csv(CSV_PATH)
text_series = (df["app"].astype(str) + " | " + df["title"].astype(str) + " | " + df["tags"].astype(str)).fillna("")
num = df[["keystrokes_per_min","mouse_px_per_min"]].astype(float).values
y = df["focus_score"].astype(float).values

print("Loading SBERT:", EMB_MODEL_NAME)
sbert = SentenceTransformer(EMB_MODEL_NAME)

def encode_batches(s, bs=BATCH):
    out = []
    for i in range(0, len(s), bs):
        out.append(sbert.encode(s[i:i+bs].tolist(), convert_to_numpy=True, show_progress_bar=False))
    return np.vstack(out)

print("Encoding...")
X_text = encode_batches(text_series)
scaler = StandardScaler()
X_num = scaler.fit_transform(num)
X = np.hstack([X_text, X_num])

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
reg = LGBMRegressor(n_estimators=800, learning_rate=0.05, num_leaves=63,
                    subsample=0.9, colsample_bytree=0.9, random_state=42)
print("Training...")
reg.fit(Xtr, ytr)

yp = reg.predict(Xte)
print(f"MAE: {mean_absolute_error(yte, yp):.2f}")
print(f"R^2:  {r2_score(yte, yp):.2f}")

joblib.dump({"regressor": reg, "numeric_scaler": scaler, "sbert_model_name": EMB_MODEL_NAME}, MODEL_PATH)
print("Saved:", MODEL_PATH)
