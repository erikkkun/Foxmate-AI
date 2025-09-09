from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
data_path = os.path.join(BASE_DIR, "realistic_activity_labeled_data.csv")
df = pd.read_csv(data_path)# 读取数据


# 拼接 app + title 为语义输入
df["combined"] = df["app"] + " - " + df["title"]

# 用 SBERT 编码整句
sbert = SentenceTransformer("all-MiniLM-L6-v2")
X = sbert.encode(df["combined"].tolist())
y = df["label"]

# 划分训练集并训练模型
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 保存模型和打印报告
model_path = os.path.join(BASE_DIR, "rf_semantic_model.pkl")
joblib.dump(clf, model_path)
print(classification_report(y_test, clf.predict(X_test)))


