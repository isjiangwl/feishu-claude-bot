@echo off
chcp 65001 >nul
echo ========================================
echo   Railway 命令行部署
echo ========================================
echo.

echo [1/3] 安装 Railway CLI...
npm install -g @railway/cli

echo [2/3] 登录 Railway...
railway login

echo [3/3] 初始化项目...
cd /d D:\install_d\feishu\feishu-claude-bot
railway init

echo.
echo ========================================
echo   登录后按提示操作
echo   完成后告诉我
echo ========================================
pause
