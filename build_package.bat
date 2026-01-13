@echo off
echo ========================================
echo FoxMate AI 打包脚本
echo ========================================
echo.

REM 检查PyInstaller是否安装
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [错误] PyInstaller未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller安装失败，请手动安装: pip install pyinstaller
        pause
        exit /b 1
    )
)

echo [信息] 开始打包...
echo.

REM 清理旧的构建文件
if exist "build" (
    echo [信息] 清理旧的构建文件...
    rmdir /s /q build
)

if exist "dist" (
    echo [信息] 清理旧的打包文件...
    rmdir /s /q dist
)

REM 执行打包
pyinstaller "FoxMate AI.spec"

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 打包文件位置: dist\FoxMate AI\
echo.
echo 下一步：
echo 1. 测试 dist\FoxMate AI\FoxMate AI.exe 是否可以正常运行
echo 2. 将 dist\FoxMate AI\ 文件夹压缩为ZIP文件
echo 3. 将 README.txt 添加到ZIP文件中
echo.
pause
