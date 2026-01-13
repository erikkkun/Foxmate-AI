
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QFrame,
    QPushButton, QLabel
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
import sys
import os
from pathlib import Path

# Support PyInstaller bundled path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
    FRONTEND_DIR = BASE_DIR / 'frontend'
else:
    # Running as script
    BASE_DIR = Path(__file__).resolve().parent
    FRONTEND_DIR = BASE_DIR

sys.path.insert(0, str(FRONTEND_DIR))

from routes import Route

# 页面导入
from pages.home import HomePage
from pages.my_info import MyInfoPage
from pages.membership import MembershipPage
from pages.customize import CustomizePage
from pages.weekly_report import WeeklyReportPage
from pages.workshop import WorkshopPage
from pages.fox_pet import FoxPetPage
from pages.shop import ShopPage
from pages.settings import SettingsPage
from pages.signin import SignInDialog
from pages.faq import FAQPage

from PySide6.QtWidgets import QDialog

# === 后端模块导入（必须在顶层，让PyInstaller正确打包） ===
# 根据PyInstaller原则：主脚本必须在顶层导入所有需要的模块
# 这样PyInstaller才能检测并打包backend模块及其所有依赖
#
# 关键：必须有无条件的import语句让PyInstaller检测到
# 即使导入可能失败（开发环境路径问题），也要有import语句

_backend_module = None  # 后端模块的引用

# 尝试导入后端模块（让PyInstaller在打包时检测到依赖）
# 注意：这里使用try-except，因为开发环境路径可能不同
# 但import语句本身必须存在，让PyInstaller分析时能检测到
try:
    # 开发环境：尝试从父目录导入
    # 这个import语句让PyInstaller知道需要打包backend/run.py
    backend_path = Path(__file__).resolve().parent.parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    # 关键：这个import语句必须存在，让PyInstaller检测到
    import run as backend_run_module  # PyInstaller会分析这个导入
    _backend_module = backend_run_module
except (ImportError, ModuleNotFoundError):
    # 开发环境中可能失败（路径问题），这是正常的
    # 在打包后，会从_MEIPASS正确导入
    _backend_module = None



# Support PyInstaller bundled path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    APP_DIR = Path(sys._MEIPASS) / 'frontend'
else:
    # Running as script
APP_DIR = Path(__file__).parent


class Overlay(QWidget):
    """半透明遮罩（点击可关闭 Drawer）"""
    def __init__(self, parent, on_click):
        super().__init__(parent)
        self.on_click = on_click
        self.setStyleSheet("background: rgba(0,0,0,140);")
        self.hide()

    def mousePressEvent(self, e):
        if self.isVisible():
            self.on_click()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(420, 750)                 # 竖屏手机大小
        self.setWindowTitle("")

        icon = APP_DIR / "assets" / "icon.ico"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))

        # ===== 主内容区 =====
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 统一跳转
        def goto(route: Route):
            index = list(self.pages.keys()).index(route)
            self.stack.setCurrentIndex(index)

        
        home = HomePage(
            on_menu=self.toggle_menu,
            on_settings=lambda: goto(Route.SETTINGS),
            on_close=self.close,
            on_go_fox=lambda: goto(Route.FOX),
            on_go_weekly=lambda: goto(Route.WEEKLY),
            on_fox_it=lambda: self.start_backend_and_exit()
        )
        home.on_signin = self.open_signin_dialog

        self.pages: dict[Route, QWidget] = {
            Route.HOME: home,
            Route.MY_INFO: MyInfoPage(
                # user_data={"username": "test", "email": "test@fox.com", "telephone": "1234567890", "school": "UCLA", "password": "123"},
                on_logout=self._logout,
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),

            Route.CUSTOMIZE: CustomizePage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),
            Route.MEMBERSHIP: MembershipPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),
            Route.WEEKLY: WeeklyReportPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),

            Route.WORKSHOP: WorkshopPage(),
            Route.FOX: FoxPetPage(),
            Route.SHOP: ShopPage(),
            Route.SETTINGS: SettingsPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),
            Route.FAQ: FAQPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),

        }
        for _, page in self.pages.items():
            self.stack.addWidget(page)
        self.stack.setCurrentIndex(0)

        # ===== 抽屉菜单 + 遮罩 =====
        self.drawer_margin = 16
        self.drawer_radius = 22
        self.drawer_width = int(self.width() * 0.78)

        self.overlay = Overlay(self, on_click=self.hide_menu)

        self.drawer = QFrame(self)
        self.drawer.setObjectName("drawer")
        self.drawer.setStyleSheet(f"""
            QFrame#drawer {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #137a7f, stop:1 #0c9d8c);
                border-radius: {self.drawer_radius}px;
            }}
        """)

        self.menu_items = [
            ("My Account",   Route.MY_INFO),
            ("Customize",    Route.CUSTOMIZE),
            ("Membership",   Route.MEMBERSHIP),
            ("Weekly Report",Route.WEEKLY),
            ("Workshop",     Route.WORKSHOP),
            ("Your Fox",     Route.FOX),
            ("Setting",      Route.SETTINGS),
            ("FAQ & Contact Us", Route.FAQ),
            ("🏠 Home",       Route.HOME),   # ✅ 新增 Home 按钮
        ]

        self.drawer_close = QPushButton("✕", self.drawer)
        self.drawer_close.setFixedSize(28, 28)
        self.drawer_close.setStyleSheet("""
            QPushButton { color:white; border:none; font-size:18px; }
            QPushButton:hover { background: rgba(255,255,255,0.12); border-radius:14px; }
        """)
        self.drawer_close.clicked.connect(self.hide_menu)

        self.drawer_buttons: list[QPushButton] = []
        for text, route in self.menu_items:
            btn = QPushButton(text, self.drawer)
            btn.setProperty("route", route)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(44)
            btn.setStyleSheet("""
                QPushButton { color: #fff; font-size: 20px; padding: 12px 14px; text-align:left; border:none; }
                QPushButton:hover { background: rgba(255,255,255,0.08); }
            """)
            btn.clicked.connect(self._on_drawer_click)
            self.drawer_buttons.append(btn)

        self.anim = QPropertyAnimation(self.drawer, b"geometry")
        self.menu_open = False
        self._layout_drawer()

        self._drag_pos = None

    # ---- Frameless 拖动支持 ----
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e):
        if self._drag_pos and (e.buttons() & Qt.LeftButton):
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            e.accept()

    def mouseReleaseEvent(self, e):
        self._drag_pos = None

    # ---- Drawer 逻辑 ----
    def _on_drawer_click(self):
        sender: QPushButton = self.sender()
        route = sender.property("route")
        index = list(self.pages.keys()).index(route)
        self.stack.setCurrentIndex(index)
        self.hide_menu()

    def _layout_drawer(self):
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        w = self.drawer_width
        h = self.height() - self.drawer_margin * 2
        y = self.drawer_margin
        x_hidden = -w
        x_shown = self.drawer_margin
        current_x = x_hidden if not self.menu_open else x_shown
        self.drawer.setGeometry(current_x, y, w, h)
        self.drawer_close.move(w - 36, 8)
        top = 50
        gap = 8
        for i, btn in enumerate(self.drawer_buttons):
            btn.setGeometry(14, top + i * (44 + gap), w - 28, 44)

    def toggle_menu(self):
        self.show_menu() if not self.menu_open else self.hide_menu()

    def show_menu(self):
        self.menu_open = True
        self.overlay.show(); self.overlay.raise_()
        w = self.drawer_width; h = self.height() - self.drawer_margin * 2
        self.anim.stop(); self.anim.setDuration(250)
        self.anim.setStartValue(QRect(-w, self.drawer_margin, w, h))
        self.anim.setEndValue(QRect(self.drawer_margin, self.drawer_margin, w, h))
        self.drawer.show(); self.drawer.raise_()
        self.anim.start()

    def hide_menu(self):
        self.menu_open = False
        w = self.drawer_width; h = self.height() - self.drawer_margin * 2
        self.anim.stop(); self.anim.setDuration(220)
        self.anim.setStartValue(QRect(self.drawer_margin, self.drawer_margin, w, h))
        self.anim.setEndValue(QRect(-w, self.drawer_margin, w, h))
        try:
            self.anim.finished.disconnect(self.overlay.hide)
        except TypeError:
            pass
        self.anim.finished.connect(self.overlay.hide)
        self.anim.start()

    def resizeEvent(self, e):
        self.drawer_width = int(self.width() * 0.78)
        self._layout_drawer()
        return super().resizeEvent(e)
    
    def open_signin_dialog(self):
        dlg = SignInDialog(self)
        if dlg.exec() == QDialog.Accepted:  # ✅ 只关心结果
            username = dlg.username.text().strip()

            # mock 的用户数据（以后从数据库获取）
            self.current_user = {
                "username": username,
                "email": f"{username}@fox.com",
                "telephone": "1234567890",
                "school": "UCLA",
                "password": "123"
            }

            # 更新 UI
            self.pages[Route.HOME].update_login_ui(
                logged_in=True,
                username=self.current_user["username"],
                membership="White Fox"
            )
            self.pages[Route.MY_INFO].update_user_data(self.current_user)


            
    def _logout(self):
        print("已登出")
        self.current_user = None

        # Home 回到未登录
        self.pages[Route.HOME].update_login_ui(
            logged_in=False,
            username="",
            membership=""
        )

        # MyInfo 清空
        self.pages[Route.MY_INFO].update_user_data({
            "username": " ",
            "email": " ",
            "telephone": " ",
            "school": " ",
            "password": " "
        })

        # 回到 Home
        self.stack.setCurrentIndex(list(self.pages.keys()).index(Route.HOME))
        
    def start_backend_and_exit(self):
        """
        关闭前端并启动后端。
        
        使用subprocess启动同一个exe，传递--backend参数。
        这是最简单可靠的方法，避免了multiprocessing的pickle问题和QApplication冲突。
        """
        import subprocess
        
        try:
            if getattr(sys, 'frozen', False):
                # 打包环境：启动同一个exe，传递--backend参数
                exe_path = Path(sys.executable)  # sys.executable指向exe本身
                print(f"🚀 Launching backend: {exe_path} --backend")
                
                # 启动后端进程（独立进程，避免QApplication冲突）
                subprocess.Popen([str(exe_path), '--backend'], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
            else:
                # 开发环境：使用Python运行launcher.py
                launcher_path = Path(__file__).resolve().parent.parent / "launcher.py"
                print(f"🚀 Launching backend: python {launcher_path} --backend")
                
                subprocess.Popen([sys.executable, str(launcher_path), '--backend'],
                               creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
            
            print("✅ Backend process started")
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            import traceback
            traceback.print_exc()
            # 显示错误消息
            try:
                from PySide6.QtWidgets import QMessageBox
                msg = QMessageBox()
                msg.setWindowTitle("Backend Error")
                msg.setText(f"Failed to start backend:\n{str(e)}\n\nCheck console for details.")
                msg.exec()
            except:
                pass
        
        # 关闭前端
        app = QApplication.instance()
        if app:
            app.quit()






def main():
    app = QApplication(sys.argv)
    app.setApplicationName("FocusMate")
    app.setFont(QFont("-apple-system, Segoe UI, Microsoft YaHei, Arial"))
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
