# FoxMate AI - PyInstaller 打包配置说明

## 项目概述

**项目名称**: FoxMate AI  
**类型**: 桌面应用程序（PySide6 GUI + 后端监控服务）  
**平台**: Windows 10/11  
**Python版本**: 3.12+  

## 项目架构

### 双模块结构
1. **前端 (Frontend)**: PySide6 GUI应用，提供用户界面
   - 入口文件: `frontend/app.py`
   - 包含多个页面模块（home, settings, weekly_report等）
   
2. **后端 (Backend)**: 桌面宠物和专注度监控服务
   - 入口文件: `backend/run.py`
   - 包含AI模型、活动监控、狐狸宠物UI

### 关键特性
- 使用PySide6进行GUI开发
- 集成机器学习模型（sentence-transformers, scikit-learn）
- 使用PyTorch进行AI推理
- Windows特定API（win32gui, win32process）
- 实时活动监控（键盘、鼠标、窗口）

## 依赖关系

### 核心GUI框架
- **PySide6** (>=6.5): Qt GUI框架
- **shiboken6**: PySide6的绑定库

### 系统监控
- **psutil** (>=5.9): 系统进程和资源监控
- **pynput** (>=1.7): 键盘鼠标事件监听
- **pywin32** (>=305): Windows API访问

### 机器学习/AI
- **sentence-transformers** (>=2.2): 文本嵌入模型
- **scikit-learn** (>=1.3): 机器学习模型
- **torch** (>=2.0): PyTorch深度学习框架
- **transformers**: Hugging Face transformers库
- **numpy** (>=1.24): 数值计算
- **pandas** (>=1.5): 数据处理

### 数据处理和可视化
- **matplotlib**: 图表生成（使用Agg后端）
- **PIL/Pillow**: 图像处理
- **tkinter**: 报告窗口（Python内置）

### 其他工具库
- **joblib** (>=1.3): 模型序列化
- **lightgbm** (>=4.0): 梯度提升框架

## 资源文件结构

### 前端资源
```
frontend/
├── app.py              # 主入口
├── routes.py           # 路由定义
└── pages/              # 页面模块
    ├── home.py
    ├── my_info.py
    ├── weekly_report.py
    ├── customize.py
    ├── membership.py
    ├── settings.py
    ├── shop.py
    ├── signin.py
    ├── faq.py
    ├── fox_pet.py
    └── workshop.py
```

### 后端资源
```
backend/
├── run.py                      # 后端主程序
├── pet_ui.py                   # 狐狸宠物UI
├── focus_regressor_sbert.pkl   # 回归模型（重要！）
├── activity_log_focus.jsonl    # 日志文件
├── result.txt                  # 结果文件
└── images/                     # 狐狸图片资源
    ├── fox_sleepy.png
    ├── fox_distracted.png
    ├── fox_neutral.png
    ├── fox_focus.png
    ├── fox_energized.png
    └── fox_celebrate.png
```

### AI模型文件
```
AI Part/
├── AI.py                # AI分类器模块
└── focus_model.pkl      # 分类模型（重要！）
```

### 其他资源
```
notification-alert-269289.mp3  # 声音提醒文件（项目根目录）
```

## PyInstaller配置要点

### 1. 入口点配置
- **主入口**: `frontend/app.py`
- **打包模式**: 文件夹模式（`exclude_binaries=True`）
- **控制台**: `console=False`（GUI应用，隐藏控制台）

### 2. 数据文件包含 (datas)

必须包含以下数据文件：

```python
datas=[
    # 前端文件
    ('frontend/routes.py', 'frontend'),
    ('frontend/pages', 'frontend/pages'),
    
    # 后端文件
    ('backend/run.py', 'backend'),
    ('backend/pet_ui.py', 'backend'),
    ('backend/images', 'backend/images'),  # 整个图片目录
    ('backend/focus_regressor_sbert.pkl', 'backend'),  # 模型文件
    ('backend/activity_log_focus.jsonl', 'backend'),
    ('backend/result.txt', 'backend'),
    
    # AI模型
    ('AI Part/AI.py', 'AI Part'),
    ('AI Part/focus_model.pkl', 'AI Part'),
    
    # 声音文件（在项目根目录）
    ('notification-alert-269289.mp3', '.'),
]
```

### 3. 隐藏导入 (hiddenimports)

必须显式导入的模块：

```python
hiddenimports=[
    # 系统监控
    'psutil', 'pynput', 'win32gui', 'win32process',
    
    # 机器学习
    'joblib', 'sklearn.neighbors._base',
    'sentence_transformers',
    'numpy', 'pandas', 'scipy',
    
    # GUI和可视化
    'matplotlib', 'tkinter',
    'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
    
    # Windows COM（声音播放）
    'win32com.client',
]
```

### 4. 路径处理

**关键问题**: PyInstaller打包后，`__file__`路径会改变，需要使用`sys._MEIPASS`。

#### 前端路径处理
```python
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys._MEIPASS) / 'frontend'
else:
    APP_DIR = Path(__file__).parent
```

#### 后端路径处理
```python
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS) / "backend"
    AI_DIR = Path(sys._MEIPASS) / "AI Part"
else:
    BASE_DIR = Path(__file__).resolve().parent
    AI_DIR = (BASE_DIR / ".." / "AI Part").resolve()
```

### 5. 后端启动机制

**特殊处理**: 打包后无法使用`subprocess`启动Python脚本，需要直接导入：

```python
if getattr(sys, 'frozen', False):
    # 直接导入并运行backend模块
    backend_dir = Path(sys._MEIPASS) / "backend"
    sys.path.insert(0, str(backend_dir))
    import run as backend_run
    backend_run._run()
```

### 6. 模型文件处理

**重要**: 模型文件（.pkl）必须正确打包：
- `backend/focus_regressor_sbert.pkl` - 回归模型
- `AI Part/focus_model.pkl` - 分类模型

这些文件较大，确保：
- 文件路径正确
- 打包后路径引用正确
- 使用`sys._MEIPASS`获取打包后的路径

### 7. 大文件依赖

**PyTorch**: 包含大量DLL和库文件
- 自动检测并包含
- 文件大小会增加（数百MB）
- 这是正常的

**sentence-transformers**: 
- 首次运行会下载模型（如果未缓存）
- 确保网络连接或预下载模型

### 8. Windows特定配置

- **UPX压缩**: 启用（`upx=True`）以减小文件大小
- **架构**: Windows 64位
- **控制台**: 禁用（`console=False`）
- **图标**: 可添加（`icon=None`，可配置）

## 打包命令

### 基本命令
```bash
pyinstaller "FoxMate AI.spec"
```

### 自动化脚本
```bash
# Windows批处理
build_package.bat

# Git Bash
./build_package.sh
```

## 打包输出结构

```
dist/FoxMate AI/
├── FoxMate AI.exe          # 主执行文件
└── _internal/              # 内部文件目录
    ├── frontend/
    │   ├── routes.py
    │   └── pages/
    ├── backend/
    │   ├── run.py
    │   ├── pet_ui.py
    │   ├── images/
    │   └── *.pkl
    ├── AI Part/
    ├── notification-alert-269289.mp3
    └── [所有Python依赖和DLL]
```

## 常见问题和解决方案

### 1. 模块找不到
- **问题**: `ModuleNotFoundError`
- **解决**: 添加到`hiddenimports`列表

### 2. 资源文件找不到
- **问题**: `FileNotFoundError`
- **解决**: 检查`datas`列表，确保路径正确

### 3. 路径错误
- **问题**: 打包后路径引用错误
- **解决**: 使用`sys._MEIPASS`检测打包环境

### 4. 后端无法启动
- **问题**: 点击"Fox it!"按钮无反应
- **解决**: 直接导入backend模块，不使用subprocess

### 5. 模型加载失败
- **问题**: 模型文件找不到
- **解决**: 确保.pkl文件在datas列表中，路径引用正确

## 文件大小优化

### 当前大小
- 完整打包: ~500MB-1GB（包含PyTorch）
- 这是正常的，因为包含完整的ML库

### 优化建议
1. 排除未使用的模块
2. 使用UPX压缩（已启用）
3. 考虑分离模型文件（首次运行时下载）

## 测试清单

打包后必须测试：
- [ ] exe可以正常启动
- [ ] 前端主页正常显示
- [ ] 所有页面可以切换
- [ ] "Fox it!"按钮可以启动后端
- [ ] 后端狐狸宠物正常显示
- [ ] 专注度分数正常更新
- [ ] 模型文件可以正常加载
- [ ] 图片资源正常显示
- [ ] 声音文件可以播放

## 分发准备

1. **压缩**: 将`dist/FoxMate AI/`文件夹压缩为ZIP
2. **添加说明**: 包含`README.txt`
3. **文件结构**:
   ```
   FoxMate AI v1.0.zip
   ├── FoxMate AI/
   │   ├── FoxMate AI.exe
   │   └── _internal/
   └── README.txt
   ```

## 特殊注意事项

1. **首次运行**: 可能需要几秒钟加载时间
2. **Windows Defender**: 可能显示安全警告（未签名应用）
3. **文件位置**: 建议用户不要移动文件夹
4. **权限**: 可能需要管理员权限（监控系统活动）
5. **网络**: 首次运行sentence-transformers可能需要下载模型

## 版本信息

- **PyInstaller版本**: 6.16.0+
- **Python版本**: 3.12.10
- **平台**: Windows-11-10.0.26200-SP0
