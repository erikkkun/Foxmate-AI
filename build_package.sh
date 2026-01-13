#!/bin/bash

echo "========================================"
echo "FoxMate AI 打包脚本"
echo "========================================"
echo ""

# 检查PyInstaller是否安装
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "[错误] PyInstaller未安装，正在安装..."
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "[错误] PyInstaller安装失败，请手动安装: pip install pyinstaller"
        exit 1
    fi
fi

echo "[信息] 开始打包..."
echo ""

# 清理旧的构建文件
if [ -d "build" ]; then
    echo "[信息] 清理旧的构建文件..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "[信息] 清理旧的打包文件..."
    rm -rf dist
fi

# 执行打包
pyinstaller "FoxMate AI.spec"

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 打包失败！"
    exit 1
fi

echo ""
echo "========================================"
echo "打包完成！"
echo "========================================"
echo ""
echo "打包文件位置: dist/FoxMate AI/"
echo ""
echo "下一步："
echo "1. 测试 dist/FoxMate AI/FoxMate AI.exe 是否可以正常运行"
echo "2. 将 dist/FoxMate AI/ 文件夹压缩为ZIP文件"
echo "3. 将 README.txt 添加到ZIP文件中"
echo ""
