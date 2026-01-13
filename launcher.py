"""
FoxMate AI - 统一入口点
根据命令行参数启动前端或后端
"""
import sys
from pathlib import Path

# 支持PyInstaller打包路径
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    FRONTEND_DIR = BASE_DIR / 'frontend'
    BACKEND_DIR = BASE_DIR / 'backend'
else:
    BASE_DIR = Path(__file__).resolve().parent
    FRONTEND_DIR = BASE_DIR / 'frontend'
    BACKEND_DIR = BASE_DIR / 'backend'

# 添加路径到sys.path
sys.path.insert(0, str(FRONTEND_DIR))
sys.path.insert(0, str(BACKEND_DIR))

# === 顶层导入（让PyInstaller检测依赖） ===
# 这些import语句必须在顶层，让PyInstaller分析时能检测到所有依赖
# 即使某些导入可能失败（开发环境路径问题），也要有import语句
try:
    # 导入前端模块（让PyInstaller打包frontend/app.py及其依赖）
    import app as _frontend_app_module
except (ImportError, ModuleNotFoundError):
    # 开发环境中可能失败，这是正常的
    _frontend_app_module = None

try:
    # 导入后端模块（让PyInstaller打包backend/run.py及其依赖）
    import run as _backend_run_module
except (ImportError, ModuleNotFoundError):
    # 开发环境中可能失败，这是正常的
    _backend_run_module = None


def run_frontend():
    """启动前端应用"""
    print("🦊 Starting Frontend...")
    try:
        # 使用顶层导入的模块
        if _frontend_app_module is not None:
            _frontend_app_module.main()
        else:
            # 如果顶层导入失败，尝试重新导入
            if str(FRONTEND_DIR) not in sys.path:
                sys.path.insert(0, str(FRONTEND_DIR))
            import app
            app.main()
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        import traceback
        traceback.print_exc()
        print(f"\nDEBUG INFO:")
        print(f"  FRONTEND_DIR = {FRONTEND_DIR}")
        print(f"  FRONTEND_DIR exists = {FRONTEND_DIR.exists()}")
        if FRONTEND_DIR.exists():
            app_file = FRONTEND_DIR / "app.py"
            print(f"  app.py exists = {app_file.exists()}")
        print(f"  sys.path = {sys.path[:5]}")  # 只显示前5个
        input("Press Enter to exit...")
        sys.exit(1)


def run_backend():
    """启动后端应用"""
    print("🦊 Starting Backend...")
    try:
        # 使用顶层导入的模块
        if _backend_run_module is not None:
            _backend_run_module._run()
        else:
            # 如果顶层导入失败，尝试重新导入
            if str(BACKEND_DIR) not in sys.path:
                sys.path.insert(0, str(BACKEND_DIR))
            import run
            run._run()
    except Exception as e:
        print(f"❌ Backend error: {e}")
        import traceback
        traceback.print_exc()
        print(f"\nDEBUG INFO:")
        print(f"  BACKEND_DIR = {BACKEND_DIR}")
        print(f"  BACKEND_DIR exists = {BACKEND_DIR.exists()}")
        if BACKEND_DIR.exists():
            run_file = BACKEND_DIR / "run.py"
            print(f"  run.py exists = {run_file.exists()}")
        print(f"  sys.path = {sys.path[:5]}")  # 只显示前5个
        input("Press Enter to exit...")
        sys.exit(1)


def main():
    """主入口点"""
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--backend':
        # 启动后端
        run_backend()
    else:
        # 默认启动前端
        run_frontend()


if __name__ == "__main__":
    main()
