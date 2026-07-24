@echo off
chcp 65001 >nul
echo ========================================
echo   上传代码到 GitHub
echo ========================================
echo.

cd /d D:\install_d\feishu\feishu-claude-bot

echo [1/3] 添加远程仓库...
git remote add origin https://github.com/isjiangwl/feishu-claude-bot.git

echo [2/3] 推送代码...
git branch -M main
git push -u origin main

echo [3/3] 完成！
echo.
echo ========================================
echo   代码已上传！
echo   下一步：去 Railway 部署
echo   1. 打开 https://railway.app/
echo   2. 登录（用 GitHub 账号）
echo   3. New Project -> Deploy from GitHub repo
echo   4. 选择 feishu-claude-bot 仓库
echo ========================================
echo.
pause
