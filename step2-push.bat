@echo off
cd /d D:\install_d\feishu\feishu-claude-bot
git remote add origin https://github.com/isjiangwl/feishu-claude-bot.git
git branch -M main
git push -u origin main
echo Done!
pause
