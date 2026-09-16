@echo off
title 5개국 중앙은행 환율 대시보드
cd /d "%~dp0"
echo 환율 대시보드 웹 서버를 시작합니다...
start http://localhost:8080
python server.py 8080
pause
