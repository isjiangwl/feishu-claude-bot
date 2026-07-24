@echo off
chcp 65001 >nul
echo ========================================
echo   初始化 Git 并提交代码
echo ========================================
echo.

cd /d D:\install_d\feishu\feishu-claude-bot

echo [1/4] 初始化 Git...
git init

echo [2/4] 添加所有文件...
git add .

echo [3/4] 提交代码...
git commit -m "Feishu Claude Bot"

echo [4/4] 完成！
echo.
echo ========================================
echo   下一步：去 GitHub 创建仓库
echo   1. 打开 https://github.com/new
echo   2. 仓库名：feishu-claude-bot
echo   3. 点击 Create repository
echo   4. 复制仓库地址
echo ========================================
echo.
pause
