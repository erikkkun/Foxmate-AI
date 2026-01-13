# QApplication冲突修复

## 问题描述

当点击"Fox it!"按钮时，前端关闭后尝试启动后端，出现错误：
```
RuntimeError: Please destroy the QApplication singleton before creating a new Application instance.
```

## 原因分析

PySide6的`QApplication`是单例模式：
- 一个进程只能有一个`QApplication`实例
- 前端创建了`QApplication`实例
- 前端关闭后，`QApplication`实例仍然存在（未完全销毁）
- 后端尝试创建新的`QApplication`时失败

## 解决方案

使用`multiprocessing`在**独立进程**中启动后端：
- 每个进程有独立的`QApplication`实例
- 前端进程和后端进程互不干扰
- 避免QApplication冲突

## 实现细节

### 1. 修改导入
```python
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
import multiprocessing  # 添加multiprocessing
```

### 2. 在独立进程中启动后端
```python
def launch_backend_in_process():
    def run_backend():
        # 在新进程中重新导入后端模块
        # 调用backend_run_module._run()
    
    # Windows上使用spawn方式
    if sys.platform == 'win32':
        multiprocessing.set_start_method('spawn', force=True)
    
    # 启动独立进程
    backend_process = multiprocessing.Process(target=run_backend)
    backend_process.start()
```

### 3. 使用QTimer延迟启动
```python
# 延迟启动后端，确保前端窗口先关闭
QTimer.singleShot(200, delayed_launch)
```

## 优势

1. **完全隔离**：前端和后端在不同进程中运行
2. **无冲突**：每个进程有独立的QApplication实例
3. **稳定性**：一个进程崩溃不影响另一个
4. **符合PyInstaller原则**：使用函数调用，不是subprocess

## 注意事项

- Windows上multiprocessing需要使用`spawn`方式（默认）
- 后端进程是daemon=False，主进程退出后继续运行
- 需要确保后端模块在新进程中可以正确导入

## 测试

1. 运行打包后的EXE
2. 点击"Fox it!"按钮
3. 前端应该关闭
4. 后端（狐狸宠物）应该在新进程中启动
5. 不应该出现QApplication冲突错误
