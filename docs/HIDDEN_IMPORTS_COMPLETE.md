# 完整Hidden Imports列表

## 已添加的所有隐藏导入

### 系统监控
- `psutil` - 系统进程监控
- `pynput` - 键盘鼠标监听
- `win32gui`, `win32process` - Windows API

### 模型序列化
- `joblib` - 模型加载（需要所有模型库）

### 机器学习库（模型反序列化需要）
- `lightgbm` - **关键**：模型文件中使用了LightGBM
- `sklearn` - scikit-learn基础
- `sklearn.neighbors._base` - KNN算法
- `sklearn.ensemble` - 集成学习
- `sklearn.linear_model` - 线性模型
- `sklearn.tree` - 决策树
- `sklearn.base` - 基础类
- `sklearn.utils` - 工具函数
- `sklearn.utils._param_validation` - 参数验证

### 文本嵌入
- `sentence_transformers` - 文本嵌入模型

### 数据科学
- `numpy` - 数值计算
- `pandas` - 数据处理
- `scipy` - 科学计算

### 可视化
- `matplotlib` - 图表生成
- `matplotlib.backends.backend_agg` - Agg后端
- `PIL`, `PIL.Image`, `PIL.ImageTk` - 图像处理

### Tkinter（报告窗口）
- `tkinter` - 基础GUI
- `tkinter.ttk` - 主题化组件
- `tkinter.filedialog` - 文件对话框
- `tkinter.messagebox` - 消息框

### PySide6 GUI
- `PySide6.QtCore`, `PySide6.QtGui`, `PySide6.QtWidgets`

### Windows COM
- `win32com.client` - 声音播放

### PyTorch（AI模型）
- `torch`, `torch.nn`, `torch.optim`, `torch.utils.data`
- `transformers` - Hugging Face transformers

### 其他工具
- `tqdm` - 进度条（AI.py中使用）

## 为什么需要这些？

### 模型文件反序列化
当使用`joblib.load()`加载.pkl文件时，Python需要：
1. 找到模型类定义（LightGBM, sklearn等）
2. 导入所有相关的模块
3. 重建对象

如果缺少任何模块，会报错：`ModuleNotFoundError: No module named 'xxx'`

### 常见问题
- **lightgbm**: 模型文件中使用了LightGBM回归器
- **sklearn子模块**: 模型可能使用各种sklearn组件
- **torch**: AI.py中使用了PyTorch
- **tkinter.ttk**: 报告窗口使用了ttk组件

## 如果仍有缺失模块

如果遇到新的`ModuleNotFoundError`：
1. 查看错误信息中的模块名
2. 添加到`hiddenimports`列表
3. 重新打包

## 验证

打包后检查：
```bash
# 检查是否包含lightgbm
python -c "import sys; sys.path.insert(0, 'dist/FoxMate AI/_internal'); import lightgbm; print('OK')"
```
