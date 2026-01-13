# 修复 app.py 打包问题

## 问题

调试信息显示：
```
FRONTEND_DIR = C:\Users\erich\Downloads\创业FocusMate AI\MVP\FoxMate AI\dist\FoxMate AI\_internal\frontend
FRONTEND_DIR exists = True
app.py exists = False  ← 问题在这里！
```

`frontend/app.py` 文件没有被正确打包到 `_internal/frontend/` 目录中。

## 原因

`.spec` 文件的 `datas` 部分缺少了 `frontend/app.py`：
- ✅ 有 `('frontend/routes.py', 'frontend')`
- ✅ 有 `('frontend/pages', 'frontend/pages')`
- ❌ **缺少** `('frontend/app.py', 'frontend')`

## 修复

在 `FoxMate AI.spec` 的 `datas` 部分添加：
```python
('frontend/app.py', 'frontend'),  # 主前端文件
('frontend/__init__.py', 'frontend'),  # 确保frontend是一个包
```

同时确保后端也有：
```python
('backend/__init__.py', 'backend'),  # 确保backend是一个包
```

## 下一步

重新打包：
```bash
pyinstaller "FoxMate AI.spec"
```

然后检查 `dist/FoxMate AI/_internal/frontend/app.py` 是否存在。
