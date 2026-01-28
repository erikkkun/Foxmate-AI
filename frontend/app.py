from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QFrame,
    QPushButton
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
import sys
import os
import tempfile
from pathlib import Path

# Support PyInstaller bundled path
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    FRONTEND_DIR = BASE_DIR / 'frontend'
else:
    BASE_DIR = Path(__file__).resolve().parent
    FRONTEND_DIR = BASE_DIR

sys.path.insert(0, str(FRONTEND_DIR))

from routes import Route

# pages
from pages.home import HomePage
from pages.my_info import MyInfoPage
from pages.membership import MembershipPage
from pages.customize import CustomizePage
from pages.weekly_report import WeeklyReportPage
from pages.settings import SettingsPage
from pages.faq import FAQPage
from pages.welcome import WelcomePage
from pages.launching import LaunchingPage
from pages.auth import AuthPage


# === Backend module import (for PyInstaller) ===
_backend_module = None
try:
    backend_path = Path(__file__).resolve().parent.parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    import run as backend_run_module  # PyInstaller will detect
    _backend_module = backend_run_module
except (ImportError, ModuleNotFoundError):
    _backend_module = None


# Support PyInstaller bundled path
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys._MEIPASS) / 'frontend'
else:
    APP_DIR = Path(__file__).parent


class Overlay(QWidget):
    """半透明遮罩（点击可关闭 Drawer）"""
    def __init__(self, parent, on_click):
        super().__init__(parent)
        self.on_click = on_click
        self.setObjectName("overlay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.hide()

    def mousePressEvent(self, e):
        if self.isVisible():
            self.on_click()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(420, 750)
        self.setWindowTitle("")

        icon = APP_DIR / "assets" / "icon.ico"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))

        # ===== stack =====
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        def goto(route: Route):
            index = list(self.pages.keys()).index(route)
            self.stack.setCurrentIndex(index)

        home = HomePage(
            on_menu=self.toggle_menu,
            on_settings=lambda: goto(Route.SETTINGS),
            on_close=self.close,
            on_go_fox=lambda: goto(Route.FOX) if Route.FOX in self.pages else goto(Route.HOME),
            on_go_weekly=lambda: goto(Route.WEEKLY),
            on_fox_it=lambda: self.start_backend_and_exit()
        )
        home.on_signin = lambda: goto(Route.AUTH)

        self.pages: dict[Route, QWidget] = {
            Route.WELCOME: WelcomePage(),
            Route.LAUNCHING: LaunchingPage(),
            Route.HOME: home,
            Route.AUTH: AuthPage(
                on_back=lambda: goto(Route.HOME),
                on_login_success=self._on_login_success
            ),
            Route.MY_INFO: MyInfoPage(
                on_logout=self._logout,
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=lambda: goto(Route.HOME)
            ),
            Route.CUSTOMIZE: CustomizePage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=lambda: goto(Route.HOME)
            ),
            Route.MEMBERSHIP: MembershipPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=lambda: goto(Route.HOME)
            ),
            Route.WEEKLY: WeeklyReportPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=lambda: goto(Route.HOME)
            ),
            Route.SETTINGS: SettingsPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=lambda: goto(Route.HOME)
            ),
            Route.FAQ: FAQPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=lambda: goto(Route.HOME)
            ),
        }

        for _, page in self.pages.items():
            self.stack.addWidget(page)

        # start: welcome -> home after 3s
        self.stack.setCurrentIndex(0)
        QTimer.singleShot(3000, lambda: goto(Route.HOME))

        # ===== Drawer + Overlay =====
        self.drawer_margin = 16
        self.drawer_radius = 22
        self.drawer_width = int(self.width() * 0.78)

        self.overlay = Overlay(self, on_click=self.hide_menu)

        self.drawer = QFrame(self)
        self.drawer.setObjectName("drawer")
        self.drawer.setAttribute(Qt.WA_StyledBackground, True)
        self.menu_items = [
            ("My Account",   Route.MY_INFO),
            ("Customize",    Route.CUSTOMIZE),
            ("Membership",   Route.MEMBERSHIP),
            ("Weekly Report",Route.WEEKLY),
            ("Setting",      Route.SETTINGS),
            ("FAQ & Contact Us", Route.FAQ),
            ("🏠 Home",       Route.HOME),
        ]

        self.drawer_close = QPushButton("✕", self.drawer)
        self.drawer_close.setObjectName("drawerClose")  # ✅ theme hook
        self.drawer_close.setFixedSize(28, 28)
        self.drawer_close.clicked.connect(self.hide_menu)

        self.drawer_buttons: list[QPushButton] = []
        for text, route in self.menu_items:
            btn = QPushButton(text, self.drawer)
            btn.setProperty("route", route)
            btn.setProperty("drawerItem", "true")  # ✅ 关键：让 theme 命中抽屉按钮样式
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(44)
            btn.clicked.connect(self._on_drawer_click)
            self.drawer_buttons.append(btn)

        self.anim = QPropertyAnimation(self.drawer, b"geometry")
        self.menu_open = False
        self._layout_drawer()

        self._drag_pos = None

    # drag window
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

    def _on_login_success(self, username: str):
        self.current_user = {
            "username": username,
            "email": f"{username}@fox.com",
            "telephone": "1234567890",
            "school": "UCLA",
            "password": "123"
        }
        self.pages[Route.HOME].update_login_ui(True, username, "White Fox")
        self.pages[Route.MY_INFO].update_user_data(self.current_user)

    # drawer click
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
        self.overlay.show()
        self.overlay.raise_()

        w = self.drawer_width
        h = self.height() - self.drawer_margin * 2

        self.anim.stop()
        self.anim.setDuration(250)
        self.anim.setStartValue(QRect(-w, self.drawer_margin, w, h))
        self.anim.setEndValue(QRect(self.drawer_margin, self.drawer_margin, w, h))
        self.drawer.show()
        self.drawer.raise_()
        self.anim.start()

    def hide_menu(self):
        self.menu_open = False

        w = self.drawer_width
        h = self.height() - self.drawer_margin * 2

        self.anim.stop()
        self.anim.setDuration(220)
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

    def _logout(self):
        self.current_user = None

        self.pages[Route.HOME].update_login_ui(
            logged_in=False,
            username="",
            membership=""
        )

        self.pages[Route.MY_INFO].update_user_data({
            "username": " ",
            "email": " ",
            "telephone": " ",
            "school": " ",
            "password": " "
        })

        self.stack.setCurrentIndex(list(self.pages.keys()).index(Route.HOME))

    def start_backend_and_exit(self):
        """
        1) switch to launching page
        2) start backend process with FOXMATE_READY_FLAG
        3) poll for ready flag -> quit frontend
        """
        import subprocess

        # 1) show launching
        try:
            idx_launch = list(self.pages.keys()).index(Route.LAUNCHING)
            self.stack.setCurrentIndex(idx_launch)
            QApplication.processEvents()
        except Exception:
            pass

        # 2) ready flag
        ready_flag = Path(tempfile.gettempdir()) / "foxmate_backend_ready.flag"
        try:
            if ready_flag.exists():
                ready_flag.unlink()
        except Exception:
            pass

        env = os.environ.copy()
        env["FOXMATE_READY_FLAG"] = str(ready_flag)

        try:
            if getattr(sys, 'frozen', False):
                exe_path = Path(sys.executable)
                self._backend_proc = subprocess.Popen(
                    [str(exe_path), "--backend"],
                    env=env,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
                )
            else:
                launcher_path = Path(__file__).resolve().parent.parent / "launcher.py"
                self._backend_proc = subprocess.Popen(
                    [sys.executable, str(launcher_path), "--backend"],
                    env=env,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
                )
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            try:
                idx_home = list(self.pages.keys()).index(Route.HOME)
                self.stack.setCurrentIndex(idx_home)
            except Exception:
                pass
            return

        # 3) poll ready flag
        self._ready_poll_timer = QTimer(self)
        self._ready_poll_timer.setInterval(200)

        def _check_ready():
            if ready_flag.exists():
                self._ready_poll_timer.stop()
                QApplication.instance().quit()
                return

            if getattr(self, "_backend_proc", None) is not None:
                code = self._backend_proc.poll()
                if code is not None:
                    self._ready_poll_timer.stop()
                    print(f"❌ Backend exited early (code={code}), ready flag not found.")
                    try:
                        idx_home = list(self.pages.keys()).index(Route.HOME)
                        self.stack.setCurrentIndex(idx_home)
                    except Exception:
                        pass

        self._ready_poll_timer.timeout.connect(_check_ready)
        self._ready_poll_timer.start()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("FocusMate")
    app.setFont(QFont("-apple-system, Segoe UI, Microsoft YaHei, Arial"))

    from theme import apply_theme
    apply_theme(app)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
